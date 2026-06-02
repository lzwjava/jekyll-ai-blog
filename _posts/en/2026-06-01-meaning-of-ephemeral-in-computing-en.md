---
audio: false
generated: true
image: false
lang: en
layout: post
title: Meaning of Ephemeral in Computing
translated: false
type: note
---

**Question:** What does "ephemeral" mean?

**Answer:**

Temporary / short-lived / existing only briefly, then gone.

In CS contexts you'll see it constantly:

- **Ephemeral storage** — disk that vanishes when the container/VM dies (e.g. Docker's writable layer, EC2 instance store)
- **Ephemeral port** — OS-assigned temporary port for outbound TCP connections (range 49152–65535)
- **Ephemeral environment** — a throwaway deploy spun up per PR, torn down after merge
- **Ephemeral key** — crypto key used once then discarded (Diffie-Hellman ephemeral = DHE/ECDHE in TLS)

Opposite: **persistent** / **durable**.
