---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Arch Linux ISO Verification GPG Key
translated: false
type: note
---

You have this GPG key (the one belonging to Pierre Schmitz, with fingerprint `3E80CA1A8B89F69CBA57D98A76A5EF9054449A5C`) in your keyring because it's the official signing key used by Arch Linux developers to cryptographically sign their ISO images. This ensures the download is authentic and hasn't been tampered with.

When you were preparing a bootable USB drive for installing Arch Linux on macOS (likely following the official Arch wiki guide), the standard process involves two steps for verification:

1. Downloading the ISO and its `.sig` file.
2. Importing the relevant developer's GPG key (in this case, Pierre Schmitz's, as he's one of the primary signers for recent ISOs) to check the signature with a command like `gpg --verify archlinux-YYYY.MM.DD-x86_64.iso.sig`.

You probably ran something like `gpg --keyserver hkps://keys.openpgp.org --recv-keys 3E80CA1A8B89F69CBA57D98A76A5EF9054449A5C` to fetch and import it, which added it permanently to your local GPG keyring. That's why it shows up in `gpg --list-keys`.

It's harmless—GPG keys are just public data for verification purposes—and many Arch users end up with a few of these after verifying ISOs. If you don't need it anymore and want to remove it, run:

```
gpg --delete-key 3E80CA1A8B89F69CBA57D98A76A5EF9054449A5C
```

(You'll be prompted to confirm; it only deletes the public key, not any signatures you've already verified.)

[Arch Linux ISO Download Page](https://archlinux.org/download/)
[Arch Wiki: Install Arch Linux on a Mac](https://wiki.archlinux.org/title/Install_Arch_Linux_on_Mac)
[Pierre Schmitz's GPG Keys](https://pierre-schmitz.com/gpg-keys/)
