// File: contracts/SecretSharing.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SecretSharing {
    struct Share {
        uint256 index;
        bytes share;
    }

    mapping(address => Share) public participantShares;

    function storeShare(address participant, uint256 index, bytes memory share) public {
        participantShares[participant] = Share(index, share);
    }

    function getShare(address participant) public view returns (uint256, bytes memory) {
        Share memory s = participantShares[participant];
        return (s.index, s.share);
    }
}
