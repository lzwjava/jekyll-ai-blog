---
audio: false
generated: true
image: false
lang: en
layout: post
title: Firewall and NAT Differences Explained
translated: false
type: note
---

Question: **What is a firewall used for, and why does it use NAT?**

Answer:

A **firewall** and **NAT** are related in many home routers, but they solve **different problems**.

### 1. What does a firewall do?

A firewall is basically a **packet-flow policy engine**:

```text
Internet
   |
   v
[ Firewall ]
   |
   +---- allow ----> LAN
   |
   +---- drop -----> X
```

For each packet, it can inspect things like:

```text
src IP
dst IP
src port
dst port
protocol
connection state
interface
```

Then apply rules:

```text
ALLOW  LAN -> Internet
ALLOW  established Internet -> LAN
DROP   unsolicited Internet -> LAN
```

For example, your PC:

```text
192.168.1.100:52341
        |
        | TCP
        v
8.8.8.8:443
```

The firewall can say:

> LAN machines are allowed to initiate HTTPS connections.

But if some random Internet host tries:

```text
1.2.3.4:54321 -> 192.168.1.100:22
```

the firewall can drop it.

So the fundamental purpose is:

**Firewall = control which traffic is allowed to cross a network boundary.**

---

### 2. Then why NAT?

NAT = **Network Address Translation**.

Suppose your LAN has:

```text
PC1  192.168.1.100
PC2  192.168.1.101
PC3  192.168.1.102
```

These are private addresses and aren't directly routable across the public Internet.

Your router might have:

```text
WAN: 203.0.113.50
LAN: 192.168.1.1
```

When PC1 sends:

```text
192.168.1.100:50000
       ->
8.8.8.8:443
```

the router translates it:

```text
203.0.113.50:40001
       ->
8.8.8.8:443
```

It maintains a NAT table:

```text
192.168.1.100:50000
        |
        v
203.0.113.50:40001
```

When the response comes back:

```text
8.8.8.8:443
       ->
203.0.113.50:40001
```

the router looks up the mapping and translates it back:

```text
203.0.113.50:40001
       ->
192.168.1.100:50000
```

---

### 3. NAT is NOT the same thing as a firewall

This distinction is important.

**NAT's primary purpose:**

```text
translate addresses/ports
```

**Firewall's primary purpose:**

```text
allow / deny traffic
```

But NAT often creates an additional security effect.

Imagine the router has:

```text
WAN IP = 203.0.113.50
LAN IP = 192.168.1.100
```

An Internet machine cannot simply send:

```text
Internet
   |
   v
192.168.1.100
```

because `192.168.1.100` is a private address and isn't globally routable.

And typical home routers additionally have a firewall rule:

```text
WAN -> LAN
unsolicited connection
        |
        v
       DROP
```

So people sometimes say:

> "NAT protects my network."

More precisely:

**NAT provides address translation; the stateful firewall provides the actual traffic filtering.**

---

### 4. Why do home routers combine them?

Because they're naturally located at the same boundary:

```text
                  Router
             +----------------+
Internet --->| WAN            |
             |                |
             | Firewall       |
             | NAT            |
             | Routing        |
             | DHCP           |
             +-------+--------+
                     |
                     |
                  LAN
              +------+------+
              |             |
             PC1           PC2
```

The router sees **all traffic entering/leaving the LAN**, so it's a convenient place to perform:

1. Routing
2. NAT
3. Stateful firewalling
4. DHCP
5. Sometimes DNS forwarding

---

### 5. The interesting part: NAT creates connection state

For TCP, a home router might effectively track:

```text
LAN:
192.168.1.100:52341

      NAT

WAN:
203.0.113.50:41002

      |
      v

8.8.8.8:443
```

Then the return packet matches this state.

Conceptually:

```text
outbound:
LAN -> WAN
CREATE NAT STATE

return:
WAN -> LAN
MATCH EXISTING STATE -> ALLOW
```

But:

```text
Internet -> WAN
NO EXISTING STATE
        |
        v
      DROP
```

That's why your PC can establish:

```text
PC -> Google
Google -> PC
```

while some random Internet host generally cannot establish:

```text
Random Internet host -> PC
```

without port forwarding / an explicit firewall rule.

So the mental model I'd use is:

```text
NAT:
"Who is this packet really from?"

Firewall:
"Should this packet be allowed?"

Routing:
"Where should this packet go?"
```

I can also walk through **one complete TCP SYN → SYN/ACK → ACK packet sequence through a home router**, showing exactly where routing, NAT, and the stateful firewall act on each packet.
