---
audio: false
generated: true
image: false
lang: en
layout: post
title: Node.js Upgrade Guide for Ubuntu
translated: false
type: note
---

Upgrading Node.js on Ubuntu can be done in several ways. The most reliable and recommended methods are using **`nvm` (Node Version Manager)** or the **NodeSource repository**. Below are step-by-step instructions for both methods.

---

## **Method 1: Using NVM (Recommended)**

NVM allows you to install and manage multiple Node.js versions easily.

### 1. Install NVM

Open a terminal and run:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

Then, reload your shell:

```bash
source ~/.bashrc
```

or

```bash
source ~/.zshrc
```

(depending on your shell)

### 2. Install the Latest Node.js Version

List available versions:

```bash
nvm ls-remote
```

Install the latest LTS version (recommended for most users):

```bash
nvm install --lts
```

Or install a specific version (e.g., 20.x):

```bash
nvm install 20
```

### 3. Set Default Version

```bash
nvm alias default 20
```

### 4. Verify

```bash
node -v
npm -v
```

---

## **Method 2: Using NodeSource Repository**

This method installs Node.js system-wide.

### 1. Remove Old Node.js (if installed via apt)

```bash
sudo apt remove --purge nodejs npm
sudo apt autoremove
```

### 2. Add NodeSource Repository

For **Node.js 20.x** (LTS as of August 2025):

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
```

For **Node.js 22.x** (if available):

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
```

### 3. Install Node.js

```bash
sudo apt install -y nodejs
```

### 4. Verify

```bash
node -v
npm -v
```

---

## **Method 3: Using Ubuntu Default Repository (Not Recommended)**

Ubuntu's default repository often contains outdated Node.js versions. If you still want to use it:

```bash
sudo apt update
sudo apt install nodejs npm
```

But this is **not recommended** for development, as the version is usually old.

---

## **Which Method Should You Use?**

- **Use NVM** if you want to switch between Node.js versions easily or need the latest features.
- **Use NodeSource** if you want a system-wide, stable installation.
