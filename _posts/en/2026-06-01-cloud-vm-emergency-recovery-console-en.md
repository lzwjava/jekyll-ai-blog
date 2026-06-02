---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloud VM Emergency Recovery Console
translated: false
type: note
---

**Question:** What does "Recovery Console" mean in the context of the AMD Developer Cloud / DigitalOcean droplet management UI?

**Answer:**

This is standard cloud VM emergency access tooling. Here's what each thing means:

**Recovery Console**
A browser-based serial/VNC console that connects directly to the VM's virtual display output — bypassing SSH entirely. It's the equivalent of physically sitting in front of the server. Use it when:
- SSH is broken (bad sshd config, firewall locked you out, wrong keys)
- The network stack is misconfigured
- The VM is in a boot loop or kernel panic
- You need to run `fsck`, edit `/etc/fstab`, or fix GRUB

**Recovery ISO**
Boots the droplet into a live rescue OS (minimal Linux) instead of your installed system. Your original disk is mounted as `/mnt` or similar. Use it when:
- The OS itself won't boot
- You need to `chroot` in and fix a broken system
- Filesystem corruption that needs repair from outside

**Password Authentication**
SSH normally uses key-based auth. The Recovery Console requires a password (since you can't pass an SSH key through a browser serial terminal). So you need to either set or enable root password login just to use this console.

**Reset Root Password**
Injects a new root password via the hypervisor (cloud-init or similar), even if you can't log in. This is the escape hatch when you've lost access entirely.

---

**TL;DR for your situation:**

If your AMD Dev Cloud droplet is unreachable via SSH:
1. Launch Recovery Console → browser terminal, no SSH needed
2. Fix whatever is wrong (sshd, firewall, network, etc.)
3. Or boot Recovery ISO → mount your disk → `chroot` → repair

It's the equivalent of IPMI/iDRAC/iLO on bare metal — out-of-band access that survives a broken OS.
