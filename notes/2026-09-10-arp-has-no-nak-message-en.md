---
audio: false
generated: true
image: false
lang: en
layout: post
title: ARP Has No NAK Message
translated: false
type: note
---

Question: What does **NAK mean in ARP**?

Answer: Strictly speaking, **ARP also does not have a NAK message**.

ARP is much simpler than TCP. It has only two important packet operations:

```text
ARP Request
ARP Reply
```

For example, host A wants to send to `192.168.1.20`, but doesn't know its MAC address:

```text
Host A                                      Host B
192.168.1.10                               192.168.1.20
AA:AA:AA:AA:AA:AA                          BB:BB:BB:BB:BB:BB

   ARP Request (broadcast)
   "Who has 192.168.1.20?
    Tell 192.168.1.10"
        ------------------------------->

                                          ARP Reply
                                          "192.168.1.20 is
                                           BB:BB:BB:BB:BB:BB"
        <-------------------------------
```

Then A caches:

```text
192.168.1.20 → BB:BB:BB:BB:BB:BB
```

### So where does "NAK" come from?

You may be seeing **NAK in a networking textbook while studying ARP**, but it is probably referring to a **different protocol/mechanism**, not an ARP packet.

**NAK = Negative Acknowledgment**

Conceptually:

```text
ACK = "I received/accepted it."

NAK = "I did not receive/accept it; do something again."
```

ARP doesn't need this because there is no ARP "data transfer" that needs acknowledgment.

If an ARP request gets no reply:

```text
A                                  B

ARP Request ---------------------> X (lost)

        no ARP Reply
        ↓
        timeout
        ↓
        retry ARP Request
```

There isn't:

```text
NAK: "your ARP request failed"
```

The **absence of an ARP Reply** is enough to indicate failure.

### One important distinction

Don't confuse **ARP** with **ARQ**:

* **ARP** = Address Resolution Protocol → IP address → MAC address
* **ARQ** = Automatic Repeat reQuest → retransmission mechanism
* **NAK** is commonly discussed in **ARQ protocols**

For example:

```text
Sender                         Receiver

DATA #1 --------------------->

        <--------------------- ACK #1

DATA #2 ---------------------> X

        <--------------------- NAK #2

DATA #2 --------------------->
```

That's **ARQ**, not ARP.

So if your material literally says **"NAK in ARP"**, send me the screenshot/page—it may be using ARP in a different context or there may be a typo.
