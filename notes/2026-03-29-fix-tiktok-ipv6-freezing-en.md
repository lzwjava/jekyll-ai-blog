---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix TikTok Freezing by Disabling IPv6
translated: false
type: note
---

**Question:** TikTok (Douyin) keeps freezing while scrolling. Someone said disabling IPv6 DHCP on the router (so no IPv6 address gets assigned) fixes it — is that correct, and how do you do it?

**Answer:**

## Why Disabling IPv6 DHCP Can Fix TikTok/Douyin Freezing

Yes, this is a **valid and commonly reported fix**. Here's the reasoning:

Some ISPs and devices don't fully support IPv6, which causes delays or interruptions in streaming. Disabling IPv6 forces the device to use IPv4 instead, which is more stable in most cases.

When your router assigns an IPv6 address via DHCPv6, your phone may try to reach TikTok's CDN servers over IPv6. If your ISP's IPv6 routing is unstable or misconfigured, the connection drops mid-stream — causing that freeze/stutter. Turning off IPv6 DHCP means no IPv6 address gets assigned, so your device falls back entirely to IPv4.

---

## How to Disable IPv6 DHCP on Your Router

Most routers allow you to disable IPv6 through their web interface. Access your router settings by opening a web browser and entering your router's IP address. Log in with your username and password. Find the IPv6 settings — they are usually under "Advanced" or "Network" settings. Then select the option to disable IPv6 and save your changes.

**General steps:**

1. Open a browser, go to your router's admin page — usually `192.168.1.1` or `192.168.0.1`
2. Log in (default credentials are often on the router label)
3. Navigate to **Advanced** → **IPv6** (or **WAN** → **IPv6**)
4. Set IPv6 to **Disabled** (or set DHCPv6 to **Off**)
5. Save and reboot the router

> **Note:** The exact menu location varies by router brand (TP-Link, Xiaomi, ASUS, Huawei, etc.). Look for labels like "IPv6 Enable/Disable", "DHCPv6 Server", or "IPv6 Address Assignment".

---

## Alternative: Disable IPv6 on Your Phone Only (Without Touching the Router)

If you don't want to affect other devices on the network, you can disable IPv6 at the device level:

- **Android:** Go to **Settings → Wi-Fi → Long-press your network → Modify Network → Advanced → IP Settings → Static** (this prevents DHCPv6 assignment, though support varies by Android version)
- **iPhone/iPad:** Apple doesn't allow you to disable IPv6 on your iPhone or iPad directly, but you can do it on your router.

---

## Is This Safe?

Yes. Disabling IPv6 does not leave you without internet. Your connection will continue working with IPv4, which is the standard and is normally more compatible.

Microsoft recommends using "Prefer IPv4 over IPv6" in settings rather than fully disabling IPv6, to avoid potential issues with some system components. However, for a home router used primarily for streaming, fully disabling IPv6 is generally safe.

---

## Summary

| Action | Effect |
|---|---|
| Disable IPv6 DHCP on router | No device gets an IPv6 address → forces IPv4 → fixes freezing |
| Disable IPv6 on device only | Same effect but only for that device |
| Leave IPv6 enabled | Risk of unstable streaming if ISP's IPv6 routing is poor |

**Bottom line:** Yes, your approach is correct. Disabling IPv6 DHCP on the router is the cleanest solution — it fixes TikTok freezing for all devices on the network by preventing IPv6 addresses from being assigned in the first place.

**References:**

- [Disable IPv6 to Fix Streaming Buffering Issues – OSN+](https://support.osnplus.com/hc/en-us/articles/9116545086618-Disable-IPv6-on-Your-TV-to-Fix-OSN-Buffering-Issues-Troubleshooting-Guide)
- [How to Disable IPv6 on Routers, iPhone & Android – RapidSeedbox](https://www.rapidseedbox.com/blog/disable-ipv6)
- [How to Enable/Disable IPv6 – NordVPN](https://nordvpn.com/blog/ipv6-enable-or-disable/)