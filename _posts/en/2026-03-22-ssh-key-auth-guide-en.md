---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deep Dive Into SSH Key Authentication
translated: false
type: note
---

## SSH Key Authentication — Deep Dive

### What Is an SSH Key Pair?

When you run `ssh-keygen`, it creates two mathematically linked files:

```
id_ed25519       → Private Key (SECRET, never leave your machine)
id_ed25519.pub   → Public Key (share freely, paste into servers)
```

For **Ed25519** (the modern standard), this is what they actually contain:

**Private key** (`id_ed25519`):

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtz
c2gtZWQyNTUxOQAAACB4G3kR2f8J...  (base64 encoded binary data)
-----END OPENSSH PRIVATE KEY-----
```

Contains: your **private scalar** (a 256-bit secret number) + your **public key** + metadata.

**Public key** (`id_ed25519.pub`):

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMTRoCy6Uo67vc1CJSAAnZQCHftNB5kbq9jf8ZsEsa+o lzwjava@gmail.com
```

Three parts:

| Part | Value | Meaning |
|------|-------|---------|
| `ssh-ed25519` | Key type | Algorithm used |
| `AAAAC3NzaC...` | Public key | 256-bit public point (base64) |
| `lzwjava@gmail.com` | Comment | Your label (optional) |

### The Math Behind Ed25519

Based on the **Curve25519** elliptic curve:

```
Private key = random 256-bit number (k)
Public key  = k × G  (point multiplication on the curve)

G = base point (fixed, everyone agrees on it)

Given k → easy to compute k×G     (one operation)
Given k×G → impossible to find k  (would need to solve ECDLP)
```

This **one-way trapdoor** is why you can freely share the public key.

### The Authentication Handshake (Step by Step)

When your Mac connects to Gitea:

```
Client (Mac)                          Server (Gitea Container)
    |                                        |
    |--- TCP connection to :2222 ----------->|
    |<-- "Hello, I'm an SSH server" ---------|
    |--- "Hello, I'm an SSH client" -------->|
    |                                        |
    |         [ Key Exchange - Diffie-Hellman ]|
    |                                        |
    |--- eph_pub_key_A ------------------>   |
    |<-- eph_pub_key_B -------------------   |
    |                                        |
    |   Both compute: shared_secret = A×B    |
    |   Session encryption key derived       |
    |                                        |
    |         [ User Authentication ]         |
    |                                        |
    |--- "I am 'git', prove my key" ------->|
    |                                        |
    |    Server checks ~/.ssh/authorized_keys|
    |    Finds matching public key           |
    |                                        |
    |<-- challenge = random data + signature |
    |    signed with server's HOST key       |
    |                                        |
    |--- signature(challenge, priv_key) --->|
    |                                        |
    |    Server verifies signature using     |
    |    the public key from authorized_keys |
    |                                        |
    |    sig == expected? → ✅ AUTHENTICATED |
    |                                        |
    |--- "shell access granted" ----------->|
```

### The Signature Step (Where Your Fix Mattered)

This is the critical moment:

```
1. Server generates random bytes: R = [0x4a, 0x1f, 0x8c, ...]

2. Server signs R with its HOST private key (proves it's the real server)
   Server sends: (R, server_signature)

3. Client verifies server's signature (anti-MITM check)

4. Client signs R with its USER private key
   Client sends: client_signature = Sign(R, private_key)

5. Server verifies:
   Verify(client_signature, R, public_key_from_authorized_keys) → true/false
```

**Step 5 is where your setup failed before and succeeded after:**

```
BEFORE (Mac had different key):
  Client signs with: key_B_private
  Server checks against: key_A_public (only key in authorized_keys)
  Verify(key_B_sig, R, key_A_pub) → ❌ MATH DOESN'T CHECK OUT

AFTER (Mac had same key as server):
  Client signs with: key_A_private
  Server checks against: key_A_public (same key in authorized_keys)
  Verify(key_A_sig, R, key_A_pub) → ✅ PERFECT MATCH
```

### What `authorized_keys` Looks Like in Gitea

```bash
# Inside the Gitea container at /data/git/.ssh/authorized_keys:

# gitea public key
command="/usr/local/bin/gitea --config=/data/gitea/conf/app.ini serv key-1",
no-port-forwarding,
no-X11-forwarding,
no-agent-forwarding,
no-pty,
no-user-rc,
restrict
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMTRoCy6Uo67vc1CJSAAnZQCHftNB5kbq9jf8ZsEsa+o user-1
```

Key details:

| Part | Purpose |
|------|---------|
| `command="...gitea serv key-1"` | Forces the connection into Gitea's handler (not a shell) |
| `no-port-forwarding` etc. | Security restrictions — you can only use Git, not tunnel |
| `restrict` | Master switch for all the `no-*` options |
| `ssh-ed25519 AAAA...` | The actual public key to match against |
| `key-1` | Gitea's internal key ID |

### Why SSH Keys Beat Passwords

```
Password auth:
  Client sends password over encrypted channel
  Server hashes it, compares to stored hash
  Problem: password can be brute-forced, phished, reused

Key auth:
  Client NEVER sends the private key
  Client proves it HAS the key by solving a mathematical challenge
  Even if someone captures the entire session, they learn nothing about the private key
  The private key never leaves your machine (unless you copy it, like you did 😉)
```

### Your Specific Setup

```
┌─────────────────────────────────────────────────────┐
│  Gitea Container (192.168.1.36)                     │
│  ┌─────────────────────────────────────────────┐    │
│  │  /data/git/.ssh/authorized_keys             │    │
│  │  ┌─────────────────────────────────────┐    │    │
│  │  │ ssh-ed25519 AAAA...sa+o user-1      │    │    │
│  │  │  ↑                                  │    │    │
│  │  │  Public key trusted by Gitea        │    │    │
│  │  └─────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────┘    │
│         ▲                      ▲                     │
│         │ matches              │ matches             │
│  ┌──────┴──────┐       ┌──────┴──────┐              │
│  │ Server      │       │ Mac         │              │
│  │ id_ed25519  │       │ id_ed25519  │ (copied)     │
│  │ (private)   │       │ (private)   │              │
│  │ AAAA...sa+o │       │ AAAA...sa+o │              │
│  └─────────────┘       └─────────────┘              │
└─────────────────────────────────────────────────────┘

Both machines have the SAME private key.
Gitea trusts that key.
So both machines can authenticate. ✅
```

The core of your fix: **you made two machines share one identity that Gitea already trusted.** 🦞
