---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: AX3000 No Repeater or WDS Mode
translated: false
type: note
---

Question: Does the TP-Link AX3000 (Archer AX3000 series, such as AX55/AX3000 Wi-Fi 6 routers) support functioning as a wireless repeater (Repeater) or wireless bridging (WDS) to extend signals?

Answer:

The TP-Link AX3000 series routers, including models like the Archer AX55 and similar AX3000 Wi-Fi 6 devices, **do not support traditional wireless repeater (Repeater) or WDS bridging modes** for extending Wi-Fi signals wirelessly.

Many users report that the admin page (tplinkwifi.net or 192.168.0.1) lacks options such as "Wireless Repeater," "WDS Bridging," or "Scan for Wi-Fi to bridge." This is intentional: newer Wi-Fi 6 routers in the AX series have phased out legacy WDS functionality in favor of modern mesh solutions like OneMesh or EasyMesh.

### Why the wireless settings page lacks repeater/bridging options

- The **Wireless** section typically only includes basic settings: SSID, password, channel, guest network, etc.
- No "Scan other Wi-Fi networks and relay" button exists.
- Older TP-Link models (e.g., WR series, some Archer C series like C80 or C7) include clear WDS/Repeater options.
- AX series routers are designed primarily as **main routers** or **wired Access Points (AP mode)** — they require an Ethernet cable to the upstream router for extension.

To use the AX3000 for signal extension, a dedicated range extender (e.g., TP-Link RE series) is required.

### Can it be used for double (cascaded) wireless repeating?

- **No**, because it cannot perform even a single wireless relay.
- Even on older WDS-supporting routers, cascading 2–3 times is theoretically possible but performs poorly:
  - Speed halves (or worse) per hop due to shared channel for receive/transmit.
  - Increased latency, unstable signal, frequent drops.
  - Cascading more than twice is rarely successful and not recommended.
- TP-Link recommends OneMesh/EasyMesh-compatible setups for multi-hop extension (though signal still degrades with hops; limit to 2–3 max).

### Recommended solutions

1. **Best option**: Purchase a TP-Link OneMesh or EasyMesh-compatible range extender or mesh node.
   - Examples: RE705X or RE715X (AX3000 Wi-Fi 6 extenders) — support OneMesh, easy pairing, seamless roaming.
   - If your main router supports OneMesh (some AX55/AX series after firmware update), pair directly.
   - For double extension: Main router → Extender 1 → Extender 2 (Mesh allows multi-hop, but expect attenuation).
2. **Strong alternative (wired, most stable)**: Use the AX3000 in **Access Point (AP) mode**.
   - Go to Advanced > Operation Mode > Access Point.
   - Connect via Ethernet cable: Main router LAN port → AX3000 LAN port (not WAN).
   - Multiple APs can chain (main → AP1 → AP2), with no speed loss.
3. **If insisting on wireless**:
   - Use an older TP-Link model that supports WDS (but loses Wi-Fi 6 benefits and speed).
   - Or install third-party firmware like OpenWrt (limited support/risky on AX3000; not recommended for most users).
4. **Troubleshooting your setup**:
   - Verify exact model (e.g., Archer AX55 Vx) and update firmware (Advanced > System Tools > Firmware Upgrade).
   - Main router's wireless page won't show scanning — that's normal (it broadcasts, doesn't scan others).
   - Repeater/bridging settings apply only to the secondary device, but AX3000 lacks this feature.
   - If reset and trying to extend someone else's Wi-Fi, it cannot do so wirelessly.

For a more precise recommendation, provide the exact model (e.g., Archer AX55 V1/V2) and the main router you want to extend (brand/model).

References:

- [TP-Link Community: AX3000/AX55 no WDS option](https://community.tp-link.com/us/home/forum/topic/244588)
- [TP-Link Community: Archer AX55 does not support WDS](https://community.tp-link.com/en/home/forum/topic/623082)
- [TP-Link OneMesh Compatible Devices List](https://www.tp-link.com/onemesh/product-list)
- [TP-Link WDS Bridging FAQ (applies to older models only)](https://www.tp-link.com/us/support/faq/1555)
