import asyncio
import websockets
import pyaudio

class AudioServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.chunk = 1024
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100

    async def handle_connection(self, websocket, path=None):  # <-- Updated signature
        p = pyaudio.PyAudio()
        print("Streaming audio...")
        try:
            stream = p.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.rate,
                output=True,
                frames_per_buffer=self.chunk,
            )
            try:
                async for data in websocket:
                    stream.write(data, exception_on_underflow=False)
            except websockets.exceptions.ConnectionClosedOK:
                print("Client disconnected gracefully.")
            except Exception as e:
                print(f"Error in websocket handling: {e}")
            finally:
                stream.stop_stream()
                stream.close()
        except Exception as e:
            print(f"Error opening audio stream: {e}")
        finally:
            p.terminate()
            print("Connection closed.")

    async def start(self):
        async with websockets.serve(self.handle_connection, self.host, self.port, ping_timeout=None, ping_interval=10):
            await asyncio.Future()

if __name__ == "__main__":
    server = AudioServer("192.168.1.45", 8766)
    asyncio.run(server.start())