---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: BGP Internet Routing Protocol
translated: false
type: note
---

Question: What is BGP (Border Gateway Protocol)?

Answer:

**Border Gateway Protocol (BGP)** is the standardized exterior gateway protocol used to exchange routing and reachability information between autonomous systems (AS) on the Internet.

### Key Points

- **Purpose**: BGP is the protocol that makes the global Internet routing work. It allows different networks (owned by ISPs, companies, universities, etc.), each identified by an Autonomous System Number (ASN), to tell each other which IP address blocks (prefixes) they can be reached through them.
- **Type**: It is a **path-vector protocol** (an advanced form of distance-vector routing). Instead of just using metrics like hop count or bandwidth, BGP routers exchange full paths (lists of ASNs) to reach a destination. This helps detect and prevent routing loops.
- **Versions**:
  - BGP-4 (BGP version 4) has been the current standard since 1994 (RFC 4271).
  - It supports CIDR (Classless Inter-Domain Routing) and IPv6.
- **Operation Modes**:
  - **eBGP (External BGP)**: Used between routers in different autonomous systems (peers from different organizations).
  - **iBGP (Internal BGP)**: Used between routers within the same autonomous system to share external routes internally.
- **How Decisions Are Made**:
  BGP doesn’t automatically choose the “shortest” or “fastest” path like internal protocols (OSPF, EIGRP). Instead, routers evaluate routes using a series of attributes in this typical order:
  1. Highest LOCAL_PREF
  2. Shortest AS_PATH
  3. Lowest origin type
  4. Lowest MED (Multi-Exit Discriminator)
  5. eBGP over iBGP
  6. Lowest IGP metric to next-hop
  … and finally router ID as tie-breaker.
  Administrators can heavily influence routing using policies (route maps, prefix lists, communities, etc.).
- **Scale**:
  The global BGP table (the “full Internet routing table”) currently contains around **950,000–1,000,000 IPv4 prefixes** and **150,000–200,000 IPv6 prefixes** (as of 2025).
- **Security Issues**:
  BGP was designed with no built-in authentication or integrity checks, leading to incidents like route hijacks and leaks. Modern mitigations include:
  - RPKI (Resource Public Key Infrastructure) and ROA (Route Origin Authorization)
  - BGPsec (still limited deployment)
  - MANRS (Mutually Agreed Norms for Routing Security) best practices

In short, BGP is essentially the “glue” that holds the Internet’s routing together, allowing thousands of independent networks to cooperate and direct traffic across the globe.
