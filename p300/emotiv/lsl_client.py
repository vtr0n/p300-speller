import json
from websockets.sync.client import connect

class Emotiv:

    def __init__(self, port=8765):
        self.port = port

    def start(self):
        with connect("ws://localhost:8765") as websocket:
            websocket.send("start")
            message = websocket.recv()

    def stop(self):
        with connect("ws://localhost:8765", max_size=1024 ** 3) as websocket:
            websocket.send("stop")
            data = websocket.recv()
            return json.loads(data)
