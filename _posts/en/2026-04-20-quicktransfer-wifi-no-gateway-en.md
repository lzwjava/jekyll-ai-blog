---
audio: false
generated: true
image: false
lang: en
layout: post
title: QuickTransfer Wi-Fi Lacks Gateway Address
translated: false
type: note
---

Question: Why does the DJI Mini 3 Quick Transfer WiFi show only an IP address and subnet mask on iPhone, with no gateway?

Answer:

The DJI Mini 3's **QuickTransfer** mode creates a direct peer-to-peer Wi-Fi connection between the drone and your iPhone. This is a private, isolated network designed solely for high-speed file transfer (up to 25 MB/s) from the drone's storage to your phone via the DJI Fly app. It is **not** a full internet-connected network, which explains why no gateway (router address) appears.

### Why No Gateway Shows
- In a standard home or public Wi-Fi, your phone connects to a router that acts as a **gateway** to the internet. The gateway field in iPhone's Wi-Fi details points to that router (e.g., 192.168.1.1).
- With QuickTransfer, the drone itself acts as the Wi-Fi access point (like a simple ad-hoc or direct Wi-Fi server). There is **no router or internet access** involved.
- The connection is local only — your iPhone gets an IP address (typically something like 192.168.x.x) and a subnet mask (usually 255.255.255.0), but **no gateway** because nothing routes traffic beyond the drone and phone.
- This is completely normal and expected behavior for DJI QuickTransfer on iOS devices. The DJI Fly app handles all communication over this direct link using Bluetooth for initial pairing/handshaking and Wi-Fi for the actual data transfer.

### How QuickTransfer Works on DJI Mini 3
1. Power on the drone and quickly press the power button **three times** to enter QuickTransfer mode (status lights blink blue).
2. Open the DJI Fly app (ensure Bluetooth and Wi-Fi are enabled, and grant Local Network permission).
3. The app prompts you to connect to the drone's Wi-Fi network (named something like "DJI_Mini3_XXXXXX").
4. iPhone joins this network automatically or manually. You may see the limited details in Wi-Fi settings (IP + subnet only).
5. Once connected, the app shows the drone's album for fast downloads.

**Note:** On iOS, the drone's Wi-Fi often does not show a visible password in settings — the app manages the connection.

### Common Issues and Fixes If Transfer Fails
- Turn **off Cellular Data** (or enable Airplane Mode then re-enable Wi-Fi + Bluetooth) — iPhones sometimes try to use mobile data instead of the drone's Wi-Fi.
- Go to iPhone **Settings > Privacy & Security > Local Network** and ensure DJI Fly is allowed.
- Restart the drone, iPhone, and close/reopen DJI Fly.
- Forget the drone's Wi-Fi network in iPhone settings and try again (this clears old cached connections).
- Update DJI Fly app and drone firmware.
- Ensure sufficient storage on both devices and that the microSD card is properly inserted in the drone.

This direct-connection design keeps transfers fast and simple without needing internet or a controller. It is not a bug — the missing gateway is by design.

References:
- https://support.dji.com/help/content?customId=01700011149&spaceId=17&re=US&lang=en (DJI Official QuickTransfer Guidelines)
- https://www.heliguy.com/blogs/knowledge-base/how-do-i-use-dji-mini-3-s-quicktransfer/
- DJI Mini 3 User Manual and multiple user reports confirming direct Wi-Fi behavior.
