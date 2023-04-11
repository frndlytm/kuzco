from functools import reduce, singledispatchmethod

from ._interfaces import *
from ._types import *
from . import filters, reducers, transformers

from .util import compose

PipelineStep = IReducer | IFilter | IMuxer | ITransformer


class ImmutablePipelineException(Exception): pass


class Pipeline(IReducer):
    """
    Pipelines are the composition of many filters applied to the Messages
    on a Channel. Specifically, iteratively building a Pipeline is the same
    as adding a step to the run method by function composition.

    A Pipeline is a callable function that takes in a Channel of messages and
    returns a Message, therefore it is an IReducer implementation.

    By default, a Pipeline auto-configures itself to Collect the results of
    the pipeline into a list; however, ending a building process with an IReducer
    overrides that behavior.
    """
    def __init__(self, chunksize: int = 20):
        self.chunksize = chunksize
        self.closed = False
        self.run = filters.Map(transformers.Identity())

    def __or__(self, step) -> "Pipeline":
        """Support the | operator for adding steps to the Pipeline."""
        return self.then(step)

    def reduce(self, channel: Channel) -> Message:
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
            self.run = compose(self.run, reducers.Collect())
            self.closed = True

        return self.run(channel)

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
        if self.closed:
            raise ImmutablePipelineException()

        self.run = compose(self.run, step)
        return self

    @then.register(IMuxer)
    def then_mux(self, step: IMuxer) -> "Pipeline":
        if self.closed:
            raise ImmutablePipelineException()

        self.run = compose(self.run, filters.Map(step))
        self.run = compose(self.run, filters.Flatten())
        return self

    @then.register(IReducer)
    def then_reduce(self, step: IReducer) -> "Pipeline":
        if self.closed:
            raise ImmutablePipelineException()

        self.run = compose(self.run, step)
        self.closed = True
        return self

    @then.register(ITransformer)
    def then_transform(self, step: ITransformer) -> "Pipeline":
        if self.closed:
            raise ImmutablePipelineException()

        self.run = compose(self.run, filters.Map(step))
        return self
