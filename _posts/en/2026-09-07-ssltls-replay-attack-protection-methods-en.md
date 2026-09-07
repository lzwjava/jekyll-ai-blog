---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSL/TLS Replay Attack Protection Methods
translated: false
type: note
---

Question: How does SSL/TLS provide replay attack protection?

Answer:

SSL/TLS protects against replay attacks through several layered mechanisms:

**1. Session Keys & Nonces**
Each TLS handshake generates a fresh session using two random values — a client random and a server random (each 28–32 bytes of cryptographically secure randomness). These are combined to derive unique session keys, so even if an attacker captures an entire session, replaying those exact bytes in a new connection will fail because the keys will differ.

**2. Sequence Numbers**
Every TLS record carries an implicit sequence number (not sent on the wire, but included in the MAC computation). The receiver maintains its own counter and rejects any record that arrives out of order or with a sequence number already seen. This directly neutralizes replay within a session.

**3. MAC (Message Authentication Code)**
Each record is authenticated with a MAC that covers:

- the payload
- the record type and version
- the **sequence number**

Replaying an old record produces a MAC mismatch (because the expected sequence number has moved on), and the connection is torn down.

**4. TLS 1.3 — 0-RTT Replay Considerations**
TLS 1.3's 0-RTT (early data) feature is the one area where replay risk reappears. Because early data is encrypted with a pre-shared key before a fresh handshake completes, a network attacker can replay it. TLS 1.3 mitigates this via:

- **Single-use session tickets** — servers can enforce that a ticket is accepted only once
- **Anti-replay cache** — a server-side bloom filter / cache of seen nonces
- Application-level idempotency requirements for any 0-RTT data

**5. Timestamps (in some implementations)**
Some deployments include a timestamp in the handshake; the server rejects handshakes with timestamps outside an acceptable window, limiting the replay window even further.

**Summary Table**

| Mechanism | Protects Against |
| --- | --- |
| Client/Server Random | Cross-session replay |
| Sequence Numbers | Within-session record replay |
| MAC over sequence number | Tampered or replayed records |
| Session ticket expiry | Stale session resumption replay |
| 0-RTT anti-replay cache | Early data replay (TLS 1.3) |

References:

- [RFC 8446 – TLS 1.3 Specification](https://datatracker.ietf.org/doc/html/rfc8446)
- [RFC 5246 – TLS 1.2 Specification](https://datatracker.ietf.org/doc/html/rfc5246)
- [OWASP – Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
- [Cloudflare – 0-RTT and Replay Attacks](https://blog.cloudflare.com/introducing-0-rtt/)
