---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Router Handles PPPoE Dial-Up
translated: false
type: note
---

Yes, you're basically correct, but let me clarify it a bit more precisely:

1. **PPPoE dial-up is indeed software (or firmware) running on your router**
   - Almost all home or small business routers (TP-Link, ASUS, Xiaomi, Huawei, etc.) have a built-in PPPoE client in their firmware.
   - When you set up the router, you go to the WAN/Internet settings page and choose “PPPoE” mode, then enter the username and password given by your ISP (in your case, China Telecom, China Unicom, China Mobile, or some local broadband provider).
   - After you save and apply, the router itself runs the PPPoE client and “dials” (establishes the PPPoE session) automatically.

2. **It connects directly to your ISP’s BRAS (Broadband Remote Access Server)**
   - In China (and many other countries), China Telecom and most other ISPs still widely use PPPoE for authentication on FTTH (fiber) and even some ADSL/VDSL lines.
   - The physical fiber → ONT (optical modem) → your router.
   - Your router sends PPPoE packets through the ONT to the ISP’s access network, and the ISP’s BRAS authenticates your username/password and assigns you a public (or sometimes NATed) IP address.

So in normal home usage in China:
- The “dial-up” is done by the router, not by your computer.
- Your computer or phone just gets a normal LAN IP (192.168.x.x) from the router via DHCP and has no idea PPPoE even exists.
- Only in some very old ADSL setups or when you bypass the router and plug the fiber ONT directly into a PC do you need to run PPPoE software on the computer itself (such as Windows built-in PPPoE dialer or third-party clients like RasPPPoE).

Summary
Yes — in 99% of modern fiber broadband homes in China, the PPPoE “dial-up” is handled entirely by the router’s firmware. You just enter the account and password once in the router, and the router keeps the connection alive (and redials automatically if the line drops).
