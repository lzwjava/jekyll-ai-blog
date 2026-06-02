---
audio: false
generated: true
image: false
lang: en
layout: post
title: Benefits of a Three Computer Setup
translated: false
type: note
---

You've got a solid understanding of the three-computer setup! Let me validate and expand on your reasoning:

**Your breakdown is correct:**

1. **First computer** - Main workstation for daily development, coding, design, meetings, etc.
2. **Second computer** - Server/NAS running self-hosted services (Gitea, Jellyfin, Nextcloud, SearXNG, etc.)
3. **Third computer** - Experimental/sandbox machine for risky operations

**Why the third is essential for engineers:**

1. **Risk isolation** - You can brick the OS, corrupt filesystems, or mess up boot configs without affecting your other systems
2. **BIOS/firmware experimentation** - Flash custom BIOS, test overclocking, modify EFI settings without risking your main machine
3. **Kernel development** - Test kernel patches, custom drivers, or low-level changes
4. **Full reinstalls** - Practice OS deployments, test different distros, partition schemes without downtime
5. **Hardware testing** - New RAM, SSDs, expansion cards can be tested here first
6. **Security research** - Safe space to test exploits, malware analysis, penetration testing
7. **No production impact** - Services stay running on server; you keep working on machine 1

**About your server (machine 2):**

Looking at your usage stats:

- Services at **100%** (Gitea, Jellyfin, Nextcloud, SearXNG, Uptime) = running well
- **0%** on Librechat & Openclaw = either disabled or not actively used
- **57.93%** on lzwjava.github.io = moderate usage (likely your personal site)

You could potentially run `openclaw` on this machine if needed—it currently has headroom.

**The real reason:** You need separation of concerns. Experimenting on your dev machine wastes time; experimenting on your server risks losing access to your data/services. A third machine is the answer.
