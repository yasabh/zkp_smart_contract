// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Verifier.sol"; // Import the Verifier contract

contract SecretSharing is Groth16Verifier {
    address public owner;
    uint256 public threshold;
    uint256 public totalShares;

    // Mapping to store shares (directly using address as key)
    mapping(address => uint256) public participants;

    event SecretVerified(address indexed verifier, bool isValid, uint256 timestamp);

    // Access control modifier
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _;
    }

    // Constructor to initialize the contract with the threshold value
    constructor(uint256 _threshold) {
        require(_threshold > 0, "Threshold must be greater than zero");
        owner = msg.sender; // Set the contract deployer as the owner
        threshold = _threshold; // Set the threshold value
    }

    // Function to add a participant and their share (restricted to owner)
    function storeShare(address _participant, uint256 _share) external onlyOwner {
        require(_participant != address(0), "Invalid participant address");
        require(participants[_participant] == 0, "Participant already added");
        require(_share != 0, "Share cannot be zero");
        // require(totalShares <= threshold, "Cannot add more participants than the threshold");

        participants[_participant] = _share;
        totalShares++;
    }

    // Function to verify a ZK proof (restricted to owner)
    function verifySecret(
        uint256[2] calldata a,
        uint256[2][2] calldata b,
        uint256[2] calldata c,
        uint256[1] calldata publicSignals
    ) public onlyOwner returns (bool) {
        bool isValid = verifyProof(a, b, c, publicSignals);

        // Emit event regardless of validity
        emit SecretVerified(msg.sender, isValid, block.timestamp);

        return isValid;
    }

    // Function to retrieve a participant's share
    function getShare(address _participant) external view returns (uint256) {
        uint256 share = participants[_participant];
        require(share != 0, "No share for this participant");
        return share;
    }
}
