---
audio: false
generated: true
image: false
lang: en
layout: post
title: VPN on iPhone, Not on Hotspot
translated: false
type: note
---

Yes, it's generally okay to use your iPhone 14 Pro Max on 5G cellular data with a VPN app like Shadowrocket enabled while sharing a personal hotspot to your Mac laptop. There's typically no inherent conflict in this setup, as iOS is designed to handle both features simultaneously without disabling one or the other.

Regarding your specific question: The traffic from devices connected to your iPhone's personal hotspot (like your Mac laptop) does not route through the VPN configured on the iPhone itself. Instead, the hotspot shares the raw cellular connection directly, bypassing the VPN tunnel. This means:

- Your iPhone's own apps and traffic will use the VPN (e.g., Shadowrocket's proxy or tunnel).
- But the Mac laptop's internet traffic will go straight through the cellular network without the VPN's encryption or routing applied.

If you want the Mac's traffic to also use a VPN, you'd need to set one up directly on the Mac itself.

[Does the VPN monitor my Hotspot traffic? - Accountable2You Support](https://support.accountable2you.com/article/791-faq-does-the-vpn-monitor-my-hotspot-traffic)
[If I am connected to my phone's hotspot on my laptop and VPN is activated on the phone, does the laptop also get VPN security protection? - Quora](https://www.quora.com/If-I-am-connected-to-my-phones-hotspot-on-my-laptop-and-VPN-is-activated-on-the-phone-does-the-laptop-also-get-VPN-security-protection)
[Why does shared WiFi connection from iPhone to laptop (personal hotspot) not go through VPN? - Apple Stack Exchange](https://apple.stackexchange.com/questions/400853/why-does-shared-wifi-connection-from-iphone-to-laptop-personal-hotspot-not-go)
