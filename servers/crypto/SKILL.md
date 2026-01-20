---
name: crypto
description: Cryptographic operations using cryptography library (symmetric/asymmetric encryption, signing, hashing).
allowed-tools:
  - generate_symmetric_key
  - encrypt_symmetric
  - decrypt_symmetric
  - generate_key_pair
  - encrypt_asymmetric
  - decrypt_asymmetric
  - sign_data
  - verify_signature
  - hash_data
---

# Crypto Skill

This skill enables the agent to perform cryptographic operations.

## Tools

### generate_symmetric_key
Generate a random symmetric key for AES encryption.

- `key_size`: Key size in bits (128, 192, 256). Default 256.
- `output_file`: Optional file path to save the key (binary).

### encrypt_symmetric
Encrypt data with AES (CBC mode) using a symmetric key.

- `plaintext`: The plaintext string.
- `key`: The symmetric key as a hex‑encoded string or file path.
- `output_file`: Optional file to write the ciphertext (binary).

### decrypt_symmetric
Decrypt data encrypted with AES.

- `ciphertext`: The ciphertext as a hex‑encoded string or file path.
- `key`: The symmetric key as a hex‑encoded string or file path.

### generate_key_pair
Generate an RSA public/private key pair.

- `key_size`: Key size in bits (2048, 3072, 4096). Default 2048.
- `output_public`: Optional file to save the public key (PEM).
- `output_private`: Optional file to save the private key (PEM).

### encrypt_asymmetric
Encrypt data with RSA public key.

- `plaintext`: The plaintext string.
- `public_key`: Public key as PEM string or file path.
- `output_file`: Optional file to write the ciphertext (binary).

### decrypt_asymmetric
Decrypt data with RSA private key.

- `ciphertext`: Ciphertext as hex‑encoded string or file path.
- `private_key`: Private key as PEM string or file path.

### sign_data
Sign a message with a private key (RSA).

- `message`: The message string.
- `private_key`: Private key as PEM string or file path.
- `output_file`: Optional file to write the signature (binary).

### verify_signature
Verify a signature with a public key.

- `message`: The original message string.
- `signature`: The signature as hex‑encoded string or file path.
- `public_key`: Public key as PEM string or file path.

### hash_data
Compute a cryptographic hash (SHA‑256) of data.

- `data`: Input string.
- `output_file`: Optional file to write the hash (hex).

## Dependencies

- cryptography (must be installed via pip)
