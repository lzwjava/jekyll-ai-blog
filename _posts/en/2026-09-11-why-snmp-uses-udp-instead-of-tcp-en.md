---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why SNMP Uses UDP Instead of TCP
translated: false
type: note
---

Question: **Why does SNMP use UDP instead of TCP?**

Answer: The core reason is **SNMP is designed for monitoring/control, where simplicity, low overhead, and robustness matter more than reliable byte-stream delivery.**

### 1. SNMP messages are independent

An SNMP request is basically:

```text
Manager                    Agent
   |                         |
   | ---- UDP request -----> |
   | <---- UDP response ---- |
```

Each SNMP message is a complete application-level message.

SNMP doesn't need a continuous stream like HTTP/TCP:

```text
TCP:
[connect] [byte stream................] [close]
```

Instead:

```text
SNMP:
request #1  ---> response #1
request #2  ---> response #2
request #3  ---> response #3
```

UDP fits this **datagram-oriented** model naturally.

### 2. Monitoring must work even when the network is unhealthy

Imagine a network-management system monitoring 10,000 routers.

If SNMP used TCP, every device would potentially require a TCP connection:

```text
Manager
 ├── TCP ── Router A
 ├── TCP ── Router B
 ├── TCP ── Router C
 ...
 └── TCP ── Router 10000
```

That's unnecessary state.

With UDP:

```text
Manager
 ──UDP──> Router A
 ──UDP──> Router B
 ──UDP──> Router C
 ...
```

No connection establishment or persistent connection state is required.

This is particularly useful when the thing you're monitoring is **the network itself**.

### 3. SNMP implements its own timeout/retry

UDP doesn't guarantee delivery.

SNMP deals with this at the application layer:

```text
send request
     |
     v
wait N seconds
     |
     +---- response ---> success
     |
     +---- timeout ----> retry
                       |
                       +--> timeout again
```

For example, conceptually:

```python
for attempt in range(3):
    send_udp(request)

    response = recv(timeout=2)

    if response:
        return response

raise TimeoutError()
```

SNMP doesn't need TCP's:

* connection establishment
* sequence numbers
* retransmission machinery
* congestion-control machinery
* ordered byte stream

because an SNMP operation is already a **discrete request/response transaction**.

### 4. UDP has much less overhead

TCP requires maintaining connection state:

```text
TCP:
SYN
SYN-ACK
ACK
data
...
FIN
```

SNMP can simply do:

```text
UDP:
request
```

This is valuable for small management messages.

A typical SNMP request might be asking:

```text
"What is your CPU utilization?"
```

or:

```text
"What is interface GigabitEthernet0/1's byte counter?"
```

There's little value in establishing a reliable stream for such a tiny transaction.

### 5. SNMP can still detect many failures

SNMP's model is:

```text
UDP
 ↓
SNMP request
 ↓
timeout/retry
 ↓
application decides device unreachable
```

That actually has an important property for network management.

If a router stops responding:

```text
SNMP timeout
      ↓
device may be down
      ↓
generate alert
```

You don't necessarily want TCP to keep trying to maintain a connection while the network is broken.

---

### Why not TCP?

The design tradeoff is roughly:

| Property                     |                       UDP |          TCP |
| ---------------------------- | ------------------------: | -----------: |
| Connection required          |                        No |          Yes |
| Reliable delivery            |                        No |          Yes |
| Ordered stream               |                        No |          Yes |
| Retransmission               | Application can implement |     Built in |
| Overhead                     |                       Low |       Higher |
| Good for independent queries |                   **Yes** | Less natural |
| Good for continuous streams  |                        No |      **Yes** |

So the fundamental design is:

> **SNMP doesn't need a reliable stream; it needs lightweight request/response datagrams.**

One interesting exception: **SNMPv3 can use TCP in some deployments**, and newer SNMP transport mappings can support other transports. But classic SNMP overwhelmingly uses **UDP port 161** for requests and **UDP port 162** for traps/informs.

I can also walk through an actual SNMP packet from Ethernet → IP → UDP → ASN.1/BER → SNMP PDU, which makes the protocol stack much easier to visualize.
