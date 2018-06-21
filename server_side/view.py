from quart import websocket


class View:
    """Serves view (HTML) from model data"""

    def init(self, model):
        return self.ready(model)

    @staticmethod
    async def display(representation: str):
        """Send view data to remote display (browser)"""
        await websocket.send(representation)

    @staticmethod
    def ready(model) -> str:
        return f"""
<p>T-{model.counter}</p>
<form onSubmit="JavaScript:return actions.start({{}});">
<input type="submit" value="Start">
</form>
"""

    @staticmethod
    def counting(model) -> str:
        return f"""
<p>T-{model.counter}</p>
<script>
    say('{model.counter}')
</script>
<form onSubmit="JavaScript:return actions.abort({{}});">
    <input type="submit" value="Abort">
</form>
"""

    @staticmethod
    def aborted(model) -> str:
        return f"<p>Aborted at T-{model.counter}</p>"

    @staticmethod
    def launched(model) -> str:
        return f"""
<p>Lift off!</p><p>
<audio autoplay>
  <source src="http://soundbible.com/grab.php?id=709&amp;type=wav">
Your browser does not support the audio element.
</audio>
<script>
    say('Lift off!')
</script>
<img src="https://png.pngtree.com/element_pic/00/16/10/0457f28e64241b1.jpg"></img></p>"""
