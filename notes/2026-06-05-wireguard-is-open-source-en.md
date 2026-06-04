---
audio: false
generated: true
image: false
lang: en
layout: post
title: WireGuard Is Open Source
translated: false
type: note
---

**Question:** Is WireGuard open source?

**Answer:**

Yes. WireGuard is free and open-source software, with Linux kernel components licensed under GPLv2, and other implementations under GPLv2 or other free/open-source licenses.

**Official repositories:**

Official repositories are hosted at git.zx2c4.com (with GitHub mirrors available). Main projects:

- **wireguard-linux** — kernel module (Linux)
- **wireguard-go** — userspace implementation (Go, portable)
- **wireguard-windows** — NT kernel driver (Windows)
- **wireguard-apple** — iOS/macOS
- **wireguard-android** — Android
- **wireguard-tools** — configuration utilities (`wg`, `wg-quick`)

Created by Jason A. Donenfeld in 2015, currently at stable release 1.0.20260223 (February 2026).

You can audit the code directly — no proprietary components. This is why Tailscale chose WireGuard as its foundation: the protocol is openly reviewed, battle-tested, and independently verifiable.

**References:**

- [WireGuard Official](https://www.wireguard.com/)
- [Official Repositories](https://www.wireguard.com/repositories/)
- [WireGuard GitHub (mirrors)](https://github.com/WireGuard)
- [Whitepaper (PDF)](https://www.wireguard.com/papers/wireguard.pdf)
