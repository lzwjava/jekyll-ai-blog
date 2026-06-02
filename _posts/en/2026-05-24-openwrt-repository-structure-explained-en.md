---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenWrt Repository Structure Explained
translated: false
type: note
---

This is the **OpenWrt** source code — the official open-source Linux distribution for embedded devices, primarily routers and networking equipment.

Here's the breakdown of the repo structure:

```
openwrt/
├── Config.in          # Top-level Kconfig menu (make menuconfig)
├── Makefile           # Main build orchestrator
├── rules.mk           # Shared build rules for all packages
├── feeds.conf.default # External package feed sources (GitHub repos)
├── target/            # Target platform definitions (SoC, board, arch)
├── toolchain/         # Cross-compilation toolchain (gcc, musl/glibc, binutils)
├── package/           # Core packages (base system, network, kernel modules)
├── tools/             # Host tools needed for firmware builds (squashfs, zstd, etc.)
├── scripts/           # Build helper scripts (feeds, metadata, config)
├── include/           # Shared Makefile includes
├── config/            # Build system config fragments
└── LICENSES/          # License files (GPL, etc.)
```

Key facts:

- Latest commits from **2026-05-23** — this is a very recent checkout of the main branch
- Recent activity includes kernel driver patches (hwmon, realtek NIC), fstools updates, and x86 ONIE installer support
- The build system is **Kconfig + Makefile** based — you configure with `make menuconfig`, then `make` to cross-compile a full firmware image
- `feeds.conf.default` pulls in hundreds of additional packages from external Git repos

This is essentially the **build system + core source** for creating custom router firmware. It's what you'd use to build a custom image for your China Telecom Gateway router at 192.168.1.1 (which I see from your memory is running LuCI/OpenWrt already).

Are you looking to build a custom firmware, modify a package, or something else with this?
