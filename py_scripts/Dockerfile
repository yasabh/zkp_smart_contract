# Start with a lightweight Python image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        curl \
        git \
        python3-pip \
        nodejs \
        npm \
        build-essential \
        g++ \
        make \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install ZoKrates
RUN curl -LSfs get.zokrat.es | sh && \
    export PATH=$PATH:/root/.zokrates/bin

# Install Hardhat globally
RUN npm install -g hardhat @openzeppelin/contracts

# Install Python dependencies
RUN pip3 install pycryptodome web3
