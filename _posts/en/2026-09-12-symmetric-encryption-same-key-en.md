---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Symmetric Encryption: Same Key"
translated: false
type: note
---

Question: What does **对称加密** mean?

Answer: **对称加密 = symmetric encryption**.

The core idea is simple:

> **The same secret key is used to encrypt and decrypt the data.**

```text
plaintext
   │
   │  encrypt + secret key
   ▼
ciphertext
   │
   │  decrypt + same secret key
   ▼
plaintext
```

For example:

```python
key = "my-secret-key"

ciphertext = encrypt("hello", key)
plaintext  = decrypt(ciphertext, key)

assert plaintext == "hello"
```

The important property is:

```text
Encrypt(message, K) → ciphertext
Decrypt(ciphertext, K) → message
```

Both sides need to know `K`.

### Why "symmetric"?

Because the cryptographic operation uses the **same shared secret** on both sides:

```text
Alice                         Bob
  │                            │
  │      shared key K          │
  ├────────────────────────────┤
  │                            │
  │ encrypt(msg, K)            │
  │ ─────── ciphertext ───────>│
  │                            │
  │              decrypt(ct, K)│
  │                            │
```

Common symmetric encryption algorithms include **AES** and **ChaCha20**.

The main problem is **key distribution**: how do Alice and Bob securely get the same secret key in the first place? That's one reason asymmetric cryptography (RSA/ECC) exists.

A useful mental model:

```text
对称加密      = one shared secret
非对称加密    = public key + private key
```

If you want, I can next walk through **AES at the byte/block level and show exactly what happens during one encryption round**.
