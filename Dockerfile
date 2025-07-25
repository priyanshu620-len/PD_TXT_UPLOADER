# Use a maintained Python base image
FROM python:3.12-slim-bullseye

# Set working directory
WORKDIR /app

# Copy all files from your repo into the container
COPY . /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
        musl-dev \
        ffmpeg \
        aria2 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the bot (replace with your actual start script if needed)
CMD ["python", "main.py"]

