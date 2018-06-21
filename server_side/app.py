from json import loads

from actions import Actions
from model import Model, ModelData, COUNTER_MAX
from quart import Quart, websocket, g, Response
from state import State
from view import View

app = Quart(__name__)


@app.route('/')
async def main() -> Response:
    """Return main index file which exposes a subset of actions in JS"""
    return await app.send_static_file("index.html")


def init(namespace):
    """Initialise SAM for the current user in a given namespace"""
    namespace.model = Model(counter=COUNTER_MAX)
    namespace.actions = Actions(namespace.model)
    namespace.view = View()
    namespace.state = State(namespace.view, namespace.actions)
    namespace.model.state = namespace.state


@app.websocket('/ws')
async def ws():
    """Websocket entry point (represents a client session) for sending view updates & receiving actions"""
    init(g)

    # Initialise the view
    await g.view.display(g.view.init(g.model))

    while True:
        # Receive proposition from client
        data = await websocket.receive()

        # Send proposition to model
        proposition = ModelData(**loads(data))
        await g.model.present(proposition)


if __name__ == "__main__":
    app.run()
