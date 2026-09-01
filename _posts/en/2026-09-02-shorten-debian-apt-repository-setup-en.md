---
audio: false
generated: true
image: false
lang: en
layout: post
title: Shorten Debian APT Repository Setup
translated: false
type: note
---

Question: Can the Debian APT repository setup be shortened?

Answer: Yes. If you just want a simple Debian 13 repository, use the old-style `sources.list` format:

```bash
sudo sh -c 'echo "deb https://deb.debian.org/debian trixie main" > /etc/apt/sources.list'
```

Then:

```bash
sudo apt update
sudo apt install openssh-server
```

If you also want security + updates, one compact command:

```bash
sudo sh -c 'printf "%s\n" \
"deb https://deb.debian.org/debian trixie main" \
"deb https://deb.debian.org/debian trixie-updates main" \
"deb https://security.debian.org/debian-security trixie-security main" \
> /etc/apt/sources.list'
```

For your use case, **the first one is enough to get started**. You can add `trixie-updates` and `trixie-security` later.

Even shorter if you don't care about `sources.list` format:

```bash
echo 'deb https://deb.debian.org/debian trixie main' | sudo tee /etc/apt/sources.list
```

Then:

```bash
sudo apt update && sudo apt install openssh-server
```
