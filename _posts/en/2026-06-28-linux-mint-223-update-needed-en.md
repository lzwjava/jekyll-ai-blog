---
audio: false
generated: true
image: false
lang: en
layout: post
title: Linux Mint 22.3 Update Needed
translated: false
type: note
---

Question: Is Linux Mint 22.1 the latest version?

Answer:

No. Let me check the current release.No — your script points at 22.1, which is two point releases behind.

The latest stable release is **Linux Mint 22.3 "Zena"**, officially released January 13, 2026. All three editions of Linux Mint – Cinnamon, MATE, and Xfce – have been updated, and 22.3 is a long term support release which will be supported until 2029. It's still based on Ubuntu 24.04 (Noble) with Cinnamon 6.6 and improved Wayland support.

Mint 23 "Alfa" won't ship until ~December 2026 (the team moved to a longer cycle), so 22.3 is what you want now.

Fixed command — swap the URL for the 22.3 Cinnamon ISO:

```bash
curl -L -o /tmp/linuxmint.iso \
  "https://mirrors.gigenet.com/linuxmint/iso/stable/22.3/linuxmint-22.3-cinnamon-64bit.iso"
```

Everything else in the flashing flow stays the same. One thing worth doing before you `dd` — verify the ISO against the published SHA256 so you don't flash a corrupted image:

```bash
curl -L -o /tmp/sha256sum.txt \
  "https://mirrors.gigenet.com/linuxmint/iso/stable/22.3/sha256sum.txt"
cd /tmp && shasum -a 256 linuxmint.iso && grep cinnamon sha256sum.txt
```

Want me to start the 22.3 download on your Air now?
