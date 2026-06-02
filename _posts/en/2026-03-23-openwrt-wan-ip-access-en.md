---
audio: false
generated: true
image: false
lang: en
layout: post
title: Accessing OpenWrt via WAN IP Address
translated: false
type: note
---

**Question:** For an OpenWrt router connected to a main home router, can a computer connected to the OpenWrt router access the OpenWrt's WAN IP address to log in to it (e.g., LuCI web interface)? I tried but it didn't work—could this be a firewall issue?

**Answer:**

No, this is usually **not possible by default** in a typical OpenWrt setup, and it's **not primarily a firewall issue** in the most common case.

Here's why it fails and what you can do:

### Typical Home Setup (Most Common Reason It Fails)
- Main router: 192.168.1.1 (or similar)
- OpenWrt WAN port connects to main router LAN → OpenWrt gets private WAN IP (e.g., 192.168.1.50)
- OpenWrt LAN: 192.168.2.1 (or whatever you set; should be different subnet from main router)
- Your computer connects to OpenWrt LAN → gets IP like 192.168.2.100

When your computer tries to reach the OpenWrt **WAN IP** (192.168.1.50):

- The packet goes to the OpenWrt router (because it's the default gateway)
- OpenWrt sees destination = its own WAN IP
- But Linux kernel (and OpenWrt) prefers to answer from the **closest/owning interface** → it answers from the **LAN interface** instead of WAN
- The return packet goes out LAN interface → source IP = 192.168.2.1 (not 192.168.1.50)
- Your computer receives reply from wrong source IP → connection fails or behaves strangely

This is normal Linux routing behavior (not specific to OpenWrt). NAT loopback / hairpinning only helps when accessing **your own public IP from inside** (not private WAN IP).

### Solutions (Pick One)

1. **Recommended & Simplest**
   Just use the **LAN IP** of OpenWrt (e.g., http://192.168.2.1 or http://openwrt.lan).
   There's almost never a good reason to force access via the WAN IP from inside your own network.

2. **If you really want to access via the WAN IP**
   - Create a firewall **traffic rule** to allow input from **LAN** zone to destination port 80/443 (LuCI) on the router itself.
     Network → Firewall → Traffic Rules → Add
     - Name: Allow LuCI from LAN to WAN IP
     - Protocol: TCP
     - Source zone: lan
     - Destination zone: Device (input)
     - Destination port: 80, 443
     - Action: ACCEPT
   - But this alone usually **still fails** due to the routing reply issue above.

   To fix the routing/reply path (advanced):
   - Add SNAT/Masquerade rule for traffic destined to the WAN IP coming from LAN
     (or use policy routing + marks — quite complicated for this purpose)

3. **Change OpenWrt to "dumb AP" mode** (if you don't need separate subnet / NAT)
   - Connect main router LAN → OpenWrt **LAN** port (not WAN)
   - Disable DHCP on OpenWrt
   - Set OpenWrt LAN IP static in same subnet as main router (e.g., 192.168.1.2)
   - Assign WAN interface to LAN firewall zone or remove it
   → Then OpenWrt only has one IP (the LAN one) and you access it normally

4. **Quick firewall test (only if upstream is trusted!)**
   Temporarily set WAN zone **Input** policy to **ACCEPT** (Network → Firewall → Zones → wan → edit → Input: ACCEPT).
   If it suddenly works → firewall was blocking.
   **Warning:** Only do this if the "WAN" is actually your trusted home LAN (not real Internet). Revert afterward.

**Bottom line**
In almost all cases you should simply use the LAN IP of the OpenWrt router from devices connected to it. Trying to reach the WAN IP from its own LAN clients rarely works cleanly without extra configuration, and it's usually unnecessary.

**References:**

- https://forum.openwrt.org/t/solved-routed-ap-from-wan-instead-of-lan/228578
- https://openwrt.org/docs/guide-user/network/openwrt_as_routerdevice
- https://forum.openwrt.org/t/22-03-2-nat-reflection-hairpinning/146458
- https://www.reddit.com/r/openwrt/comments/1gmsr17/how_to_access_my_openwrt_router_from_wan_when_im
