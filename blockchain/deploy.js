const fs = require("fs");

async function main() {
    const threshold = 3; // Set your threshold value here
    
    const SecretSharing = await ethers.getContractFactory("SecretSharing");
    const secretSharing = await SecretSharing.deploy(threshold);
    await secretSharing.waitForDeployment();

    const address = await secretSharing.getAddress();
    fs.writeFileSync("./contracts/deployed_address.txt", address);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });