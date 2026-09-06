---
audio: false
generated: true
image: false
lang: en
layout: post
title: IETF Developed IPv6 Standard
translated: false
type: note
---

Question: What is the IETF, and did it create/raise IPv6?

Answer:

**IETF = Internet Engineering Task Force.**

It is an international, open standards organization that develops the **technical standards and protocols that make the Internet work**.

Think of it roughly like:

```text
Internet
   │
   ├── IP        ← addressing/routing
   ├── TCP       ← reliable transport
   ├── UDP       ← lightweight transport
   ├── HTTP      ← web
   ├── DNS       ← domain → IP
   ├── TLS       ← encryption
   └── IPv6      ← newer IP addressing
          ↑
        IETF
```

### Did IETF create IPv6?

**Yes.** More precisely, the IETF developed and standardized IPv6 through its standards process.

The important history is:

```text
IPv4
  │
  │  32-bit address
  │  ~4.3 billion addresses
  ↓
Address exhaustion becomes a problem
  │
  ↓
IETF develops IPng
("IP Next Generation")
  │
  ↓
IPv6
  │
  │  128-bit address
  │  2^128 addresses
  ↓
RFC 2460 (1998)
```

IPv6 was originally called **IPng (Internet Protocol Next Generation)** before becoming IPv6.

The fundamental IPv6 specification was published as **RFC 2460 in 1998**, titled *Internet Protocol, Version 6 (IPv6) Specification*.

Today, the specification has been updated/replaced by newer RFCs, notably **RFC 8200**.

### What exactly does "IETF standard" mean?

The IETF doesn't operate like a government that says:

> "Everyone must use IPv6."

Instead, engineers and researchers propose protocols, discuss them publicly, implement them, test them, and eventually publish specifications as **RFCs**.

For example:

```text
Engineer proposes protocol
        ↓
Internet-Draft
        ↓
IETF discussion / review
        ↓
Working Group
        ↓
Consensus
        ↓
RFC
        ↓
Implementations
        ↓
Internet adoption
```

**RFC** means **Request for Comments**. Despite the name, many RFCs are now formal Internet standards or specifications.

Some extremely important Internet technologies came through this process:

* IPv4 / IPv6
* TCP
* UDP
* HTTP
* DNS
* BGP
* TLS
* QUIC
* SMTP
* DHCP

So when you use something like:

```bash
curl https://example.com
```

you're standing on decades of IETF protocols.

### Why did IPv6 happen?

The fundamental problem was **IPv4's 32-bit address space**:

$$
2^{32}=4,294,967,296
$$

That sounds huge, but the Internet grew enormously.

IPv6 uses 128-bit addresses:

$$
2^{128}\approx3.4\times10^{38}
$$

That's an astronomically larger address space.

For example:

```text
IPv4:
192.168.1.100

IPv6:
2001:db8:1234:5678:abcd:ef01:2345:6789
```

So yes: **IETF is one of the core organizations behind the technical architecture of the Internet, and IPv6 is an IETF-developed Internet protocol.**

I can also walk you through **how an IPv6 packet actually travels from your machine → router → ISP → destination**, including the IPv6 header and routing, which makes the IETF's role much clearer.
