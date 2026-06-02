---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Install Zed on Ubuntu 24.04
translated: false
type: note
---

For Ubuntu 24.04 LTS, the most straightforward and official installation method for Zed (the high-performance code editor) is via their provided shell script, which works natively on most Linux distributions including Debian-based ones like Ubuntu. It handles dependencies automatically and ensures you get the latest stable release.

### Recommended Installation: Official Script

Run this in your terminal:

```
curl -f https://zed.dev/install.sh | sh
```

- This installs Zed to `~/.local/bin/zed` (add to your PATH if needed: `export PATH="$HOME/.local/bin:$PATH"` in `~/.bashrc` or similar).
- Prerequisites: Your system (glibc 2.39 on kernel 6.14) meets the requirements (x86_64 glibc >= 2.31).
- After install, launch with `zed` or from GNOME's app menu.
- For the preview channel (nightly builds): `curl -f https://zed.dev/install.sh | ZED_CHANNEL=preview sh`.

If you prefer a sandboxed, universal package (no native deps to worry about), use the Flathub option from your list (`dev.zed.Zed`) via Flatpak:

1. Install Flatpak if not present: `sudo apt update && sudo apt install flatpak`.
2. Add Flathub repo: `flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo`.
3. Install: `flatpak install flathub dev.zed.Zed`.
4. Run: `flatpak run dev.zed.Zed`.

The script is generally faster and more integrated for a desktop like GNOME, but Flatpak is great if you want isolation or already use it for other apps. Avoid the other options in your list, as they're for non-Debian distros and won't work directly on Ubuntu without extra setup.

### References

- [Zed Linux Installation Docs](https://zed.dev/docs/linux)
- [Zed on Linux Announcement](https://zed.dev/linux)
- [Repology Zed Packages](https://repology.org/project/zed-editor/versions)
