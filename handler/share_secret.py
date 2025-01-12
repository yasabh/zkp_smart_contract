from Crypto.Protocol.SecretSharing import Shamir
from Crypto.Hash import SHA256
from web3 import Web3
import subprocess
import time
import json

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
    },
    {
        "inputs": [
            {"internalType": "uint256[2]", "name": "a", "type": "uint256[2]"},
            {"internalType": "uint256[2][2]", "name": "b", "type": "uint256[2][2]"},
            {"internalType": "uint256[2]", "name": "c", "type": "uint256[2]"},
            {"internalType": "uint256[1]", "name": "publicSignals", "type": "uint256[1]"}
        ],
        "name": "verifySecret",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "onlyOwner",
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
assert reconstructed_secret == hashed_secret, "Self-reconstructed secret does not match!"
print(f"Secret '{reconstructed_secret.hex()}' successfully self-reconstructed and verified!")

# Generate Proof and Public Signals using snarkjs (off-chain)
input_data = {
    "shares": [int(share[1].hex(), 16) for share in shares],
    "threshold": THRESHOLD
}
# Save to input.json
with open("contracts/input.json", "w") as f:
    json.dump(input_data, f)

# Generate the witness and the proof
try:
    subprocess.run(['node', 'contracts/threshold_secret_js/generate_witness.js', 'contracts/threshold_secret_js/threshold_secret.wasm', 'contracts/input.json', 'contracts/witness.wtns'], check=True)
    subprocess.run(['snarkjs', 'groth16', 'prove', 'contracts/threshold_secret_0001.zkey', 'contracts/witness.wtns', 'contracts/proof.json', 'contracts/public.json'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error generating witness and/or the proof: {e}")
    exit(1)

# Load the generated proof and public signals (from snarkjs or any other tool)
with open('contracts/proof.json', 'r') as f:
    proof = json.load(f)

with open('contracts/public.json', 'r') as f:
    public_signals = json.load(f)

# Extract proof components from the generated proof file
a = [int(x) for x in proof['pi_a'][:2]]  # First two values of pi_a
b = [[int(x) for x in pair] for pair in proof['pi_b'][:2]]  # First two arrays of pi_b
c = [int(x) for x in proof['pi_c'][:2]]  # First two values of pi_c
public_signals = [int(public_signals[0])]  # Convert public signals to uint256[1]

# print(a,b,c, public_signals)

# Call the verifySecret function on the contract
is_valid = contract.functions.verifySecret(a, b, c, public_signals).call()

# if is_valid:
#     print("The proof is valid!")
# else:
#     print("The proof is invalid.")