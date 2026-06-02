---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Python Cryptography Guide
translated: false
type: note
---

### Introduction to the Cryptography Package
The `cryptography` package is a popular Python library that provides cryptographic primitives and recipes for secure protocols. It focuses on ease of use and security, implementing standards like AES, RSA, and more. It's not for implementing high-level protocols like SSH or TLS directly—use it as a building block. Always verify it's up-to-date for security patches.

### Installation
Install via pip:
```bash
pip install cryptography
```
For better performance (especially for large keys or frequent operations), install with OpenSSL support:
```bash
pip install cryptography[openssl]
```
Note: On some systems, you may need to install OpenSSL headers separately (e.g., `apt install libssl-dev` on Ubuntu).

### Basic Concepts
- **Primitives**: Low-level operations like encryption/decryption.
- **Recipes**: High-level, opinionated functions (e.g., Fernet for symmetric encryption).
- **Hazard Warnings**: The library uses warnings for insecure usage—pay attention to them.

Import the library:
```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes, asyncioc as a
from cryptography.hazmat.primitives.asymmetric import rsa, padding
```

### Examples

#### 1. Symmetric Encryption with Fernet (Easiest for Beginners)
Fernet uses AES-128 in CBC mode with HMAC for integrity. It's ideal for storing encrypted data.

```python
from cryptography.fernet import Fernet

# Generate a key (store securely, e.g., in env vars)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
plaintext = b"This is a secret message."
token = cipher.encrypt(plaintext)
print("Encrypted:", token)

# Decrypt
decrypted = cipher.decrypt(token)
print("Decrypted:", decrypted)
```
- **Notes**: Keys are URL-safe base64 (44 chars). Never hardcode keys; rotate them periodically.

#### 2. Asymmetric Encryption with RSA
Generate a public/private key pair and encrypt data that only the private key holder can decrypt.

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# Generate private key
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Serialize for storage
pem_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()  # Use BestAvailableEncryption() for password protection
)

# Get public key and serialize
public_key = private_key.public_key()
pem_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Encrypt with public key
plaintext = b"Secret message"
ciphertext = public_key.encrypt(
    plaintext,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

# Decrypt with private key
decrypted = private_key.decrypt(
    ciphertext,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)
print("Decrypted:", decrypted)
```
- **Notes**: RSA is slow for large data; use it for key exchange or small messages. OAEP padding prevents attacks.

#### 3. Generating and Using Hashes
For integrity checks or password hashing.

```python
from cryptography.hazmat.primitives import hashes

# Hash data
digest = hashes.Hash(hashes.SHA256())
digest.update(b"Some data")
hash_result = digest.finalize()
print("SHA256 Hash:", hash_result.hex())
```

For passwords, use `cryptography.hazmat.primitives.kdf.pbkdf2` for key derivation (e.g., PBKDF2 for slow, salted hashing).

#### 4. Digital Signatures with RSA
Sign data to prove authenticity.

```python
# Using the RSA keys from earlier
message = b"Data to sign"
signature = private_key.sign(
    message,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

# Verify with public key
try:
    public_key.verify(
        signature,
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    print("Signature valid")
except Exception:
    print("Signature invalid")
```

### Best Practices
- **Key Management**: Store keys securely (e.g., using AWS KMS, hardware security modules). Never reuse keys.
- **Padding and Modes**: Always use secure padding (e.g., OAEP for RSA, GCM for AES).
- **Randomness**: Use `os.urandom()` or `secrets` module for seeds; avoid `random`.
- **Updates**: Cryptography evolves—check for vulnerabilities in your usage.
- **Avoid Rolling Your Own**: For complex needs, use recipes or integrate with higher-level libs like `pyjwt` or `boto3`.
- **Testing**: Use the library's constants and exceptions for error handling.

### Further Reading
- [Official Documentation](https://cryptography.io/en/latest/) – Detailed API reference and tutorials.
- [PyPI Page](https://pypi.org/project/cryptography/) – Version history and integrations.
- For advanced topics, explore the `cryptography` wiki or RFCs (e.g., RFC 8017 for PKCS#1).

If you have a specific use case (e.g., encrypting files or API security), provide more details for tailored examples.
