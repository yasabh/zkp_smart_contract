#!/bin/sh

# Start Hardhat node and deploy the contract
echo "Starting Hardhat node and deploying the contract..."
npx hardhat node & sleep 5
npx hardhat run deploy.js --network localhost
