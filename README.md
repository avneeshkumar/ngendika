# Ngendika: Audio Streaming with WebSockets

This very simple project named "Ngendika" (a Javanese word meaning "speaking"), demonstrates a real-time audio streaming system using WebSockets. It consists of a server and a client, built with Python. The server receives audio data from the client and plays it in real-time, enabling low-latency audio communication.

## Project Background

Ngendika was created to solve a practical problem. At my campus, I have a Jetson Nano connected to a speaker system. While I can monitor the room using CCTV, the CCTV system lacks a built-in speaker for communication. To address this, I developed this system, allowing me to send instructions to people in the room via the Jetson Nano from anywhere.

## Features

- Real-time audio capture and playback.
- Asynchronous WebSocket communication.
- Configurable audio settings (sample rate, channels, etc.).

## Prerequisites

- Python 3.7+
- `pyaudio` library for audio streaming.
- `websockets` library for WebSocket communication.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/satyaadhiyaksaardy/ngendika.git
   cd ngendika
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have `pyaudio` installed:
   - On Linux:
     ```bash
     sudo apt-get install portaudio19-dev
     pip install pyaudio
     ```
   - On macOS:
     ```bash
     brew install portaudio
     pip install pyaudio
     ```
   - On Windows:
     Download and install the appropriate [PyAudio binary](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

## Usage

### Server

1. Run the server to start listening for incoming connections:
   ```bash
   python server.py
   ```

### Client

1. Run the client:
   ```bash
   python client.py
   ```
2. When prompted, input the server's IP address.
3. Start speaking.

## File Structure

- `server.py`: WebSocket server for receiving and playing audio.
- `client.py`: WebSocket client for capturing and sending audio.

## Configuration

- Audio settings like sample rate, channels, and chunk size can be configured in `AudioClient` and `AudioServer` classes.
- The default WebSocket port is `8765`. You can modify it in `server.py` and `client.py`.

## Troubleshooting

- **Audio latency**: Experiment with `chunk` size and `rate` settings.
- **Connection issues**: Ensure the client and server are on the same network and the correct IP and port are used (I am using cloudflared tunnel to access local network).
- **PyAudio errors**: Make sure `portaudio` is installed correctly for your OS.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to contribute to this project by opening issues or submitting pull requests!
