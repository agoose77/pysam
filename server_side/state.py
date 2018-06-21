import asyncio
from functools import wraps

from quart import copy_current_websocket_context
from model import ModelData, COUNTER_MAX


def ensure_future_with_ws_ctx(coro_fun):
    """Calls ensure future on coroutine whilst maintaining websocket context"""

    @wraps(coro_fun)
    def wrapper(*args, **kwargs):
        coro = copy_current_websocket_context(coro_fun)(*args, **kwargs)
        asyncio.ensure_future(coro)

    return wrapper


class State:
    """3. State function computes the State Representation from the Model property values and makes sure that everyone
    who needs to "learn"" about the new application state is notified, such as the view which will display the
    “state representation”.
    Then computes the next-action-predicate which will invoke any automatic action, given the current application state
    """

    def __init__(self, view, actions):
        self.view = view
        self.actions = actions

    @staticmethod
    def counting(model) -> bool:
        return 0 <= model.counter <= COUNTER_MAX and \
               model.started and not (model.launched or model.aborted)

    @staticmethod
    def ready(model) -> bool:
        return model.counter == COUNTER_MAX and \
               not (model.started or model.launched or model.aborted)

    @staticmethod
    def launched(model) -> bool:
        return not model.counter and model.started and model.launched and \
               not model.aborted

    @staticmethod
    def aborted(model):
        return 0 <= model.counter <= COUNTER_MAX and \
               model.started and model.aborted and not model.launched

    async def next_action_predicate(self, model):
        """Next-Action-Predicate (nap) used to invoke automatic actions where necessary (e.g the counting process)"""
        if self.counting(model):
            if model.counter:
                # Use ensure future to prevent blocking of user requests
                ensure_future_with_ws_ctx(self.actions.decrement)(ModelData(counter=model.counter))
            else:
                ensure_future_with_ws_ctx(self.actions.launch)(ModelData())

    async def render(self, model):
        await self.representation(model)
        await self.next_action_predicate(model)

    async def representation(self, model):
        representation = "oops... something went wrong"

        if self.ready(model):
            representation = self.view.ready(model)

        if self.counting(model):
            representation = self.view.counting(model)

        if self.launched(model):
            representation = self.view.launched(model)

        if self.aborted(model):
            representation = self.view.aborted(model)

        await self.view.display(representation)
