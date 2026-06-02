---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Contrarian Networking Opinions Debated
translated: false
type: note
---

Question: What are some unpopular opinions about switching and routing technologies?

Answer:

Here are some genuinely unpopular (or at least contrarian) opinions in the networking community that regularly trigger heated debates on Reddit, Cisco forums, and vendor conferences:

- **Vendor certifications (especially CCIE) are mostly a tax on engineers and don’t correlate with real-world skill anymore.**
  Many self-taught or vendor-agnostic engineers running large networks (cloud providers, hedge funds, hyperscalers) outperform lifelong CCIEs who’ve never touched anything outside IOS/XE.

- **SDN was oversold and largely failed in the enterprise.**
  Outside of very large cloud providers and a few niche telco use-cases, most “SDN” deployments are just centralized management + traditional distributed control planes with a fancy overlay (ACI, NSX, etc.). True OpenFlow-style SDN is effectively dead.

- **EVPN/VXLAN is overcomplicated for 95% of enterprise campuses.**
  A well-designed Layer-3-to-the-access model with OSPF/BGP and good old 802.1Q trunks is simpler, more deterministic, and cheaper than running EVPN everywhere just because “it’s the future.”

- **White-box switching + merchant silicon (Broadcom Tomahawk/Jericho) has won, and traditional vendors are just reselling the same chips with a bloated NOS tax.**
  Cisco, Arista, and Juniper all run on the same Broadcom/Intel/Marvell silicon. The premium you pay for Catalyst/NCS/QFX is mostly brand and support theater.

- **IPv6 adoption is still pathetic after 25+ years because most network engineers secretly don’t want to learn it.**
  NAT + private addressing “just works” and gives a false sense of security. Most IPv6 deployments are half-hearted “dual-stack” that still rely on IPv4 for everything important.

- **TRILL, SPB, and FabricPath were better ideas than VXLAN/EVPN but lost for marketing reasons, not technical ones.**
  They provided true Layer-2 multipathing without the encapsulation tax and controller dependency, yet the industry went all-in on VXLAN because of cloud hype.

- **Multicast is dying and doesn’t deserve the complexity we still throw at it.**
  Outside of IPTV and finance, almost nobody needs PIM anymore. Application-layer multicast (BitTorrent-style) or anycast + unicast replication is good enough.

- **Network automation hasn’t delivered the promised 10x productivity gains because most teams spend more time fighting YAML and Jinja2 than they ever did with CLI.**
  Poor abstractions and constant schema changes (looking at you, Cisco’s ever-shifting YANG models) make “infrastructure as code” a nightmare.

- **Leaf-spine (Clos) topologies are often cargo-culted without understanding the traffic matrix.**
  Many organizations deploy 3:1 oversubscribed leaf-spine fabrics when a simple two-tier design would have been cheaper and performed better for their east-west-light workloads.

- **Hardware routing (ASICs) isn’t magically better than software routing in 2025.**
  Modern x86/ARM servers with DPDK, VPP, or eBPF/XDP can push 100–400 Gbps of routing per box at lower cost than merchant-silicon switches once you factor in licensing and support.

These opinions tend to be unpopular with traditional enterprise engineers, vendor SEs, and certification junkies—but increasingly accepted in cloud-native, web-scale, and low-level Linux networking circles.

References:
- [Reddit r/networking “What’s your networking hill to die on?” threads (multiple years)](https://www.reddit.com/r/networking/search/?q=hill%20to%20die%20on)
- [NANOG mailing list archives on SDN/EVPN debates](https://www.nanog.org/mailing-list/archives/)
- [Ivan Pepelnjak’s blog posts on EVPN complexity](https://blog.ipspace.net/tag/evpn/)
- [DPDK and FD.io performance claims](https://www.fd.io/) / [eBPF/XDP routing benchmarks](https://cilium.io/blog/2023/03/21/ebpf-xdp-performance/)
