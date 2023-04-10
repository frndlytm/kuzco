from functools import reduce, singledispatchmethod

from ._interfaces import *
from ._types import *
from .filters import Map, Flatten

from .util import compose

PipelineStep = IReducer | IFilter | IMuxer | ITransformer


class ImmutablePipelineException(Exception): pass


class Pipeline:
    def __init__(self, chunksize: int = 20):
        self.chunksize = chunksize
        self.closed = False
        self.steps = []

    def __or__(self, step) -> "Pipeline":
        """Support the | operator for adding steps to the Pipeline."""
        return self.then(step)

    def __call__(self, channel: Channel) -> Message:
        """Execute the Sequence of steps on the Channel of Messages.

        Args:
            channel (Channel):
                A Channel of Messages

        Returns:
            Message:
                A Reduced form of the Channel down to a result set,
                potentially just a list of transformed messages

        """
        # If we don't have an IReducer on the end, then reduce the Channel
        # to a list, i.e., a finite result
        if not self.closed:
            self.steps.append(list)
            self.closed = True

        return reduce(compose, self.steps)(channel)

    @singledispatchmethod
    def then(self, _) -> "Pipeline":
        """
        `then` is the explicit method call to add a step to the pipeline. It
        dispatches based on type of the step to the following methods:
    
        `then_filter` adds an IFilter to the Pipeline. In general, a Pipeline
        is just a Sequence of filters that map over a channel to 

        `then_mux` adds an IMuxer to the Pipeline as a builder, i.e., returning
        the Pipeline we're building.
        
        Since IMuxers take a single Message and then turns it into a Channel,
        an IMuxer actually needs to combine Map and Flatten semantics to function
        effectively.

        `then_reduce` closes the Pipeline with an IReducer step and returns an
        updated Pipeline.

        `then_transform` adds an ITransform to the pipeline by adding a Map step
        for the ITransform onto the Pipeline.

        Args:
            step (IReducer):
                The IReducer we want to reduce the Channel by.

        Raises:
            ImmutablePipelineException:
                If the Pipeline is closed, we cannot add new steps

        Returns:
            Pipeline:
                This pipeline, configured with the new step.
        """
        raise NotImplementedError()

    @then.register(IFilter)
    def then_filter(self, step: IFilter) -> "Pipeline":
        if self.closed: raise ImmutablePipelineException()
        self.steps.append(step)
        return self

    @then.register(IMuxer)
    def then_mux(self, step: IMuxer) -> "Pipeline":
        if self.closed: raise ImmutablePipelineException()
        return self | Map(step) | Flatten()

    @then.register(IReducer)
    def then_reduce(self, step: IReducer) -> "Pipeline":
        if self.closed: raise ImmutablePipelineException()
        self.steps.append(step)
        self.closed = True
        return self

    @then.register(ITransformer)
    def then_transform(self, step: ITransformer) -> "Pipeline":
        if self.closed: raise ImmutablePipelineException()
        return self | Map(step)
