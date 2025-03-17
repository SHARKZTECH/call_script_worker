# Use NVIDIA's official CUDA image with Python 3.9 support
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# Pull the required Llama model
RUN ollama pull llama3.2:1b

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Expose Flask port
EXPOSE 8000

# Ensure NVIDIA container runtime is used for GPU access
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Start Ollama service before launching Flask
CMD ollama serve & sleep 5 && python3 -m api.app
