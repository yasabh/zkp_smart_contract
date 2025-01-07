from Crypto.Protocol.SecretSharing import Shamir
from Crypto.Hash import SHA256
from web3 import Web3
import time

# Configuration
THRESHOLD = 3
PARTICIPANTS = [
    "0x1234567890abcdef1234567890abcdef12345678",
    "0xabcdefabcdefabcdefabcdefabcdefabcdef1234",
    "0x567890abcdef567890abcdef567890abcdef5678",
    "0x9876543210abcdef9876543210abcdef98765432",
    "0xabcdef1234567890abcdef1234567890abcdef12"
]
SECRET = "A SECRET MESSAGE"

def wait_for_deployment(file_path, interval=3):
    while True:
        try:
            with open(file_path, "r") as file:
                address = file.read().strip()
                # Check if the address is valid
                if Web3.to_checksum_address(address) == address:
                    return address
        except (FileNotFoundError, ValueError):
            # Handle the case where the address is invalid (not a valid Ethereum address)
            pass
        time.sleep(interval)

# Prepare Web3 connection and contract
w3 = Web3(Web3.HTTPProvider("http://blockchain:8545"))
contract_address = wait_for_deployment("contracts/deployed_address.txt")

# Load contract ABI
contract_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "_participant", "type": "address"},
            {"internalType": "uint256", "name": "_share", "type": "uint256"}
        ],
        "name": "storeShare",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "_participant", "type": "address"}],
        "name": "getShare",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

print(f"Using Contract Address: {contract_address}")
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Hash the secret
hashed_secret = SHA256.new(SECRET.encode("utf-8")).digest()[:16]
print(f"Hashed secret: {hashed_secret.hex()}")

# Generate shares
shares = Shamir.split(THRESHOLD, len(PARTICIPANTS), hashed_secret)
participants = [Web3.to_checksum_address(p) for p in PARTICIPANTS]
address_shares = dict(zip(participants, shares))

# Store shares in the contract
for address, (index, share) in address_shares.items():
    tx = contract.functions.storeShare(address, int.from_bytes(share, "big")).transact({
        "from": w3.eth.accounts[0]
    })
    stored_share = contract.functions.getShare(address).call()
    print(f"Storing Share: {share.hex()} for Participant: {address} {'SUCCESS' if hex(stored_share)[2:] == share.hex() else 'FAILED'}")
    print(f"Transaction hash: {tx.hex()}")

# Reconstruct secret from a subset of shares
selected_shares = list(address_shares.values())[:THRESHOLD]
reconstructed_secret = Shamir.combine(selected_shares)
assert reconstructed_secret == hashed_secret, "Reconstructed secret does not match!"
print(f"Secret '{reconstructed_secret.hex()}' successfully reconstructed and verified!")