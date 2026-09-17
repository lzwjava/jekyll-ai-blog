---
audio: false
generated: true
image: false
lang: en
layout: post
title: Packet-Filter Firewall Pros and Cons
translated: false
type: note
---

Question: **What is a packet-filter firewall, and what are its pros and cons?**

Answer:

A **packet-filter firewall** is the simplest classic type of network firewall. It examines individual network packets and decides **allow / deny** based on fields in the packet header.

Think of it as:

```text
Internet
   |
   v
+-------------------+
| Packet Firewall   |
|                   |
| src IP            |
| dst IP            |
| protocol          |
| src port          |
| dst port          |
| TCP flags         |
+-------------------+
   |
   v
Internal network
```

### 1. What does it actually inspect?

Suppose a TCP packet arrives:

```text
src IP:      1.2.3.4
dst IP:      10.0.0.5
protocol:    TCP
src port:    52341
dst port:    22
flags:       SYN
```

The firewall can have rules like:

```text
ALLOW TCP 10.0.0.0/24 -> 10.0.0.5:22
DENY  TCP ANY          -> 10.0.0.5:22
DENY  TCP 1.2.3.4      -> ANY
ALLOW TCP ANY          -> 10.0.0.5:443
```

The decision is basically:

```python
def filter(packet):
    for rule in rules:
        if rule.matches(packet):
            return rule.action   # ACCEPT / DROP / REJECT

    return DEFAULT_POLICY       # usually DROP
```

So it operates primarily at **OSI Layer 3/4**:

```text
Layer 3: IP
    source IP
    destination IP

Layer 4: TCP/UDP
    protocol
    source port
    destination port
    TCP flags
```

It generally does **not understand the application payload**.

---

## 2. Stateless packet filtering

The simplest version is **stateless**.

Imagine:

```text
Client                         Server
  |                              |
  | -------- SYN ------------->  |
  | <------- SYN/ACK ----------  |
  | -------- ACK ------------->  |
```

A stateless firewall examines each packet independently.

It doesn't inherently know:

> "This SYN/ACK belongs to a TCP connection that I previously allowed."

You therefore need rules describing both directions.

For example:

```text
ALLOW outbound TCP :ANY -> server:443
ALLOW inbound TCP server:443 -> :ANY
```

The second rule can potentially be dangerous if written too broadly.

---

# 3. Stateful firewall

A **stateful firewall** adds a connection table.

For example:

```text
Connection table

src              dst             state
------------------------------------------------
10.0.0.10:52341  8.8.8.8:443     ESTABLISHED
```

Now the firewall can say:

```python
if packet.belongs_to_existing_connection():
    ACCEPT
```

rather than treating every packet independently.

Conceptually:

```text
             packet
               |
               v
       +---------------+
       | conntrack     |
       |               |
       | NEW           |
       | ESTABLISHED   |
       | RELATED       |
       | INVALID       |
       +---------------+
               |
               v
          firewall rules
```

Linux `nftables`/`iptables` commonly uses this model.

---

# 4. Pros of packet filtering

### Very fast

The firewall only needs to inspect headers:

```text
IP + protocol + ports + flags
```

instead of parsing application data.

This makes it suitable for **high-throughput routers and network appliances**.

### Simple

Rules are conceptually easy:

```text
allow TCP :443
deny TCP :22
allow UDP :53
```

There isn't much application-level complexity.

### Low overhead

No need to understand:

```text
HTTP
TLS
JSON
SQL
DNS payloads
etc.
```

So CPU and memory requirements can be relatively low.

### Good basic access control

You can implement policies such as:

```text
Internet -> server:443       ALLOW
Internet -> server:22        DROP
Internet -> server:3306      DROP

LAN -> Internet:443          ALLOW
LAN -> Internet:80           ALLOW
```

This alone blocks a large class of unwanted network access.

---

# 5. Cons

The fundamental weakness is:

> **A packet filter sees the envelope, not the meaning of the message.**

For example:

```text
TCP
dst port = 443
```

tells you that something is going to HTTPS.

It does **not necessarily tell you what the application is doing**.

A packet filter cannot normally distinguish:

```text
GET /index.html
```

from:

```text
GET /malicious-command
```

if both are inside an encrypted HTTPS connection.

---

### 5.1 Cannot easily detect application attacks

Suppose:

```text
Internet
   |
   | TCP 443
   v
Firewall
   |
   v
Web server
```

A packet filter sees:

```text
TCP
dst = 443
```

and says:

```text
ALLOW
```

But the HTTP request could contain:

```text
GET /normal
```

or something like an SQL injection attempt.

Application-aware systems are needed for deeper inspection.

---

### 5.2 Stateless filtering becomes complicated

Imagine allowing:

```text
LAN -> Internet:443
```

The response comes back from:

```text
Internet:443 -> LAN:random-port
```

A stateless firewall needs rules to permit the return traffic correctly.

As the network grows, rules can become messy:

```text
ALLOW ...
ALLOW ...
DENY ...
ALLOW ...
DENY ...
ALLOW ...
```

Stateful firewalls solve much of this using connection tracking.

---

### 5.3 IP/port ≠ application

Port numbers are only conventions.

For example:

```text
TCP 443 -> usually HTTPS
TCP 80  -> usually HTTP
TCP 22  -> usually SSH
```

But nothing fundamental prevents an application from running some other protocol on port 443.

Therefore:

```text
port == application
```

is not a reliable security assumption.

---

### 5.4 Encryption reduces visibility

With modern TLS:

```text
Packet
+----------------------+
| IP/TCP headers       | <- firewall can see
+----------------------+
| encrypted TLS data   | <- cannot normally inspect
+----------------------+
```

The firewall may know:

```text
client IP
server IP
TCP
port 443
packet sizes
timing
```

but not the plaintext HTTP request.

---

# 6. Where packet filtering fits

A useful evolution is:

```text
Packet filter
     |
     v
Stateful firewall
     |
     v
Application firewall
     |
     v
WAF / IDS / IPS / NGFW
```

Roughly:

| Firewall             | Understands                    | Example                         |
| -------------------- | ------------------------------ | ------------------------------- |
| Packet filter        | IP/ports/protocol              | `deny :22`                      |
| Stateful firewall    | Connections                    | `allow ESTABLISHED`             |
| Application firewall | Application protocol           | HTTP rules                      |
| WAF                  | Web requests                   | SQLi/XSS protection             |
| NGFW                 | Multiple layers + applications | application/user-aware policies |

These aren't necessarily mutually exclusive; modern firewalls often combine several mechanisms.

---

## 7. The key mental model

Think of networking as layers:

```text
Application
    ↓
HTTP / DNS / SSH / ...
    ↓
TCP / UDP
    ↓
IP
    ↓
Ethernet
```

A basic packet filter operates around:

```text
        ┌─────────────────┐
        │ IP              │
        │ TCP / UDP       │  ← inspect
        ├─────────────────┤
        │ HTTP / TLS / ...│  ← mostly don't understand
        └─────────────────┘
```

So its strength is precisely its limitation:

> **It is extremely good at making fast decisions from simple packet metadata, but it has little understanding of what the traffic actually means.**

For learning networking/firewalls, I'd implement a tiny packet filter first, then add **conntrack/statefulness**. That progression makes the architecture of Linux `nftables`/`iptables` much easier to understand.
