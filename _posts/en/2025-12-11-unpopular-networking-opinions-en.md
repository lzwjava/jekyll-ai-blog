---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Unpopular Networking Technology Opinions
translated: false
type: note
---

Question: What are some unpopular opinions about networking technology, TCP/IP, DDNS, and the current global network infrastructure?

Answer:

Unpopular opinions in networking often challenge the status quo of established protocols and infrastructures, highlighting inefficiencies, outdated designs, or overhyped alternatives. Based on discussions from tech communities, experts, and engineers, here are some notable ones focused on TCP/IP, DDNS (Dynamic DNS), and broader global network infra. I've grouped them thematically for clarity.

### On TCP/IP and Its Core Design

- **TCP/IP is fundamentally flawed for modern, content-driven applications and should be replaced by something like NDN (Named Data Networking).**
  Traditional TCP/IP routes packets based on host addresses, leading to inefficiencies like redundant data fetches and vulnerability to outages (e.g., when a popular site crashes globally). NDN, by contrast, focuses on named content, enabling better caching, security, and resilience—ideal for an IoT/AI era where data availability trumps host connectivity. This view argues the 45-year-old stack is a relic holding back innovation.

- **TCP connections are a poor abstraction for RPCs (remote procedure calls) in distributed systems.**
  TCP's reliability features (e.g., retransmissions) don't meaningfully improve service-based apps; they add overhead without aiding fault tolerance in microservices or cloud environments. Modern alternatives like QUIC (from Google) are already supplanting TCP for faster, more reliable app-layer transport, suggesting TCP's days as the default are numbered.

- **The entire TCP/IP stack is inadequate for an AI/robotics-driven future focused on value transfer, not just information.**
  Built for sharing data packets, it can't handle the low-latency, secure value exchanges needed in a world of autonomous machines and tokenized economies. Upgrading global infra on this foundation would be inefficient; we'd need a purpose-built protocol overlay or replacement to avoid bottlenecks.

### On DDNS and DNS Infrastructure

- **DDNS introduces unnecessary complexity and security risks that outweigh its convenience for dynamic environments.**
  While DDNS automates IP updates for DHCP-heavy setups (e.g., in AD-integrated networks), it creates single points of failure—like master-slave dependencies that hackers exploit for phishing or redirects. In static or reservation-based networks, it's often skipped entirely, proving it's not essential for most modern infra. Better to lean on alternatives like SLAAC for IPv6.

- **DNS's decentralized "magic" is overhyped; its eventual consistency and caching layers make it a privacy nightmare and reliability headache.**
  Billions of queries route through recursive resolvers and caches (including sneaky ones in browsers, OSes, ISPs, and CDNs that ignore TTLs), creating a fragile, opaque system prone to hijacks or stale data. Routing everything to a single provider like Cloudflare improves speed but trades privacy—proving the ecosystem has failed users so badly that centralization feels like progress.

### On Current Global Network Infrastructure

- **IPv6's overengineering doomed its adoption; a simpler address extension would have solved scarcity without the mess.**
  Doubling octets with router-based conversion (like 32-bit to 64-bit ASNs) could have enabled seamless IPv4 extension, reducing NAT hacks and dual-stack bloat. Instead, IPv6's radical changes created compatibility hurdles, keeping IPv4 dominant for another decade despite endless exhaustion talks.

- **Push-style networks (e.g., unsolicited inbound traffic) are obsolete and insecure; everything should default to pull-based models.**
  With rising threats, assuming inbound packets are malicious aligns with zero-trust principles. This shifts infra toward request-driven designs, obsoleting legacy protocols and forcing a rethink of global routing like BGP, which is just "glorified advertising" for IPs anyway.

- **Centralized cloud giants (AWS, Azure) are yesterday's tech; decentralized infra like blockchain-backed networks is the inevitable future.**
  Paying premiums for crash-prone, resource-wasting services is like sticking with landlines in a smartphone world. Ethernet's dominance shows simple, scalable standards win, but global infra needs distributed alternatives to handle AI-scale loads without greed-driven bloat.

These views spark debate because they question sacred cows like TCP/IP's universality or DNS's resilience, often citing real-world pain points like slow IPv6 rollout or DNS outages. They're "unpopular" as they imply costly overhauls, but proponents argue sticking with the status quo risks stagnation in an exploding data era.

References:

- [Is TCP/IP ideal in a perfect world? (Reddit)](https://www.reddit.com/r/networking/comments/1atenol/is_tcpip_ideal_in_a_perfect_world/)
- [It's always DNS (Reddit)](https://www.reddit.com/r/networking/comments/1c5gpnl/its_always_dns/)
- [TCP/IP versus NDN (BCS)](https://www.bcs.org/articles-opinion-and-research/tcp-ip-versus-ndn/)
- [What's The Future For TCP/IP (Reddit)](https://www.reddit.com/r/Network/comments/eig5sw/whats_the_future_for_tcpip_a_start_for_discussion/)
- [Dynamic DNS Advantages and Disadvantages (RF Wireless World)](https://www.rfwireless-world.com/terminology/dynamic-dns-advantages-disadvantages)
- [Bridging The Gap: From TCP/IP to NDN (Medium)](https://medium.com/ndn-link-official/bridging-the-gap-from-tcp-ip-to-ndn-bdb4fe4ea91d)
- [Advantages and Disadvantages of Using DNS (TinyDNS)](https://tinydns.org/advantages-and-disadvantages/)
- [Which DNS approach is "best practice"? (Reddit)](https://www.reddit.com/r/sysadmin/comments/1oyvyny/which_dns_approach_is_considered_best_practice/)
- [DNS is the largest eventually consistent system (X Post)](https://x.com/arpit_bhayani/status/1963087598882324658)
- [IPv6 like IPsec is overengineered (X Post)](https://x.com/sdxsdx_/status/1979818454497559037)
- [Hot take: TCP connections ill-suited for RPCs (X Post)](https://x.com/DominikTornow/status/1903461669852021118)
- [TCP/IP not feasible for AI/robotics (X Post)](https://x.com/LordRaspyIII/status/1996376104526131366)
- [Push style networks obsolete (X Post)](https://x.com/nic_carter/status/1929649750200275275)
- [Sending DNS to Cloudflare bad but improvement (X Post)](https://x.com/hdevalence/status/1177020193807011840)
- [No easier alternative to IPv6 (X Post)](https://x.com/noIPv6/status/1563165943693332480)
