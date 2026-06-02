---
audio: false
generated: true
image: false
lang: en
layout: post
title: Installing Scratch via Homebrew on macOS
translated: false
type: note
---

Here's exactly what I did:

**1. Pre-flight check — is Homebrew available?**
```bash
which brew && brew --version
```
Homebrew 5.1.1 was found at `/opt/homebrew/bin/brew`.

**2. Check if Scratch was already installed**
```bash
brew list --cask | grep -i scratch
ls /Applications/ | grep -i scratch
```
Neither returned anything — clean slate.

**3. Install via Homebrew Cask**
```bash
brew install --cask scratch
```
Homebrew downloaded Scratch 3.31.1 and moved `Scratch 3.app` to `/Applications/`.

**4. Verify**
```bash
ls /Applications/ | grep -i scratch
```
Confirmed `/Applications/Scratch 3.app` exists.

---

**Why Homebrew Cask?**
On macOS, `brew install --cask` is the standard way to install GUI apps — it handles the download, `.dmg` mounting, and moving to `/Applications` automatically. No flatpak, no manual download needed. The alternative is downloading the `.dmg` from `scratch.mit.edu/download` manually, but Homebrew is cleaner and easier to update later (`brew upgrade --cask scratch`).
