const fs = require("fs");

async function main() {
    const SecretSharing = await ethers.getContractFactory("SecretSharing");
    const secretSharing = await SecretSharing.deploy();
    await secretSharing.deployed();

    fs.writeFileSync("./contracts/deployed_address.txt", secretSharing.address);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
