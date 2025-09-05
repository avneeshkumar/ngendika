import asyncio
import websockets
import pyaudio

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
            while True:
                data = stream.read(self.chunk, exception_on_overflow=False)
                await websocket.send(data)
                count += 1
                if count % 100 == 0:
                    print(f"[{self.name}] Sent {count} audio chunks")
        except Exception as e:
            print(f"[{self.name}] Error sending audio: {e}")
            raise

    async def receive_audio(self, websocket, stream):
        try:
            count = 0
            async for data in websocket:
                stream.write(data, exception_on_underflow=False)
                count += 1
                if count % 100 == 0:
                    print(f"[{self.name}] Played {count} audio chunks")
        except Exception as e:
            print(f"[{self.name}] Error receiving audio: {e}")

    async def run(self):
        uri = f"ws://192.168.1.45:8766"
        async with websockets.connect(uri, ping_interval=10, ping_timeout=None) as websocket:
            print(f"[{self.name}] Connected to server")

            # Initialize PyAudio
            p = pyaudio.PyAudio()

            # Open audio streams
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

            try:
                await asyncio.gather(
                    self.send_audio(websocket, input_stream),
                    self.receive_audio(websocket, output_stream),
                )
            finally:
                input_stream.stop_stream()
                input_stream.close()
                output_stream.stop_stream()
                output_stream.close()
                p.terminate()
            print(f"[{self.name}] Connection closed.")

if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else None
    client = AudioClient(name)
    asyncio.run(client.run())
