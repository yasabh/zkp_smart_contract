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

# Install Hardhat globally
RUN npm install -g snarkjs hardhat @openzeppelin/contracts

# Install Python dependencies
RUN pip3 install pycryptodome web3

# Install Rust then Circom (only needed for the trusted setup)
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y \
    && export PATH="$HOME/.cargo/bin:$PATH" \
    && git clone https://github.com/iden3/circom.git /app/circom \
    && cd /app/circom \
    && cargo build --release \
    && ln -s /app/circom/target/release/circom /usr/bin/circom