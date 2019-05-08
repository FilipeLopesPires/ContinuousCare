import json
import asyncio
import websockets
from threading import Thread
import logging
logging.basicConfig(level=logging.DEBUG)


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
        logging.debug("WEBSOCKET STARTED IN "+self.host+":"+str(self.port))

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
            logging.debug("WEBSOCKET RECEIVED "+data)
            jsonData=json.loads(data)
            token=jsonData["token"]
            self.processor.checkPermissions(token)
            self.sockets[token]=websocket

    async def send(self, data, user):
        if user in self.sockets:
            await self.sockets[user].send(data)

    def getUsers(self):
        return self.sockets.keys()



'''

w = WSServer()
w.start()

i=input("-")
loop = asyncio.get_event_loop()  
loop.run_until_complete(w.send("banana", "Joao"))  
loop.close()  
'''

