# Use NVIDIA's official CUDA image with Python 3.9 support
FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04

# Set shell and noninteractive environment variables
SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL=/bin/bash

# Set the working directory
WORKDIR /

# Update and upgrade the system packages (Worker Template)
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install --yes --no-install-recommends sudo ca-certificates git wget curl bash libgl1 libx11-6 software-properties-common ffmpeg build-essential -y gcc espeak-ng &&\
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Add the deadsnakes PPA and install Python 3.9
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get install python3.9-dev python3.9-venv python3-pip -y --no-install-recommends && \
    ln -s /usr/bin/python3.9 /usr/bin/python && \
    rm /usr/bin/python3 && \
    ln -s /usr/bin/python3.9 /usr/bin/python3 && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Download and install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# Pull the required Llama model
RUN ollama pull llama3.1:8b


COPY ./runpod_handler/handler.py .
COPY ./runpod_handler/test_input.json .
COPY . .


# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install  --ignore-installed --no-cache-dir -r ./requirements.txt


# Expose Flask port
EXPOSE 8000

# Ensure NVIDIA container runtime is used for GPU access
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Start Ollama service before launching Flask
CMD ollama serve & sleep 5 && python3 -m handler

