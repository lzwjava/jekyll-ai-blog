---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Cryptographic Algorithms in GnuPG
translated: false
type: note
---

### Supported Algorithms in Cryptographic Software (e.g., GnuPG)

This list outlines the algorithms supported by a tool like GnuPG (GPG), which is commonly used for secure email (PGP/MIME), file encryption, and digital signatures. It categorizes them into public-key (asymmetric) cryptography for key exchange and signing, symmetric ciphers for bulk data encryption, hash functions for integrity checks and signatures, and compression methods to reduce data size before encryption. Below, I'll break it down by category with brief explanations of each algorithm's purpose and key traits.

#### Public-Key Algorithms (Pubkey)

These handle asymmetric operations: one key (public) for encryption/signing verification, another (private) for decryption/signing. They're used in key pairs for secure communication.

- **RSA**: Rivest-Shamir-Adleman. A foundational algorithm for both encryption and digital signatures. Widely used due to its security with large key sizes (e.g., 2048+ bits), but computationally intensive.
- **ELG**: ElGamal. Primarily for encryption (not signatures). Based on the discrete logarithm problem; efficient for key exchange but produces larger ciphertexts.
- **DSA**: Digital Signature Algorithm. Designed solely for digital signatures (not encryption). Relies on discrete logs; common in older systems but largely replaced by ECDSA for efficiency.
- **ECDH**: Elliptic Curve Diffie-Hellman. For key agreement/exchange using elliptic curves. Provides strong security with smaller keys than traditional DH, ideal for mobile/constrained devices.
- **ECDSA**: Elliptic Curve Digital Signature Algorithm. An elliptic curve variant of DSA for signatures. Faster and more secure per bit than DSA, with widespread use in modern protocols like TLS.
- **EDDSA**: Edwards-curve Digital Signature Algorithm. A high-speed elliptic curve signing scheme (e.g., Ed25519 variant). Resistant to side-channel attacks; favored in protocols like SSH and Signal for its simplicity and speed.

#### Symmetric Ciphers

These encrypt data with a shared secret key (faster for large files). Block ciphers process data in fixed-size blocks, often with modes like CBC for chaining.

- **IDEA**: International Data Encryption Algorithm. A 64-bit block cipher from the 1990s; once popular but now considered weak due to key size and brute-force risks.
- **3DES**: Triple Data Encryption Standard. Applies DES three times for added security. Legacy algorithm; slow and vulnerable to attacks, phased out in favor of AES.
- **CAST5**: CAST-128. A 64-bit block cipher (CAST family). Balanced speed/security for its era; still used but overshadowed by AES.
- **BLOWFISH**: A 64-bit block cipher with variable key lengths (up to 448 bits). Fast and flexible; good for software but not hardware-accelerated like AES.
- **AES**: Advanced Encryption Standard (128-bit key). NIST-approved block cipher; the gold standard for symmetric encryption—secure, fast, and ubiquitous.
- **AES192**: AES with 192-bit keys. Offers a middle-ground security boost over standard AES.
- **AES256**: AES with 256-bit keys. Highest security variant of AES; recommended for highly sensitive data.
- **TWOFISH**: A 128-bit block cipher (AES finalist). Highly secure with flexible key sizes; performs well in software.
- **CAMELLIA128**: Camellia block cipher (128-bit key). Japanese/European standard; AES-like security and speed.
- **CAMELLIA192**: Camellia with 192-bit keys. Enhanced security tier.
- **CAMELLIA256**: Camellia with 256-bit keys. Top-tier variant, comparable to AES256.

#### Hash Algorithms

These create fixed-size digests from data for verifying integrity, authenticity, or use in signatures/passwords. Collision resistance is key (though SHA1 is now broken).

- **SHA1**: Secure Hash Algorithm 1. Produces 160-bit digests; fast but insecure due to collision vulnerabilities—avoid for new uses.
- **RIPEMD160**: RACE Integrity Primitives Evaluation Message Digest (160-bit). European alternative to SHA1; still reasonably secure but aging.
- **SHA256**: SHA-2 family (256-bit). Robust and widely used; basis for Bitcoin and secure passwords.
- **SHA384**: SHA-2 (384-bit). Longer digest for higher security in sensitive apps.
- **SHA512**: SHA-2 (512-bit). Largest SHA-2 variant; excellent for high-security hashing.
- **SHA224**: SHA-2 (224-bit). A truncated SHA-256 for legacy compatibility.

#### Compression Algorithms

These shrink data before encryption to speed up processing and reduce storage/transmission size. Applied transparently in tools like GPG.

- **Uncompressed**: No compression—data is encrypted as-is. Useful for already-compressed files (e.g., JPEGs) to avoid overhead.
- **ZIP**: DEFLATE algorithm (LZ77 + Huffman coding). Common in file archives; good balance of speed and ratio.
- **ZLIB**: Enhanced DEFLATE with headers/checksums. Similar to ZIP but more flexible for streams.
- **BZIP2**: Burrows-Wheeler transform + Huffman. Slower but achieves better compression ratios than ZIP/ZLIB, especially for text.

This configuration allows flexible, secure workflows—e.g., signing with ECDSA, encrypting with AES256, hashing with SHA256, and compressing with ZLIB. For the latest GnuPG details, check the [official manual](https://www.gnupg.org/documentation/manuals/gnupg/index.html).
