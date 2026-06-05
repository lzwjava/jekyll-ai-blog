---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ways to Refresh Tailscale IP Address
translated: false
type: note
---

Question: How can I refresh or change a Tailscale IP address?

Answer:

Tailscale IP addresses are typically stable within a network, but you **can force a change** by reassigning or renewing the IP. Here are ways to do it:

1. **Restart the Tailscale service**

   * On most systems, this will re-register the device with Tailscale and sometimes assign a new IP if the previous one is freed.
   * Commands:

     * **Linux/macOS:**

       ```bash
       sudo tailscale down
       sudo tailscale up
       ```
     * **Windows (PowerShell as admin):**

       ```powershell
       tailscale down
       tailscale up
       ```

2. **Remove and re-add the device**

   * Go to the **Tailscale Admin Console** → Devices → select your device → **Delete**.
   * Then reconnect your device using `tailscale up`.
   * This will guarantee a new Tailscale IP.

3. **Switch to a different subnet / exit node** (optional)

   * If your Tailscale IP is part of a routed subnet, changing the exit node or subnet router can sometimes give a new IP within that range.

4. **Use ephemeral IPs (for advanced setups)**

   * Tailscale can assign ephemeral addresses in some enterprise configurations, but for most home users, removing and re-adding the device is the simplest approach.

**Summary:** The easiest way for a home server is to **stop Tailscale and start it again**, or **remove the device from the admin console and reconnect it**.

References:

* [Tailscale Admin Console](https://login.tailscale.com/admin)
* [Tailscale CLI Guide](https://tailscale.com/kb/1100/cli/)

If you want, I can explain a **trick to force Tailscale to immediately give a completely new IP** without waiting for lease expiry. Do you want me to show that?
