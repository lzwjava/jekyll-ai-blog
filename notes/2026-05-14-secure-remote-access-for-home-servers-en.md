---
audio: false
generated: true
image: false
lang: en
layout: post
title: Secure Remote Access for Home Servers
translated: false
type: note
---

Question: How can I use Tailscale or other solutions on Linux to let a friend connect to my home server in Guangzhou, China?

Answer:

You can securely allow remote access to a home server in a big city like Guangzhou using Tailscale or other VPN/remote-access solutions. Here’s a detailed guide:

---

### **1. Using Tailscale on Linux**

Tailscale is a zero-configuration VPN based on WireGuard. It creates a secure network between your devices.

**Steps:**

1. **Install Tailscale on Linux**

   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo tailscale up
   ```

   * This will open a URL to authenticate with your Tailscale account (Google, GitHub, Microsoft, or email-based login).

2. **Check Tailscale status**

   ```bash
   tailscale status
   ```

   * You should see your device listed with a Tailscale IP (usually `100.x.x.x`).

3. **Share access with your friend**

   * Go to [Tailscale admin console](https://login.tailscale.com/admin/machines) in your browser.
   * Share access by adding your friend’s email to your Tailscale network. They install Tailscale on their device and authenticate.
   * They will get a private Tailscale IP to access your server.

4. **Connect to the server**

   * On your friend’s machine:

     ```bash
     ssh user@100.x.x.x   # Use your server’s Tailscale IP
     ```

   * Or access any service you expose (web server, media server) via the Tailscale IP.

**Notes:**

* Works even behind NAT and restrictive ISPs (common in China).
* End-to-end encrypted, no port forwarding needed.
* Free tier is sufficient for small networks; for more devices, consider the paid tier.

---

### **2. Alternative Options**

#### **A. WireGuard Directly**

* Tailscale uses WireGuard under the hood, but you can configure WireGuard manually.
* Requires:

  * Generating keys for server and client.
  * Configuring `wg0.conf` on both devices.
  * Port forwarding on your router if needed.
* More flexible but more technical and less convenient than Tailscale.

#### **B. Ngrok / Cloudflare Tunnel**

* Useful if your friend only needs access to a specific service (web, SSH, etc.).
* Example with SSH:

  ```bash
  ssh -R 2222:localhost:22 user@remote-ngrok-server
  ```

* Pros:

  * No VPN setup.
  * Easy to use even with CGNAT or strict ISP.
* Cons:

  * May require paid plan for persistent tunnels.
  * Not full network access.

#### **C. ZeroTier**

* Another VPN solution similar to Tailscale.
* Works behind NAT, peer-to-peer connections.
* Free for up to 50 devices.
* Requires creating a network at [ZeroTier](https://www.zerotier.com) and installing their client.

---

### **3. Practical Advice for China**

* Tailscale and ZeroTier generally work in China, but some ISPs may block or throttle WireGuard-based traffic.
* Using Cloudflare Tunnel or VPS-based relay can help bypass strict NAT or firewall limitations.
* If speed matters (like gaming or large file transfer), Tailscale on a wired broadband home server works best.

---

If you want, I can write a **step-by-step example of a complete setup in Guangzhou** with Linux server, Tailscale, and friend access—including SSH and web services—so your friend can connect immediately.

Do you want me to do that?
