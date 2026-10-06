---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ubuntu 26.04 Codename Not Resolute
translated: false
type: note
---

**Question:** Does Ubuntu 26.04 use the same "resolute" codename and persistence setup as what's shown on screen?

**Answer:**

**No**, Ubuntu and Kali Linux are different distributions. Here's the comparison:

---

**Codename System — Different:**

| Distro | Codename Style | Example |
|---|---|---|
| **Kali Linux** | Adjectives | `resolute`, `kali-rolling` |
| **Ubuntu** | Animal names (Adjective + Animal) | `noble` (24.04), `oracular` (24.10) |

**Ubuntu 26.04 codename** would follow the pattern — likely something like **"P\_\_\_\_ P\_\_\_\_"** (starts with P, not yet officially announced as of now).

---

**Persistence Setup — Also Different:**

| Feature | Kali Live USB | Ubuntu Live USB |
|---|---|---|
| Persistence label | `writable` | `casper-rw` |
| Persistence folder | `/log-persistence` | `/casper-rw` |
| Default user | `kali/kali` | `ubuntu` (no password) |
| APT source label | `resolute` (Kali codename) | `noble`, `oracular`, etc. |

---

**Bottom Line:**

What's on your screen is **definitely Kali Linux**, not Ubuntu. The word **"resolute"** in the boot log is the giveaway — that is Kali's release codename, Ubuntu has never used that name.

If you want to use Ubuntu instead, you would flash `ubuntu-26.04-desktop-amd64.iso` separately with a tool like **Balena Etcher** or **Rufus**.

---

**References:**
- [Kali Linux 2024.4 "resolute" release](https://www.kali.org/blog/kali-linux-2024-4-release/)
- [Ubuntu release codenames list](https://wiki.ubuntu.com/DevelopmentCodeNames)
- [Balena Etcher — USB flashing tool](https://etcher.balena.io/)
