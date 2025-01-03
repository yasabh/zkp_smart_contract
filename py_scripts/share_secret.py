from Crypto.Protocol.SecretSharing import Shamir
from Crypto.Hash import SHA256
from web3 import Web3

THRESHOLD = 3
participants = [
    "0x1234567890abcdef1234567890abcdef12345678",
    "0xabcdefabcdefabcdefabcdefabcdefabcdef1234",
    "0x567890abcdef567890abcdef567890abcdef5678",
    "0x9876543210abcdef9876543210abcdef98765432",
    "0xabcdef1234567890abcdef1234567890abcdef12"
]
contract_address = "0xYourContractAddress"
secret_string = "This is a secret message"
hashed_secret = SHA256.new(secret_string.encode('utf-8')).digest()[:16]
print(hashed_secret)

# Contract ABI
contract_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "participant", "type": "address"},
            {"internalType": "uint256", "name": "index", "type": "uint256"},
            {"internalType": "bytes", "name": "share", "type": "bytes"}
        ],
        "name": "storeShare",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Connect to Hardhat network
w3 = Web3(Web3.HTTPProvider("http://hardhat:8545"))
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Split the secret into shares
shares = Shamir.split(THRESHOLD, len(participants), hashed_secret)

# Map shares to participant addresses
address_shares = dict(zip(participants, shares))

# Display shares assigned to participants and send them to the contract
print("Sending shares to the smart contract:")
for address, (idx, share) in address_shares.items():
    print(f"Participant {address} -> Share Index: {idx}, Share: {share.hex()}")
    
    # Send share to the smart contract
    tx = contract.functions.storeShare(address, idx, share).transact({"from": w3.eth.accounts[0]})
    print(f"Transaction hash for {address}: {tx.hex()}")

# Simulate reconstruction using 3 participants
selected_shares = list(address_shares.values())[:THRESHOLD]
reconstructed_secret = Shamir.combine(selected_shares)
assert reconstructed_secret == hashed_secret

print("Secret successfully reconstructed and verified!")
