---
audio: false
generated: true
image: false
lang: en
layout: post
title: Retransmission in Networking Security
translated: false
type: note
---

**Question: What does 重传 (retransmission) mean in networking security?**

**Answer:**

In networking, **重传 (chóng chuán)** means **retransmission**: sending the same data packet again because the receiver did not get it correctly or the sender is not sure it arrived.

At the basic networking level:

```
Sender                         Receiver

  Packet #1  ------------------>
             (lost)

  timeout

  Packet #1  ------------------>
             received OK
```

The sender retransmits the packet after detecting a problem.

Common reasons for retransmission:

1. **Packet loss**

   Example:

   ```
   TCP segment #100
          X  (dropped by router)

   Sender waits...
   Sender sends #100 again
   ```

2. **Corrupted data**

   Receiver checks checksum:

   ```
   received packet
        |
        v
   checksum OK? ---- no ----> discard
                              |
                              v
                         sender retransmits
   ```

3. **No acknowledgement (ACK)**

   TCP uses ACKs:

   ```
   Client                         Server

   Data ------------------------>

        <---------------- ACK 100

   ```

   If the ACK never arrives:

   ```
   Data ------------------------>

   (no ACK)

   timeout

   Data ------------------------>
   ```

---

## Security meaning: retransmission attacks

In security, "retransmission" is often discussed with **replay attacks (重放攻击)**.

A replay attack abuses retransmission:

```
Original communication:

User ---- "Transfer $100" ----> Bank


Attacker captures:

"Transfer $100"


Later:

Attacker ---- "Transfer $100" ----> Bank
```

The attacker is not creating new data; they are **replaying old valid data**.

Security protocols prevent this using:

### 1. Nonce (random number)

```
Request:
    nonce = 839201

Response:
    sign(nonce + data)
```

A captured old message with another nonce becomes invalid.

### 2. Sequence numbers

Example TCP:

```
Packet:
sequence = 1000
data = hello
```

Receiver remembers:

```
already received sequence 1000
```

A duplicate packet is ignored.

### 3. Timestamps

```
message timestamp = 10:30:01

current time = 10:40:00

too old -> reject
```

---

So:

* **Networking:** 重传 = send the same packet again because delivery failed.
* **Security:** 重传 can become dangerous when attackers replay old valid messages; this is called a **replay attack (重放攻击)**.

TCP retransmission is normal reliability behavior. Replay attacks are malicious retransmissions.
