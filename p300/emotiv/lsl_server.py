import asyncio
import json
import logging
import threading
import time

from pylsl import StreamInlet, resolve_stream
from websockets.server import serve

logging.basicConfig(level=logging.INFO)

class Watcher():
    
    def __init__(self):
        self.start = True
        self.buffer = []

        streams = resolve_stream('type', 'EEG')

        # create a new inlet to read from the stream
        self.inlet = StreamInlet(streams[0])
       
    def main(self):
        i = 0
        while True:
            sample, _ = self.inlet.pull_sample()
            sample = [el / 1000000 for el in sample]
            
            if i % 128 == 0:
                logging.info("Buffer size: %s", len(self.buffer))
            i += 1

            if self.start:
                sample.append(time.time())
                self.buffer.append(sample)

obj = Watcher()

async def echo(websocket):
    async for message in websocket:
        if message == "start":
            obj.start = True
            obj.buffer = []
            await websocket.send(json.dumps("ok"))
        elif message == "stop":
            obj.start = False
            await websocket.send(json.dumps(obj.buffer))


async def main():
    x = threading.Thread(target=obj.main,)
    x.start()

    async with serve(echo, "localhost", 8765, max_size=1024 ** 3):
        await asyncio.Future()  # run forever

asyncio.run(main())