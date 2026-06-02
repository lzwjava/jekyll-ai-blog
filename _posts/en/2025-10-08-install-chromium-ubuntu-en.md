---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Installing Chromium on Ubuntu 24.04
translated: false
type: note
---

To install **Chromium** on **Ubuntu 24.04**, you have a few good options — depending on whether you want the **official Snap version**, the **APT (Debian package)** version, or a **manual download**. Here’s a clean guide for each:

---

### 🧩 Option 1: Install via Snap (Official Ubuntu Way)

This is the **default** and most stable method.

```bash
sudo snap install chromium
```

Then run it with:

```bash
chromium
```

✅ *Advantages:*

* Officially maintained by Canonical.
* Automatically updates.

⚠️ *Disadvantages:*

* Startup may be slower.
* Snap sandboxing can cause issues with system proxies or file access.

---

### ⚙️ Option 2: Install via APT (Debian Package, Non-Snap)

If you **don’t like Snap**, you can install Chromium from a **third-party repo** such as the official Debian build provided by **ungoogled-chromium** or **OBS**.

1. Add the OBS repo:

   ```bash
   sudo apt install wget gnupg
   wget -qO - https://download.opensuse.org/repositories/home:/ungoogled_chromium/Ubuntu_24.04/Release.key | sudo gpg --dearmor -o /usr/share/keyrings/ungoogled-chromium.gpg
   ```

2. Add the repository:

   ```bash
   echo "deb [signed-by=/usr/share/keyrings/ungoogled-chromium.gpg] https://download.opensuse.org/repositories/home:/ungoogled_chromium/Ubuntu_24.04/ /" | sudo tee /etc/apt/sources.list.d/ungoogled-chromium.list
   ```

3. Install Chromium:

   ```bash
   sudo apt update
   sudo apt install ungoogled-chromium
   ```

Then run it with:

```bash
ungoogled-chromium
```

✅ *Advantages:*

* No Snap dependency.
* Privacy-hardened version available.

⚠️ *Disadvantages:*

* Updates come slower than Snap.
* Some features (like Google Sync) disabled.

---

### 🧰 Option 3: Install from Chromium’s Official Build (Manual)

If you want the **latest developer version**:

```bash
sudo apt install chromium-browser
```

If it redirects to Snap and you want to avoid that:

```bash
sudo apt purge chromium-browser
sudo apt install chromium
```

Or, download a `.deb` file manually:

```bash
wget https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/LAST_CHANGE -O /tmp/LAST_CHANGE
LATEST=$(cat /tmp/LAST_CHANGE)
wget "https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/${LATEST}/chrome-linux.zip"
unzip chrome-linux.zip
./chrome-linux/chrome
```

---

### 🌍 Note on Proxy Settings

Since your system uses:

```
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

make sure Snap and APT respect your proxy by exporting these in `/etc/environment` or your shell profile:

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

---

Would you like me to show how to make Chromium automatically use that proxy (so that it always connects through it)?
