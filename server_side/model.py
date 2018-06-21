COUNTER_MAX = 10


class ModelData:
    """Container representing model state and proposition"""

    def __init__(self, **kwargs):
        self.counter = None
        self.started = False
        self.launched = False
        self.aborted = False

        vars(self).update(**kwargs)


class Model(ModelData):
    """2. Model is responsible for accepting, rejecting, or partially rejecting action propositions, and re-rendering the
    """
    state = None

    async def present(self, data):
        if self.state.counting(self):
            if not self.counter:
                self.launched = data.launched
            else:
                self.aborted = data.aborted
                if data.counter is not None:
                    self.counter = data.counter
        else:
            if self.state.ready(self):
                self.started = data.started

        await self.state.render(self)
