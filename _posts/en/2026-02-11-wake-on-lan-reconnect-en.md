---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Wake on LAN After Ethernet Reconnect
translated: false
type: note
---

**Question:** Is it true that after unplugging the computer's Ethernet cable for several hours and plugging it back in, you must physically power on the computer first so the switch can learn its MAC address, otherwise Wake-on-LAN won't work?

**Answer:**

Yes, your observation is **generally correct** in many common home/SOHO or small office network setups — especially when the computer stays off (or in a very deep sleep) and the link was completely down for a long time.

Here's why this happens and when/why it matters:

### How Wake-on-LAN normally works on a local LAN

- The magic packet is almost always sent to the **broadcast address** (e.g., 255.255.255.255 or the subnet broadcast like 192.168.1.255).
- The destination MAC in the Ethernet frame is **FF:FF:FF:FF:FF:FF** (broadcast).
- A switch treats this as an **unknown unicast** or broadcast frame → it **floods** the packet to **all ports** (in the same VLAN).
- The powered-off computer's NIC (still receiving standby power) sees the packet on the wire, checks if its own MAC appears in the payload 16 times → if yes → wakes the machine.

→ In theory, **the switch does not need to know the target MAC address** in its MAC address table, because the packet is flooded anyway.

### Why it still fails in your described scenario

The real issue is usually **not** the switch's MAC table for the broadcast magic packet itself, but one of these common related problems:

1. **Link goes fully down → some switches immediately remove the MAC entry**
   - When you unplug the cable (or the computer is fully powered off and the NIC stops asserting link), the switch port goes down.
   - Many switches (especially Cisco, Juniper, some consumer models) **immediately flush** MAC addresses associated with a down port (instead of waiting for the normal aging timer of 300–3600 seconds).
   - But again — for broadcast this shouldn't matter.

2. **The bigger real-world problem: many WoL tools / apps send unicast by default (directed to the MAC)**
   - Your python script output shows it's sending to 255.255.255.255:9 → this is correct (broadcast).
   - But many other implementations (routers' built-in WoL, phone apps, Home Assistant, etc.) try to send a **unicast** magic packet to the last-known MAC address.
   - If the switch no longer has the MAC in its table → it treats the frame as **unknown unicast** → still floods it → should still work.
   - But some managed switches have features like **port security**, **sticky MAC**, **unknown unicast suppression**, **energy-efficient Ethernet quirks**, or aggressive aging that interfere.

3. **Link negotiation / PHY power-down after long unplug**
   - After hours of being unplugged, when you plug the cable back in:
     - The NIC + switch port must renegotiate link speed/duplex.
     - On some NICs (especially older Realtek, some Intel), the WoL listening mode only fully activates after link is established **and** the driver/firmware has "seen" some traffic or after an initial boot.
     - Some consumer routers/switches temporarily block or rate-limit unknown sources until they see traffic from that port.

4. **ARP table on the sending device / router (if crossing subnets)**
   - But since you're using broadcast (255.255.255.255), this usually isn't the issue on the same LAN.

### Summary – when you really need a boot first

You usually have to power on the PC once after a long unplug/replug when:

- Your WoL sender is sending **unicast** instead of broadcast (very common)
- The switch/router has aggressive port-flush or security features
- The NIC only properly enables WoL listening after seeing some outgoing traffic or after OS boot once
- There is a quirky switch/router model that doesn't flood properly until it sees source traffic from the port

In pure theory with a correct broadcast magic packet → **no**, you shouldn't need to boot the PC first.

In real life (your case) → **yes**, many people experience exactly what you describe, and powering on once "refreshes" the link, lets the switch learn the MAC from outgoing frames, and often "stabilizes" the NIC's WoL state.

### Quick workarounds

- Always send to broadcast (255.255.255.255 or subnet broadcast) — your script already does this → good.
- After plugging cable back in, try sending 3–5 magic packets with 1–2 seconds delay between them.
- On managed switches: increase MAC aging time or disable port-fast-flush behaviors if possible.
- Some people use a scheduled script to ping/broadcast something to "wake" the port periodically.

**References:**

- [https://networkengineering.stackexchange.com/questions/35346/what-happens-with-mac-table-in-switch-when-i-disconnect-some-device](https://networkengineering.stackexchange.com/questions/35346/what-happens-with-mac-table-in-switch-when-i-disconnect-some-device)
- [https://superuser.com/questions/792027/is-wake-on-lan-supposed-to-work-even-after-ac-power-reset](https://superuser.com/questions/792027/is-wake-on-lan-supposed-to-work-even-after-ac-power-reset)
- [https://en.wikipedia.org/wiki/Wake-on-LAN](https://en.wikipedia.org/wiki/Wake-on-LAN)
