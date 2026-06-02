---
audio: false
generated: true
image: false
lang: en
layout: post
title: Android VPN Clients for Hysteria 2
translated: false
type: note
---

Question: Which Android client VPN supports Hysteria 2?

Answer:

Several Android apps support **Hysteria 2** (a QUIC-based proxy/VPN protocol). Hysteria 2 itself does not have an official full-featured Android APK from the core project (only low-level binaries exist), so third-party clients are the main options. These apps integrate Hysteria 2 support and often function in full VPN mode (using Android's VPN service) or system proxy mode.

Here are the most commonly recommended and officially listed Android clients that support Hysteria 2 (as of early 2026, based on the official Hysteria documentation and community usage):

- **Hiddify** (often recommended for ease of use)
  A popular multi-protocol VPN/proxy app with good Hysteria 2 support. It allows easy import of `hy2://` links and works in full VPN mode.
  Download: GitHub releases (<https://github.com/hiddify/hiddify-app/releases>) or sometimes available via other sources.

- **NekoBox for Android**
  A universal proxy toolchain app with Hysteria 2 support since version 1.2.4. It is widely used for advanced configurations.
  GitHub: <https://github.com/MatsuriDayo/NekoBoxForAndroid>

- **Sing-box / SFA (sing-box for Android)**
  Official sing-box client for Android (io.nekohasekai.sfa on Play Store). Supports Hysteria 2 natively and is frequently mentioned for clean Hysteria 2 setups.
  Play Store: Search for "sing-box" or use the package name above.

- **V2Box**
  Multi-protocol proxy client with Hysteria 2 support since version 2.6.1. Available directly on Google Play Store.
  Link: <https://play.google.com/store/apps/details?id=dev.hexasoftware.v2box>

Other mentions in communities include forks or specialized apps like custom Hysteria 2-only clients on GitHub (e.g., lry127/Android-Hysteria-2-client), but these are less polished and not as widely recommended.

For the most up-to-date and complete list, check the official Hysteria 2 documentation page on third-party apps.

References:

- [https://v2.hysteria.network/docs/getting-started/3rd-party-apps](https://v2.hysteria.network/docs/getting-started/3rd-party-apps)
- [https://fornex.com/help/hysteria2-vpn-android](https://fornex.com/help/hysteria2-vpn-android)
- [https://github.com/MatsuriDayo/NekoBoxForAndroid](https://github.com/MatsuriDayo/NekoBoxForAndroid)
- [https://play.google.com/store/apps/details?id=dev.hexasoftware.v2box](https://play.google.com/store/apps/details?id=dev.hexasoftware.v2box)
