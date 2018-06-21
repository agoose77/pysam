import asyncio


class Actions:
    """1. Actions are triggered by events, and translate event into proposed values changes to the model"""

    def __init__(self, model):
        self.model = model

    async def decrement(self, data):
        await asyncio.sleep(1.0)
        data.counter -= 1
        await self.model.present(data)

    async def launch(self, data):
        data.launched = True
        await self.model.present(data)
