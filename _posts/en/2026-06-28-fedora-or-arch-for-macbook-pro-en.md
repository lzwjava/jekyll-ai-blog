---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fedora or Arch for MacBook Pro
translated: false
type: note
---

Question: What's the best Linux distro for a 2017 MacBook Pro, given my profile?

Answer:

Short version: **Fedora** or **Arch**, not Mint. Mint is the right call for a general user installing their first Linux. You're not that user — you train models, live in the terminal, and want frontier tooling. Mint's whole value proposition (stability, conservative packages, hand-holding) is friction for you.

But the 2017 MacBook Pro has hardware quirks that matter more than the distro choice. Let me search for the current state of that hardware support before recommending.Here's the real situation. The 2017 13"/15" MacBook Pro (A1707/A1706, MacBookPro14,x) has a **T1 chip (iBridge)** — not the harder T2. That matters a lot. The known pain points, per the maintained tracker repos: the basic keyboard works but the Touch Bar with Esc and function keys needs a custom driver, Wi-Fi is partly functional, suspend can't resume much hardware, and TouchID isn't supported. Sound also needs the out-of-tree `snd_hda_macbookpro` driver — the upstream cs8409 driver in Linux 6.18 still doesn't fully work for some users.

Critical gotcha that overrides distro choice: the T1 chip provides the camera, ambient light sensor, Touch Bar and Touch ID, and all of these depend on firmware that macOS stores on the EFI system partition. The easiest way to keep that firmware available is to install Linux alongside macOS and leave the original ESP in place. So **don't wipe the disk — dual-boot, keep macOS's ESP.** If you nuke it, you lose the camera and Touch Bar firmware and recovery gets painful.

The two things that decide the distro here are **kernel freshness** and **DKMS ergonomics**, because you'll be building out-of-tree drivers (`applespi`, `apple_ib_tb`, the sound driver). That's the lens for the recommendation.

What I'd actually pick, in order:

**1. Fedora (Workstation) — my top pick for you.** Ships a recent mainline kernel (6.17+ in the 2026 release), excellent DKMS support, SELinux/security defaults you'll learn from, and it's what a lot of kernel/ML people run. Newer kernel = more of this hardware works out of the box, less driver-wrangling. You won't fight conservative package versions for your CUDA-adjacent / Python ML stack.

**2. Arch (or EndeavourOS if you want a faster install).** Bleeding-edge kernel, the AUR has `macbook12-spi-driver` and `snd-hda-macbook` packaged, and the Arch Wiki has the best Mac-specific documentation. This is the *most aligned with your Yin-Wang / first-principles ethos* — you build the system, you understand every layer. The cost is time, and on this laptop you'll spend real hours on the Touch Bar and suspend. Worth it if you treat the install as a learning exercise; not worth it if you just want a working machine.

**3. Mint — skip it.** It's pinned to the Ubuntu 24.04 base with kernel 6.8/6.11, which is *older* than what you want for marginal hardware. One user got the Touch Bar working on Ubuntu 24.04 but only on the 6.8.0 kernel, not the 6.11.x kernels — that kind of regression dance is exactly what an LTS-conservative distro inflicts on quirky hardware. You're over-qualified for Mint's hand-holding and under-served by its old kernels.

A 2017 MBP is a fine secondary Linux box, but be clear-eyed: this is a tinkerer's install, not a clean one. If you mainly want a no-friction Linux experience, that's what the RTX 4070 workstation (`lzw@192.168.1.36`) is for — run Fedora or Ubuntu there bare-metal and keep the MBP as a portable terminal. The MBP install is worth doing if you *want* the kernel-driver rabbit hole; if you just want a working laptop, it'll frustrate you.

Practical path if you go Fedora:
- Dual-boot, preserve macOS + ESP (firmware dependency above).
- After install, expect to build: `macbook12-spi-driver` (keyboard/touchpad/Touch Bar) and `snd_hda_macbookpro` (sound), both via DKMS so they survive kernel updates.
- Wi-Fi (Broadcom BCM43xx) needs `broadcom-wl` / `wl` DKMS — flaky on 5GHz per the reports, so have a USB-C ethernet dongle ready for the install.

Want me to adjust the flashing script for the Fedora Workstation ISO (verify-then-`dd`, same flow as before), or write out the post-install DKMS driver setup as a script?
