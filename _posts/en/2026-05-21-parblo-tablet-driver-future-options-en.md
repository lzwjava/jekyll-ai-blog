---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parblo Tablet Driver Future Options
translated: false
type: note
---

Here's your comprehensive situation and fix options:

---

**The Problem**

| Detail | Value |
|--------|-------|
| Installed driver | Parblo Tablet Driver v3.7.1 |
| Architecture | **x86_64 (Intel-only)** — no arm64 slice |
| Built with | Xcode 10.3, targeting macOS 10.14 (Mojave) |
| Running via | Rosetta 2 on Apple Silicon |
| LaunchAgent | `com.parblo.Tablet` — starts at login |
| macOS version | 26.5 |

**Why Apple is warning you**: Apple has announced they will remove Rosetta 2 in a future macOS release. This Parblo driver is an Intel binary with no Apple Silicon support, so once Rosetta is gone, the driver simply won't run. The notification is a heads-up that you need a plan.

**Parblo's status**: Their website (parblo.com) still lists all their macOS drivers generically as "Windows&Mac" — there is no Apple Silicon / ARM-specific version available. Even the newest downloads appear to be the same old Intel build. Contacting `cs@parblo.com` to ask about ARM-native support would be the only way to confirm if they plan one, but there's no evidence they've shipped it.

---

**Your Options**

**Option A — OpenTabletDriver (recommended for the future)**

[OpenTabletDriver](https://opentabletdriver.net/) v0.6.7 is a free, open-source tablet driver that **runs natively on Apple Silicon** (no Rosetta needed). It supports many Parblo models:

- **Fully supported**: Parblo A609, A610 Pro (Variant 2), A640 V2, Ninos N4, Ninos N7
- **Has quirks** (minor issues): Parblo A610, Ninos M, Ninos N7B, Ninos S
- **Missing some features**: Parblo A610 Pro (wheel unsupported), A640 (aux buttons), Intangbo M/S (wheel), Intangbo SW (wheel + wireless)

If your model is in the "fully supported" or "has quirks" list, OpenTabletDriver is a clean drop-in replacement. Install via `brew install --cask opentabletdriver` and it coexists on ARM without Rosetta.

**Option B — Keep using the current driver (works today, uncertain tomorrow)**

The driver works fine right now via Rosetta. If you're not planning to upgrade macOS soon, you can ignore the warning for now. But it will become non-functional once Apple drops Rosetta.

**Option C — Uninstall completely** if you no longer use the tablet.

There's already an uninstaller at `/Applications/ParbloTablet/UninstallParbloTablet.app`, or use the pkg receipt: `pkgutil --forget com.parblo.pkg.Tablet` after deleting the app bundle and the launch agent at `/Library/LaunchAgents/com.parblo.Tablet.plist`.

---

Which tablet model do you have? I can tell you exactly how well it's supported by OpenTabletDriver, or help you switch to it.