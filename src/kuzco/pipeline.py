from functools import singledispatchmethod

PipelineStep = IAggregator | IFilter | IMuxer | ITransformer


class Pipeline:
    def __init__(self):
        self.steps = []

    def __or__(self, step: PipelineStep) -> "Pipeline":
        return self.then(step)

    @singledispatchmethod
    def then(self, step) -> Pipeline:
        raise NotImplementedError()

    @then.register(IAggregator)
    def then_aggregate(self, step):
        self.steps.append()

    @then.register(IFilter)
    def then_filter(self, step):
        ...

    @then.register(IMuxer)
    def then_mux(self, step):
        ...

    @then.register(ITransformer)
    def then_transform(self, step):
        ...
