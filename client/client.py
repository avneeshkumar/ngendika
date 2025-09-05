import asyncio
import websockets
import pyaudio
import sys
import time

class AudioClient:
    def __init__(self, name=None):
        self.chunk = 1024
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.name = name or str(id(self))

    async def send_audio(self, websocket, stream):
        try:
            count = 0
            chunk_duration = self.chunk / self.rate  # seconds per chunk
            while True:
                data = stream.read(self.chunk, exception_on_overflow=False)
                await websocket.send(data)
                count += 1
                if count % 100 == 0:
                    print(f"[{self.name}] Sent {count} audio chunks")
                await asyncio.sleep(chunk_duration)  # maintain real-time pace
        except Exception as e:
            print(f"[{self.name}] ERROR sending audio: {e}")
            sys.exit(1)

    async def receive_audio(self, websocket, stream):
        try:
            count = 0
            async for data in websocket:
                stream.write(data, exception_on_underflow=False)
                count += 1
                if count % 100 == 0:
                    print(f"[{self.name}] Played {count} audio chunks")
        except Exception as e:
            print(f"[{self.name}] ERROR receiving audio: {e}")
            sys.exit(1)

    async def run(self):
        uri = f"ws://192.168.1.45:8766"
        async with websockets.connect(uri, ping_interval=10, ping_timeout=None) as websocket:
            print(f"[{self.name}] Connected to server")
            p = pyaudio.PyAudio()
            try:
                input_stream = p.open(
                    format=self.audio_format,
                    channels=self.channels,
                    rate=self.rate,
                    input=True,
                    frames_per_buffer=self.chunk,
                )
                output_stream = p.open(
                    format=self.audio_format,
                    channels=self.channels,
                    rate=self.rate,
                    output=True,
                    frames_per_buffer=self.chunk,
                )
            except Exception as e:
                print(f"[{self.name}] ERROR opening PyAudio stream: {e}")
                sys.exit(1)

            try:
                await asyncio.gather(
                    self.send_audio(websocket, input_stream),
                    self.receive_audio(websocket, output_stream),
                )
            except Exception as e:
                print(f"[{self.name}] ERROR in main gather: {e}")
                sys.exit(1)
            finally:
                input_stream.stop_stream()
                input_stream.close()
                output_stream.stop_stream()
                output_stream.close()
                p.terminate()
            print(f"[{self.name}] Connection closed.")

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else None
    client = AudioClient(name)
    asyncio.run(client.run())
