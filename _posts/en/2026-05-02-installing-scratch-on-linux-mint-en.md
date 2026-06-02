---
audio: false
generated: true
image: false
lang: en
layout: post
title: Installing Scratch on Linux Mint
translated: false
type: note
---

Question: How can I install Scratch on Linux Mint, and is it supported on Linux or only on Windows?

Answer:

Scratch is fully supported on Linux, not just Windows. In fact, it runs very well on Linux Mint. You have several easy ways to install and use it.

---

## ✅ Option 1: Use Scratch Online (No installation needed)

The simplest way is to use Scratch directly in your browser:

* Open: [https://scratch.mit.edu](https://scratch.mit.edu)
* Works on Linux Mint, Windows, macOS, and even Chromebooks
* No setup required
* Always the latest version

This is recommended if you just want to start quickly.

---

## 🧩 Option 2: Install Scratch Desktop (Offline app)

### Method A — Flatpak (Recommended for Linux Mint)

Linux Mint supports Flatpak by default.

1. Open Terminal
2. Run:

```bash
flatpak install flathub edu.mit.Scratch
```

3. Launch it:

```bash
flatpak run edu.mit.Scratch
```

Or search “Scratch” in your application menu after installation.

---

### Method B — Snap (alternative)

If Snap is enabled:

```bash
sudo snap install scratch-desktop
```

---

## 🧰 Option 3: Install via Software Manager (GUI way)

Linux Mint also has a graphical store:

1. Open **Software Manager**
2. Search for **Scratch**
3. Click **Install**

---

## 🖥️ Compatibility Notes

* ✔ Linux Mint: Fully supported
* ✔ Windows: Fully supported
* ✔ macOS: Fully supported
* ✔ Web browser version: works everywhere
* ⚠ Desktop app is mainly a wrapper around the web version, but works offline for basic projects

---

## 💡 Recommendation

* If you are learning or teaching → use browser version
* If you want offline work → use Flatpak version
* If you want simplicity → Software Manager install

---

If you want, I can also show:

* how to create your first Scratch project
* how to teach a child Scratch step-by-step
* or how to run Scratch on low-end Linux machines smoothly
