---
audio: false
generated: true
image: false
lang: en
layout: post
title: BGP Inter-AS Routing Strategies
translated: false
type: note
---

**Question:** What are the inter-AS (inter-domain) routing strategies a router uses to communicate with routers in another Autonomous System?

**Answer:**

When routing between Autonomous Systems (ASes), the primary protocol is **BGP (Border Gateway Protocol)** — specifically eBGP (external BGP). Below is a diagram of the overall architecture, followed by an explanation of the key strategies.Here are the core strategies in detail:

**1. eBGP (External BGP) — the foundation**
When two routers belong to different ASes, they establish an eBGP peering session over a direct link (or via eBGP multihop). They exchange reachability information in the form of IP prefixes with path attributes. Each eBGP router prepends its own AS number to the `AS_PATH` attribute, creating a loop-detection mechanism and a map of which ASes the route traverses.

**2. Route advertisement and filtering**
Not every learned route is re-advertised. A border router applies *import policies* (on routes received) and *export policies* (on routes sent). Prefix lists, route maps, and ACLs control which prefixes are accepted or denied, preventing route leaks and limiting exposure.

**3. Path attribute manipulation**
BGP's real power is in its path attributes, used to steer traffic:

- `LOCAL_PREF` — set on import inside your AS to prefer one upstream/peer over another (higher = preferred).
- `MED` (Multi-Exit Discriminator) — sent to a neighbor to suggest which entry point into your AS they should prefer (lower = preferred).
- `AS_PATH prepending` — artificially lengthen the AS path to make a route look less attractive to neighbors, useful for traffic engineering.
- `NEXT_HOP` — the IP address traffic should be forwarded toward; critical for IBGP to function correctly (often requires IGP reachability).

**4. Peering relationships and policy**
The commercial relationships between ASes determine what routes are announced to whom:

- **Provider → customer**: the provider announces a full routing table or default; the customer pays for transit.
- **Customer → provider**: the customer announces only its own prefixes (and possibly its own customers').
- **Peer → peer** (settlement-free peering): each party announces only its own routes and customers' routes — neither carries transit traffic for the other.

This "valley-free routing" principle (routes go up to a provider or across to a peer, but not back up again) is enforced purely through export policy, not by the protocol itself.

**5. Communities for traffic engineering**
BGP Communities (standard 32-bit or large communities) are tags attached to routes that carry policy signals across AS boundaries. For example, a customer might tag a route with a community value that tells the upstream provider "do not re-advertise this to peers X and Y," or "set LOCAL_PREF 150 for this prefix."

---

**References:**
- [RFC 4271 — A Border Gateway Protocol 4 (BGP-4)](https://datatracker.ietf.org/doc/html/rfc4271)
- [RFC 1997 — BGP Communities Attribute](https://datatracker.ietf.org/doc/html/rfc1997)
- [Cisco BGP Best Practices](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/26634-bgp-toc.html)
- [RIPE NCC — BGP Routing Policies](https://www.ripe.net/publications/docs/ripe-399)
