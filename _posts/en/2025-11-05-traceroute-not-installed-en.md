---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Traceroute Not Installed By Default
translated: false
type: note
---

Traceroute is definitely available on Linux—it's a standard network diagnostic tool that traces the route packets take to a destination. However, it's often **not installed by default** in many modern distributions (like Ubuntu, Fedora, or Debian minimal installs) to keep base systems lightweight. That's why it's not showing up in your tab completion for "trac".

### Quick Fix
Install it via your package manager:
- **Debian/Ubuntu**: `sudo apt update && sudo apt install traceroute`
- **Fedora/RHEL/CentOS**: `sudo dnf install traceroute` (or `sudo yum install traceroute` on older versions)
- **Arch**: `sudo pacman -S traceroute`

Once installed, typing `trac` + Tab should now include `traceroute` in the list. You can then run it like `traceroute example.com` to test.

If you're on a containerized or super-minimal setup (e.g., Alpine Linux), it might use `tr` as an alias or require a different package—let me know your distro for more specifics!
