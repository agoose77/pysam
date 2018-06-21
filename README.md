# pysam
State-Action-Model demo in Python. Based upon http://sam.js.org/

## server_side
A server side demonstration of SAM, where the client provides the actions (those which are not used by the next-action-predicate (nap)), and the server provides the View, Model, and State.
Websockets are used to communicate between the server and client, and to maintain the global state (model) for each client. View updates are returned to the client, and rendered to a `div`.

Run `python3 app.py`, and navigate to http://localhost:5000/ to try the demo.