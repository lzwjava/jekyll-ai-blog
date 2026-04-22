---
audio: false
generated: true
image: false
lang: en
layout: post
title: Installing WSL on Windows Guide
translated: false
type: note
---

Question: How to install WSL on Windows?

Answer:

WSL (Windows Subsystem for Linux) lets you run a real Linux environment (like Ubuntu) directly on Windows. The modern setup is very simple—Microsoft has mostly automated it.

---

## 1. Check your Windows version

WSL 2 works best on:

* Windows 10 version 2004+ (Build 19041+)
* Windows 11 (recommended)

You can check by:

```text
Win + R → winver
```

---

## 2. Install WSL (fastest method)

Open **PowerShell as Administrator**, then run:

```powershell
wsl --install
```

This single command will:

* Enable required Windows features
* Install WSL 2
* Download and install **Ubuntu (default Linux distro)**
* Set WSL 2 as default

---

## 3. Restart your computer

After installation completes:

* Reboot Windows

---

## 4. First-time Linux setup

After restart:

* Ubuntu will open automatically
* It will ask you to:

  * Create a Linux username
  * Set a password

That’s your Linux environment inside Windows.

---

## 5. Verify installation

Run:

```powershell
wsl --list --verbose
```

You should see something like:

```text
Ubuntu    Running    2
```

---

## 6. Upgrade WSL (if needed)

To ensure WSL 2 is used:

```powershell
wsl --set-default-version 2
```

---

## 7. Install another Linux distro (optional)

List available distros:

```powershell
wsl --list --online
```

Install example:

```powershell
wsl --install -d Debian
```

---

## 8. How to use WSL

You can open it in multiple ways:

* Start menu → “Ubuntu”
* VS Code → “WSL extension”
* Terminal:

```bash
wsl
```

---

## 9. Using WSL with VS Code (highly recommended)

Install:

* VS Code extension: **WSL**

Then inside WSL terminal:

```bash
code .
```

This opens your Linux environment directly in VS Code.

---

## 10. Why WSL is useful (especially for you)

Since you're doing dev + SSH + AI tools:

WSL gives you:

* Native Linux tools (`ssh`, `grep`, `curl`, `bash`, `python`)
* No Windows path issues
* Better compatibility with servers
* Cleaner dev environment than Git Bash

---

## Quick recommendation

If your goal is:

* SSH to servers
* Use Copilot
* Run dev tools consistently

👉 WSL 2 + Ubuntu is the best long-term setup on Windows.

---

If you want, I can help you set up a **perfect WSL dev environment (Git, SSH keys, Docker, Python, Node, VS Code integration)** in one go.