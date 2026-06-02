---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remote Mac Control via TeamViewer
translated: false
type: note
---

Question: How can I connect and remotely control another Mac (my wife’s Mac) using TeamViewer?

Answer:

To remotely control your wife’s Mac from your Mac using TeamViewer, follow these steps carefully:

---

## 1. Install TeamViewer on both Macs

* On **both your Mac and your wife’s Mac**:

  * Go to the official website of TeamViewer
  * Download and install the macOS version
  * Open the app after installation

---

## 2. Get your wife’s Mac ID and password

On your wife’s Mac:

* Open TeamViewer
* You will see:

  * **Your ID** (a number)
  * **Password** (temporary by default)

👉 She needs to send you:

* Her **ID**
* Her **password**

---

## 3. Connect from your Mac

On your Mac:

* Open TeamViewer
* In **“Control Remote Computer”**:

  * Enter her **ID**
  * Click **Connect**
  * Enter her **password**

Now you should see her screen and can control her Mac.

---

## 4. Important macOS permissions (VERY important)

macOS blocks remote control unless permissions are enabled.

On your wife’s Mac:

1. Go to **System Settings → Privacy & Security**
2. Enable for TeamViewer:

   * **Screen Recording**
   * **Accessibility**
3. Restart TeamViewer after enabling

⚠️ If you skip this, you may connect but **can’t control the mouse/keyboard**.

---

## 5. Optional: Set up unattended access (no need to ask each time)

If you want to access her Mac anytime:

On your wife’s Mac:

* In TeamViewer:

  * Go to **Settings → Security**
  * Set a **personal password**
  * Enable **Start TeamViewer with system**

Now you can connect anytime using:

* Her ID
* The fixed password

---

## 6. Tips for smoother use

* Use **good internet** on both sides
* Enable **Optimize speed** in settings if laggy
* Use **Voice call inside TeamViewer** or another app to communicate

---

## Alternative (built-in Mac option)

If you don’t want third-party tools:

* Use **Screen Sharing (VNC)** via Apple ID or local network
* But it’s harder across different networks compared to TeamViewer

---

## Common problems

* **Black screen** → Screen Recording permission not enabled
* **Can’t control mouse** → Accessibility not enabled
* **Connection failed** → firewall or wrong ID/password

---

If you want, I can also show you:

* A faster setup using **Chrome Remote Desktop**
* Or a **one-click unattended setup workflow** (best for family tech support)
