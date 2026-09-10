---
audio: false
generated: true
image: false
lang: en
layout: post
title: One-Way Hash Functions in Message Digests
translated: false
type: note
---

Question: What does **单向哈希函数 (one-way hash function)** mean in **报文摘要算法 (message digest algorithms)**?

Answer:

A **one-way hash function** is a function that maps an arbitrary-length message to a **fixed-length digest**:

```text
message M
   │
   ▼
H(M)
   │
   ▼
fixed-size digest
```

For example, SHA-256:

```text
"hello"
   │
   ▼ SHA-256
2cf24dba5fb0a30e26e83b2ac5b9e29e...
   └── 256 bits = 32 bytes
```

### Why "单向"?

Because:

```text
M ──H──> digest
```

is computationally easy, but:

```text
digest ──???──> M
```

is computationally infeasible.

There is **no practical inverse function**:

```python
digest = sha256(message)

# You cannot do:
message = sha256_inverse(digest)
```

You can only try candidate messages:

```python
for candidate in candidates:
    if sha256(candidate) == digest:
        print("found it")
```

That's why password systems store something like:

```text
SHA-256(password)
```

rather than the plaintext password—although for real password storage, **Argon2id/bcrypt/scrypt** should be used instead of raw SHA-256.

### What makes a cryptographic hash useful?

Usually these properties matter:

**1. Deterministic**

```text
H("hello") == H("hello")
```

**2. Fixed output size**

```text
H("a")          -> 256 bits
H("a very long message...") -> 256 bits
```

**3. Preimage resistance**

Given:

```text
y = H(x)
```

finding an `x` such that `H(x) = y` should be infeasible.

**4. Collision resistance**

It should be very difficult to find:

```text
x != y
```

such that:

```text
H(x) == H(y)
```

### Why is it called "报文摘要"?

Think of the digest as a **fingerprint of the message**:

```text
             SHA-256
Message ─────────────────> Digest
                            ↓
                         fingerprint
```

If even one bit changes:

```text
"hello"
   ↓
2cf24dba...

"Hello"
   ↓
185f8db3...
```

the digest changes drastically.

This is why message digests are used in **digital signatures, integrity checking, certificates, Git, TLS, etc.**

One subtle but important point: **"one-way" does not mean mathematically impossible to reverse**. It means that there is no known computationally feasible way to recover a preimage for a properly designed cryptographic hash.