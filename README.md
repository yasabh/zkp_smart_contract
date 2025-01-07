# a Smart Contract for ZKP and Threshold Secret Sharing

https://pycryptodome.readthedocs.io/en/latest/src/protocol/ss.html

### 1. Compile the Circuit
```bash
circom threshold_secret.circom --r1cs --wasm --sym
```

### 2. Trusted Setup
```bash
snarkjs powersoftau new bn128 12 pot12_0000.ptau
snarkjs powersoftau contribute pot12_0000.ptau pot12_0001.ptau --name="YASIN"
snarkjs powersoftau prepare phase2 pot12_0001.ptau pot12_final.ptau
```

### 3. Generate Proving and Verification Keys
```bash
snarkjs groth16 setup threshold_secret.r1cs pot12_final.ptau threshold_secret_0000.zkey
snarkjs zkey contribute threshold_secret_0000.zkey threshold_secret_0001.zkey --name="YASIN"
snarkjs zkey export verificationkey threshold_secret_0001.zkey verification_key.json
```

### 3. Proof Generation
1. Save inputs to `input.json`:
   ```bash
   echo '{
    "shares": [10, 20, 30, 40, 50],
    "threshold": 3
    }' > input.json
   ```
2. Generate witness and proof:
   ```bash
   node threshold_secret_js/generate_witness.js threshold_secret_js/threshold_secret.wasm input.json witness.wtns
   snarkjs groth16 prove threshold_secret_0001.zkey witness.wtns proof.json public.json
   ```

### 4. Verify Proof
```bash
snarkjs groth16 verify verification_key.json public.json proof.json
```

### 5. Export Solidity Verifier
```bash
snarkjs zkey export solidityverifier threshold_secret_0001.zkey Verifier.sol
```