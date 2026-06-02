---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Home Router IP Conflict Guide
translated: false
type: note
---

Question: What if there's an IP conflict, no response, and I can only connect to one router, where that router is connected to an access point router in the home?

Answer:

If you're experiencing **IP address conflicts** (common error: "IP address conflict" on Windows, or devices can't get online, slow/no internet, can't reach the router admin page) in a home setup where one router is acting as an **Access Point (AP)** connected to the main router, here's what usually happens and how to fix it step by step.

### Most Common Cause in Your Setup

You have:

- **Main Router** (e.g. connected to modem, handles DHCP, gives out IPs like 192.168.0.x or 192.168.1.x)
- **Second Router** (your TP-Link XDR3050 or AX3000) set as **Access Point mode** (or mistakenly left in Router mode)

**Problem scenarios**:

1. The second router is **still in Router mode** (not changed to AP mode) → It runs its own DHCP server → It hands out the same IP range as the main router → IP conflict (two devices fight over who gives 192.168.0.100, for example).
2. Both routers have the **same LAN IP** (e.g. both set to 192.168.0.1) → Direct IP conflict on the management address.
3. After setting AP mode incorrectly (e.g. WAN port used instead of LAN, or DHCP not disabled), it still tries to act as a router.
4. In Mesh/EasyMesh setup, one node got misconfigured or firmware glitch caused overlapping DHCP.

**Symptoms you see**:

- Can connect Wi-Fi to one router but not the other.
- "No internet" or "IP conflict" message.
- Can't open router admin page (tplinkwifi.net or 192.168.0.1 times out or conflicts).
- Some devices work, others don't (depends on which router's DHCP they got IP from).

### Step-by-Step Fix (Start from Simplest)

1. **Physically disconnect the second router** (unplug its power and Ethernet cable from the main router)
   → This stops the conflicting DHCP immediately.
   → Now only the main router is running → Most devices should get internet back quickly.

2. **Connect a computer directly to the main router** (Wi-Fi or Ethernet)
   → Make sure you have internet and can open its admin page (usually 192.168.0.1 or tplinkwifi.net).

3. **Factory reset the second router** (the one you want to use as AP)
   - Press RESET hole 10+ seconds while powered on → lights flash/reboot.
   - This clears any bad settings.

4. **Set the second router to Access Point mode correctly** (critical step to avoid IP conflict forever)
   **Method A: Via web (recommended)**
   - Temporarily connect computer to the second router only (Wi-Fi or Ethernet to one of its LAN ports).
   - Open browser → <http://tplinkwifi.net> or 192.168.0.1 (default after reset).
   - Log in (admin/admin or set new password).
   - Go to **Advanced > Operation Mode** (or System > Operation Mode).
   - Choose **Access Point** mode → Save → It will reboot.
   - **Important**: After reboot, its IP usually changes to something like 192.168.0.2 (auto-assigned by main router).
   - Check the sticker or app to find new IP, or look in main router's "Connected Devices" list.

   **Method B: Use TP-Link app** (if web is hard)
   - TP-Link Wi-Fi app → Add device → Choose AP mode during setup.

5. **Re-connect the second router properly**
   - Use **Ethernet cable**: Main router **LAN port** → Second router **LAN port** (NOT WAN port!).
   - Power on second router.
   - It should now get IP from main router (no longer runs DHCP).
   - Wi-Fi name/password can be same as main (for seamless roaming) or different.

6. **Verify no conflict**
   - On a computer/phone: Open cmd (Windows) or terminal → type `ipconfig` (Windows) or `ifconfig`/`ip addr` (others).
   - Default gateway should be only the main router's IP (e.g. 192.168.0.1).
   - Try pinging both routers' IPs → both should respond.
   - Open both admin pages → should work without conflict.

### If Still No Response / Can't Connect After Reset

- **Try different Ethernet ports** on main router.
- **Change main router's LAN IP range** temporarily (e.g. from 192.168.0.1 to 192.168.1.1) → helps if second router was stuck on old IP.
- **Use static IP on your computer** to reach second router after reset:
  IP: 192.168.0.100
  Subnet: 255.255.255.0
  Gateway: 192.168.0.1
  → Then access <http://192.168.0.1> to set AP mode.
- **Firmware bug**: Update both routers to latest firmware from TP-Link China site (especially for XDR3050 EasyMesh version).

### Quick Prevention Tips

- Always set second router to **AP mode** before connecting cable.
- Never use WAN port on the AP router.
- In EasyMesh: if you want Mesh instead of classic AP, use one-touch EasyMesh pairing (but AP mode is simpler and zero conflict risk).

Follow these steps in order — 90% of IP conflict + no response issues in home AP setups are fixed by step 4 + correct cable connection. If still stuck, tell me: which exact models are main and AP router, and what IP your device gets now (from ipconfig).

References:

- [https://www.tp-link.com.cn/support/faq/1384/](https://www.tp-link.com.cn/support/faq/1384/) (Chinese FAQ on AP mode setup)
- [https://www.tp-link.com/support/faq/1384/](https://www.tp-link.com/support/faq/1384/) (English equivalent for Archer series, similar process)
