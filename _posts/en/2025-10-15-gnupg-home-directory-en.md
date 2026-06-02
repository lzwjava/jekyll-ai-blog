---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GnuPG Home Directory Contents Explained
translated: false
type: note
---

These files and directories are part of your GnuPG (GPG) home directory (`~/.gnupg/`), which stores cryptographic keys and related data for encryption, signing, and authentication. GPG is a tool for secure communication and data protection. Here's a breakdown of each one based on standard GnuPG 2.1+ behavior:

- **openpgp-revocs.d**: A directory containing revocation certificates (`.rev` files) generated when you create keypairs. These are used to revoke (invalidate) your keys if they're compromised or no longer needed, preventing further use.

- **private-keys-v1.d**: A directory storing your private (secret) keys in the modern key format introduced in GnuPG 2.1. Each key is in its own file for better security and management. Keep this highly protected—it's like your digital vault.

- **pubring.kbx**: The public keyring file in the new "keybox" format (`.kbx`). It holds your imported public keys from others, which you use to encrypt messages to them or verify their signatures.

- **pubring.kbx~**: A backup copy of `pubring.kbx`, automatically created by GPG during edits or updates. The tilde (`~`) suffix is a common Linux convention for backups.

- **trustdb.gpg**: The trust database file, which tracks the trust levels you've assigned to public keys (e.g., "ultimate" for your own keys, or levels for others based on signatures). It helps GPG decide if a key is reliable for validation.

If you've recently generated or imported keys, this setup is normal. Always back up your entire `~/.gnupg/` directory securely, and never share private keys. For more details, check the official GnuPG docs.

[Using the GNU Privacy Guard](https://www.gnupg.org/documentation/manuals/gnupg.pdf)
[GnuPG Part 2 - Create and Manage Keys](https://www.hacksanity.com/kb/gnupg-create-manage-keys/)
[How to Back Up and Restore Your GPG Keys on Linux](https://www.howtogeek.com/816878/how-to-back-up-and-restore-gpg-keys-on-linux/)
[GPG(1) Manual](https://www.gnupg.org/(en)/documentation/manuals/gnupg24/gpg.1.html)
