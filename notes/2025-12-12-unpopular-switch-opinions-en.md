---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Unpopular Network Switch Opinions
translated: false
type: note
---

Question: What are some unpopular or controversial opinions about network switches that most network engineers disagree with?

Answer:

Here are some genuinely unpopular (and often heatedly debated) opinions about switches in networking that regularly trigger arguments on Reddit’s r/networking, NANOG mailing list, or LinkedIn:

- **Vendor-agnostic “white-box” switches with merchant silicon (Broadcom Tomahawk/Jericho) + open NOS (Cumulus, SONiC, FRR) are already superior to Cisco/Juniper/Arista in 95 % of real-world enterprise and datacenter deployments.**
  Most engineers still believe you “get what you pay for” with big-vendor support contracts and won’t trust a $5k Dell/Broadcom box running Linux to carry production traffic.

- **Buffer bloat on modern switches is massively over-buffered switches (12–36 MB shared buffer) actually makes networks worse for latency-sensitive traffic.**
  The conventional wisdom is “more buffer = better,” but many low-latency advocates (Cerberus, Facebook, Cloudflare engineers) argue deep buffers just hide congestion and hurt VoIP, trading, gaming, etc.

- **802.1X and MACsec are mostly security theater in wired enterprise networks and add more risk than they mitigate.**
  Unpopular because almost every consultant sells 802.1X as mandatory, yet plenty of large networks run perfectly fine (and with fewer helpdesk calls) using simple port-security + DHCP snooping only.

- **Managed Layer-3 switches in the access layer are a terrible idea; keep access switches Layer-2 only.**
  This is the complete opposite of the current “route closer to the host” religion pushed by Cisco and Juniper. Some old-school engineers still swear distributed routing on access switches causes more meltdowns than it solves.

- **10GBASE-T is still a bad choice in 2025; always use DAC or fiber instead.**
  Despite being “easier,” the power draw, heat, latency, and distance limitations of BASE-T make it inferior in almost every rack, yet most enterprises keep buying it because “RJ45 feels safer.”

- **Trunking multiple VLANs to desktops (“voice VLAN” + data VLAN) is obsolete and harmful; everyone should be on a single VLAN with MAB/802.1X profiling.**
  This one gets massive pushback from anyone who lived through the 2000s and still thinks separating voice traffic is sacred.

- **EVPN/VXLAN is overkill for 98 % of enterprise networks; good old L2 with MSTP or SPB is simpler and more reliable.**
  The industry is currently in an EVPN hype bubble, so saying this in 2025 is borderline heresy.

- **Arista is no longer the golden child; their quality and support have declined since the 2020–2023 supply-chain mess and they’re now “Cisco with better CLI.”**
  Saying anything negative about Arista still gets you downvoted to oblivion in most forums.

- **Smart/managed switches for home or small office are a scam; use dumb switches + a proper firewall/router.**
  Extremely unpopular with the consumer “Ubiquiti porn” crowd who love their pretty web GUIs and VLAN tabs they never actually use.

These opinions tend to be held quietly by very experienced engineers who have been burned multiple times by following the mainstream trend of the moment.
