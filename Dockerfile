# Use a maintained Python base image
FROM python:3.12-slim-bullseye

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . /app

# Install system dependencies including build tools for TgCrypto
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libc6-dev \
        libffi-dev \
        musl-dev \
        ffmpeg \
        aria2 \
        python3-pip \
        python3-dev \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the bot (update script name if needed)
CMD ["python", "main.py"]


