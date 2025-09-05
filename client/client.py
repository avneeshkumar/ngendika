import asyncio
import websockets
import pyaudio


class AudioClient:
    def __init__(self):
        self.chunk = 1024
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100

    async def run(self):
        uri = f"ws://192.168.1.45:8766"
        async with websockets.connect(uri, ping_interval=10, ping_timeout=None) as websocket:
            print("Streaming audio...")

            # Initialize PyAudio
            p = pyaudio.PyAudio()

            # Open audio stream
            stream = p.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
            )

            try:
                while True:
                    data = stream.read(self.chunk, exception_on_overflow=False)
                    await websocket.send(data)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                # Close the stream and terminate PyAudio
                stream.stop_stream()
                stream.close()
                p.terminate()

        print("Connection closed.")


if __name__ == "__main__":
    client = AudioClient()
    asyncio.run(client.run())
