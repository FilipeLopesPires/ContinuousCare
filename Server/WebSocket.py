import json
import asyncio
import websockets
from threading import Thread
import logging
logging.basicConfig(level=logging.INFO)


class WebSocket:

    def __init__(self, host, port, processor):
        self.sockets={}
        self.t=None
        self.host=host
        self.port=port
        self.processor=processor

    def start(self):
        self.t=Thread(target=self.serve_forever)
        self.t.start()
        logging.info("WEBSOCKET STARTED IN "+self.host+":"+str(self.port))

    def stop(self):
        self.t._stop()

    def serve_forever(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self.handler, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def handler(self, websocket, path):
        while True:
            data = await websocket.recv()
            logging.info("WEBSOCKET RECEIVED "+data)
            jsonData=json.loads(data)
            token=jsonData["token"]
            self.processor.checkPermissions(token)
            self.sockets[token]=websocket

    async def send(self, data, token):
        socket = self.sockets.get(token)
        if socket:
            await socket.send(data)

    def getUsers(self):
        return self.sockets.keys()

    def delToken(self, token):
        if token in self.sockets:
            self.sockets[token].close()
            del self.sockets[token]


'''

w = WSServer()
w.start()

i=input("-")
loop = asyncio.get_event_loop()  
loop.run_until_complete(w.send("banana", "Joao"))  
loop.close()  
'''

