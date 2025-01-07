pragma circom 2.1.4;

template ThresholdSecretSharing(n, k) {
    // Inputs: Array of shares (e.g., from participants)
    signal input shares[n];
    // Input: Threshold (minimum number of shares required)
    signal input threshold;
    // Output: The reconstructed secret
    signal output reconstructed;

    // Assert that threshold is less than or equal to the number of shares
    assert(threshold <= n);

    // Temporary variables for Lagrange interpolation
    var numerator;
    var denominator;
    var sum;

    // Initialize sum and reconstructed secret
    sum = 0;

    // Perform Lagrange interpolation to reconstruct the secret
    for (var i = 0; i < k; i++) {
        numerator = 1;
        denominator = 1;
        for (var j = 0; j < k; j++) {
            if (i != j) {
                numerator = numerator * (0 - j);
                denominator = denominator * (i - j);
            }
        }
        sum = sum + shares[i] * (numerator / denominator);
    }

    // Assign the accumulated sum to the reconstructed secret
    reconstructed <== sum;
}

// Example instantiation
component main = ThresholdSecretSharing(5, 3);
