#!/bin/sh

# Empty the file
echo -n > contracts/deployed_address.txt

# Wait for the Hardhat node to be ready, then deploy the contract
while ! nc -vz 0.0.0.0 8545; do sleep 1; done && echo "Deploying the contract..." && npx hardhat run deploy.js --network localhost &

# Start Hardhat node
echo "Starting Hardhat node..."
npx hardhat node