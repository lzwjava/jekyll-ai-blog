---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing APT GPG Signature Error
translated: false
type: note
---

The error you’re seeing means APT refuses to update from the ShiftKey repo because it can’t verify its GPG signature. You have two simple ways to fix this:

---

## 1. **Remove or disable the broken repository**

If you don’t actually need `https://apt.packages.shiftkey.dev/ubuntu`, just disable it:

```bash
# Find the file defining that repo (it’ll live in /etc/apt/sources.list.d/)
ls /etc/apt/sources.list.d/shiftkey*

# Remove it (replace with the actual filename)
sudo rm /etc/apt/sources.list.d/shiftkey.packages.shiftkey.dev.list

# Then update and install
sudo apt update
sudo apt install pkg-config libssl-dev
```

---

## 2. **Import the repo’s signing key**

If you do want to keep using ShiftKey’s packages, you need to fetch and install its public key:

```bash
# Download & dearmor their GPG key into APT’s keyring
curl -fsSL https://apt.packages.shiftkey.dev/ubuntu/pubkey.gpg \
  | gpg --dearmor \
  | sudo tee /usr/share/keyrings/shiftkey-archive-keyring.gpg > /dev/null

# Edit the repo file so it references that keyring.
# Open /etc/apt/sources.list.d/shiftkey*.list in your editor, and change the deb line to:
#   deb [signed-by=/usr/share/keyrings/shiftkey-archive-keyring.gpg] https://apt.packages.shiftkey.dev/ubuntu any main

# Then update & install
sudo apt update
sudo apt install pkg-config libssl-dev
```

---

Once APT can update without GPG errors, you’ll be free to install `pkg-config` and `libssl-dev`, and then rebuild:

```bash
cargo clean
cargo run
```
