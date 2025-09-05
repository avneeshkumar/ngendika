import asyncio
import websockets

class AudioRelayServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = set()

    async def relay(self, sender, data):
        recipients = [client for client in self.clients if client != sender]
        for client in recipients:
            try:
                await client.send(data)
            except Exception as e:
                print(f"Error sending data to client: {e}")

    async def handle_connection(self, websocket, path=None):
        self.clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.clients)}")
        try:
            async for data in websocket:
                await self.relay(websocket, data)
        except websockets.exceptions.ConnectionClosedOK:
            print("Client disconnected gracefully.")
        except Exception as e:
            print(f"Error in websocket handling: {e}")
        finally:
            self.clients.remove(websocket)
            print(f"Client disconnected. Total clients: {len(self.clients)}")

    async def start(self):
        async with websockets.serve(self.handle_connection, self.host, self.port, ping_timeout=None, ping_interval=10):
            print(f"Server running on ws://{self.host}:{self.port}")
            await asyncio.Future()

if __name__ == "__main__":
    server = AudioRelayServer("192.168.1.45", 8766)
    asyncio.run(server.start())
