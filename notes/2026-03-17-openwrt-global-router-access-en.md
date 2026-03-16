---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenWrt Router for Global Access
translated: false
type: note
---

**Question:** I want to set up a home router in China to serve as an entry point at my home for better global network access. I have a fast Hysteria2 server in Los Angeles. I tried using an old 2013 Lenovo laptop with Linux Mint, but the iPad connected via USB still cannot connect. I also have a Xiaomi WiFi router that already has OpenWrt installed, but I have not yet installed LuCI or proxy apps due to past difficulties. Now with OpenClaw (AI agent) to help with configuration, should I go back to the OpenWrt solution? What do you think?

**Answer:**

Yes, you should absolutely go back to the OpenWrt solution on your Xiaomi WiFi router. It is the far better long-term choice for your goal of creating a proper home-wide entry point in China that routes traffic through your fast Los Angeles Hysteria2 server for global access. Here's a clear breakdown of why, plus exactly how to proceed with AI assistance (me) making it simple this time.

### Why OpenWrt on Xiaomi beats the laptop + USB setup
- **Whole-home coverage instead of one device**: Your current laptop setup only serves the iPad via USB tethering (with all the DHCP, forwarding, NAT, and routing-loop headaches you already debugged). The Xiaomi router will proxy *every* device on your home WiFi and wired LAN automatically — phones, laptops, TVs, smart devices, etc. — without any USB cables or per-device tweaks.
- **No more USB-specific problems**: The summary you provided shows the laptop architecture is now mostly correct (DHCP working, forwarding allowed, NAT active, Clash split-routing with loop prevention). The remaining issue is almost certainly just the iPad caching the old DNS (8.8.8.8). A quick "Forget this network + reconnect" or manual DNS set to 192.168.201.1 on the iPad would probably finish it. But even if it works, the laptop is a 2013 machine — it will run hot, draw more power, and is not designed for 24/7 router duty. The Xiaomi is purpose-built for this.
- **Native, stable proxy tools**: OpenWrt was made exactly for this use case. Your Xiaomi already has OpenWrt flashed, so you skip the hard part. The community packages handle Hysteria2, DNS hijacking, fake-IP, split routing (local subnets + Apple/iCloud + Chinese sites DIRECT, everything else Hysteria2), and DHCP DNS push perfectly — without manual ufw rules or dnsmasq edits.
- **Performance & reliability**: Hysteria2 is UDP-heavy and benefits from router hardware. Your old laptop works, but a dedicated router will be more stable and use less electricity.

### Recommended tool: PassWall2 (not OpenClash)
You mentioned "openclaw" (likely OpenClash) and LuCI. OpenClash is popular and can import your existing Clash config, but recent OpenWrt versions (especially kernel 6.6 in 24.10+) have occasional Hysteria2 compatibility issues under certain WAN types. 

**PassWall2** is the clear winner here:
- Full native support for Hysteria2 via the sing-box backend (latest packages as of 2026 include hysteria 2.6.5+).
- Built-in split routing, China-list DIRECT rules, Apple/iCloud bypass, and DNS handling — exactly matching the rules you already tuned on the laptop (IP-CIDR 192.168.1.0/24 and 192.168.201.0/24 DIRECT, etc.).
- Easy LuCI web interface — no command-line needed after initial install.
- Pre-built IPK packages work on almost all Xiaomi models.

### Step-by-step plan (I will guide you live)
1. Log into your Xiaomi's OpenWrt LuCI web interface (usually 192.168.1.1).
2. Update packages: `opkg update`.
3. Install PassWall2 (I will give you the exact wget/opkg commands for your router architecture once you tell me the exact Xiaomi model and OpenWrt version — run `cat /etc/openwrt_release` and paste it).
4. Upload/import your existing Clash config (the one with Hysteria2 outbound + the split rules you already perfected).
5. Set LAN DNS to the PassWall2 DNS server (it auto-pushes via DHCP, just like the dnsmasq fix you did).
6. Enable masquerading/NAT and the same loop-prevention rules.
7. Test exactly as in your summary:
   - iPad connects to WiFi → gets IP automatically.
   - `nslookup google.com` returns fake-IP (198.18.x.x).
   - `curl https://api.ipify.org` shows your LA US IP.
   - `curl baidu.com` works DIRECT.

Because you already solved every routing/DNS/firewall puzzle on the laptop, translating it to PassWall2 will take under 30 minutes with me walking you through screenshots and exact commands. Previous difficulties were because you didn't have real-time AI help — now you do.

If you want to finish the laptop setup first for a quick test (just renew the iPad DHCP lease), that's fine as a backup. But for your stated goal of a "home router" entry point, the Xiaomi + PassWall2 is the professional, clean solution.

Tell me your exact Xiaomi model (e.g., Mi Router 4A, AX1800, etc.) and OpenWrt version, and I'll give you the precise installation commands right now. We can have this running today.

**References:**
- [Openwrt-Passwall/openwrt-passwall2](https://github.com/Openwrt-Passwall/openwrt-passwall2)
- [2026 PassWall2 Tutorial](https://passwall2.org/)