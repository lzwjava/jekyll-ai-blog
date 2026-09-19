---
audio: false
generated: true
image: false
lang: en
layout: post
title: Static IP Assignment on Home Router
translated: false
type: note
---

Here's a clear diagram of how static IP assignment works on a home router with a switch:---

**Question:** How do I make IP addresses static and stable on a home router that has a switch and Wi-Fi?

**Answer:**

There are two main methods. **Method A (recommended)** is done on the router; **Method B** is done on each device.

---

**Method A — DHCP Reservation (best choice)**

The router keeps assigning IPs automatically, but it always gives the *same* IP to the same device, identified by its MAC address. The device never needs to be reconfigured.

Steps (works on most routers — TP-Link, ASUS, Netgear, etc.):

1. Open your router admin panel — typically `http://192.168.1.1` or `http://192.168.0.1` in a browser.
2. Log in (check the sticker on the bottom of your router for credentials).
3. Go to **DHCP Settings** → look for "Address Reservation", "Static DHCP", or "DHCP Binding".
4. Find the device in the connected client list and note its **MAC address**.
5. Add a reservation: bind that MAC address to a fixed IP like `192.168.1.10`.
6. Repeat for each device (PC, printer, NAS, etc.).
7. Reboot the device so it picks up the reserved IP.

> Your switch doesn't need any configuration — it just passes traffic through. The switch has no role in IP assignment.

---

**Method B — Static IP on the Device**

You configure the IP directly in Windows, macOS, Linux, or Android/iOS settings. Use this only if you can't access the router admin panel.

When doing this, make sure to set:

| Field | Example value |
|---|---|
| IP address | `192.168.1.10` |
| Subnet mask | `255.255.255.0` |
| Default gateway | `192.168.1.1` (your router) |
| DNS | `8.8.8.8` or your router IP |

**Important:** Choose an IP *outside* the router's DHCP pool range (e.g., if DHCP assigns `.100`–`.200`, use `.10`–`.50`) to avoid conflicts.

---

**Which method to choose:**

- **DHCP Reservation** — centralized, nothing to set on each device, easiest to manage. ✅ Recommended.
- **Device static IP** — works without router access, but each device needs manual config and risks IP conflicts.

**References:**
- [How to set up DHCP reservation — TP-Link](https://www.tp-link.com/us/support/faq/170/)
- [Static IP vs DHCP reservation explained — How-To Geek](https://www.howtogeek.com/184310/ask-htg-whats-the-difference-between-dhcp-and-static-ip-addresses/)
- [How to find MAC address on Windows/Mac/Linux — Lifewire](https://www.lifewire.com/how-to-find-your-mac-address-2542).