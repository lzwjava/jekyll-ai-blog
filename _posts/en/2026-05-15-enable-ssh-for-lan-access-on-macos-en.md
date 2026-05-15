---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enable SSH for LAN Access on macOS
translated: false
type: note
---

Question: How do you enable SSH on macOS to log in over a local area network (LAN)?

Answer:

To access your Mac via SSH over a LAN, you need to enable the SSH server (called **Remote Login** on macOS) and then connect from another device. Here's a step-by-step guide:

---

### 1. Enable SSH on macOS

1. Open **System Settings** (or **System Preferences** depending on macOS version).
2. Go to **Sharing**.
3. Find and **check “Remote Login”**.

   * This automatically starts the SSH server.
   * You can choose to allow access for:

     * **All users** – any user account on your Mac.
     * **Only these users** – specify which accounts can log in.
4. Note the message at the top like:

   ```
   To log in to this computer remotely, type "ssh username@192.168.x.x"
   ```

   * Here, `username` is your Mac account name, and `192.168.x.x` is your Mac’s local IP address.

---

### 2. Find Your Mac’s Local IP

1. Go to **System Settings > Network**.
2. Select your active network (Wi-Fi or Ethernet).
3. Note the **IP address** (e.g., `192.168.1.25`).

---

### 3. Connect from Another Device on LAN

1. On another computer (Windows, Linux, or Mac) on the same LAN, open a terminal (or PowerShell on Windows with OpenSSH installed).

2. Run:

   ```bash
   ssh username@192.168.x.x
   ```

   Replace `username` with your Mac user and `192.168.x.x` with the IP address from step 2.

3. Accept the fingerprint prompt the first time.

4. Enter your Mac password when prompted.

---

### 4. Optional: Set a Static IP or Use Hostnames

* For convenience, consider setting a **static LAN IP** on your Mac so it doesn’t change.
* Or use a local hostname (e.g., `ssh username@macbook.local`) if Bonjour is enabled.

---

### 5. Troubleshooting

* Make sure **firewall** allows incoming SSH connections:
  **System Settings > Network > Firewall Options**, allow **Remote Login**.
* Ensure both devices are on the **same LAN/subnet**.
* Test with `ping <Mac_IP>` first to verify connectivity.

---

This setup lets you securely log in to your Mac from any device on your local network.

References:

* [Apple Support – Share files and screen on Mac](https://support.apple.com/guide/mac-help/share-files-and-screen-on-mac-mchlp2586/mac)
* [macOS SSH Access Guide](https://www.ssh.com/ssh/mac/)

---

If you want, I can also show a **one-line Terminal command method** to enable SSH without using System Settings. It’s faster for advanced users. Do you want me to?