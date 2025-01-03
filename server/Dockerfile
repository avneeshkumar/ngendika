# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install required system packages for PyAudio
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    && apt-get clean

# Copy the requirements (if any) and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY server.py .

# Expose the necessary port
EXPOSE 8101

# Command to run the server
CMD ["python", "audio_server.py"]
