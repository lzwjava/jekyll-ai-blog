---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Wake Ubuntu Remotely Without Power
translated: false
type: note
---

Question: What are solutions for remote access to Ubuntu without keeping the PC always on?

Answer: 

To remotely access your Ubuntu PC from your MacBook Air M2 without keeping the Ubuntu machine powered on all the time (to save electricity), the key challenge is waking it up on demand while ensuring secure connectivity. This typically involves combining Wake-on-LAN (WoL) with remote access protocols like SSH, RDP, or VNC. WoL allows you to send a "magic packet" over the network to power on the PC from a sleep or shutdown state, but it requires the PC's motherboard to support it (most modern ones do) and proper configuration.

Below, I'll outline comprehensive, step-by-step solutions based on reliable methods. These assume your Ubuntu PC is on the same home network initially for setup, and you're accessing it remotely (e.g., from outside via the internet). For external access, you'll need to handle port forwarding, a VPN, or a third-party service to securely reach your home network. Always prioritize security by using strong passwords, firewalls, and avoiding unnecessary port exposures.

### 1. **Wake-on-LAN (WoL) Combined with SSH for Command-Line Access**
   This is the most lightweight and electricity-efficient option since SSH is text-based and doesn't require a graphical session. It's ideal if you mainly need terminal access to run commands or scripts on Ubuntu.

   **Step-by-Step Setup:**
   - **Enable WoL on the Ubuntu PC:**
     1. Boot into BIOS/UEFI (usually by pressing Del, F2, or F10 during startup) and enable "Wake-on-LAN" or "PCIe/PCI Wake" under power management settings. Save and exit.
     2. On Ubuntu, install the ethtool package: `sudo apt update && sudo apt install ethtool`.
     3. Identify your network interface (e.g., enp0s3): `ip link show`.
     4. Enable WoL: `sudo ethtool -s <interface> wol g` (replace <interface> with yours, like enp0s3).
     5. Make it persistent: Create a script or use systemd. For example, edit `/etc/network/interfaces` or create a service file in `/etc/systemd/system/` with `[Service] ExecStart=/usr/bin/ethtool -s enp0s3 wol g`.
     6. Test locally: Shut down the PC, then from another device on the same network, send a magic packet using tools like `wakeonlan` (install via `sudo apt install wakeonlan` on a test machine) with command: `wakeonlan <MAC address>`. Get the MAC with `ip link show`.
   - **Set Up SSH on Ubuntu:**
     1. Install OpenSSH server: `sudo apt install openssh-server`.
     2. Enable and start: `sudo systemctl enable --now ssh`.
     3. Configure firewall: `sudo ufw allow ssh`.
     4. For key-based authentication (more secure): Generate keys on your MacBook (`ssh-keygen`), copy to Ubuntu (`ssh-copy-id user@ubuntu-ip`).
   - **Remote Wake and Access:**
     - For remote WoL (from outside home), you can't send magic packets directly over the internet. Solutions:
       - Use a low-power always-on device like a Raspberry Pi (costs ~$35-50, low electricity use) as a "gateway." Set it up with SSH access via port forwarding or a VPN, then from your MacBook, SSH into the Pi and run the wakeonlan command to wake the Ubuntu PC.
       - Set up port forwarding on your router: Forward UDP port 9 (or custom) to your Ubuntu PC's broadcast address (e.g., 192.168.1.255). Then use a mobile app like "WoL - Wake on Lan" on your iPhone (since MacBook Air can connect via phone hotspot if needed) to send the packet remotely. Note: This exposes your network; use with caution.
       - Use a VPN like WireGuard (free and low-overhead): Install WireGuard on Ubuntu, your router (if supported, e.g., OpenWRT), and MacBook. Connect via VPN first, then send WoL packet as if on local network.
     - Once woken: From MacBook Terminal, connect with `ssh user@ubuntu-external-ip` (use dynamic DNS like No-IP for changing IPs).
   - **Pros:** Low resource use, secure for CLI. **Cons:** Requires initial wake-up step; graphical access needs additional tools like X forwarding (e.g., `ssh -X`).

### 2. **WoL with TeamViewer or Similar GUI Tools for Full Desktop Access**
   If you need graphical remote control (e.g., to use Ubuntu's desktop environment), use tools that integrate WoL.

   **Step-by-Step Setup with TeamViewer (Free for Personal Use):**
   - **Install on Ubuntu:**
     1. Download from official site: `wget https://download.teamviewer.com/download/linux/teamviewer_amd64.deb`.
     2. Install: `sudo dpkg -i teamviewer_amd64.deb` (fix dependencies with `sudo apt install -f`).
     3. Run and set up an account for unattended access.
   - **Enable WoL in TeamViewer:**
     1. In TeamViewer settings on Ubuntu, go to Extras > Options > General > Wake-on-LAN.
     2. Configure it to use "Public address" or another PC on the network (e.g., if you have a always-on device).
     3. Ensure BIOS WoL is enabled as in Method 1.
   - **Install on MacBook:**
     1. Download TeamViewer for macOS and log in with the same account.
   - **Remote Access:**
     - From MacBook, in TeamViewer, select the Ubuntu device (it shows as offline), and choose "Wake up."
     - Once awake, connect for full remote desktop control.
     - TeamViewer handles NAT/firewalls automatically, no port forwarding needed.
   - **Alternatives:**
     - **AnyDesk:** Similar to TeamViewer, supports WoL via configuration. Faster for some users.
     - **RustDesk with Tailscale:** Open-source and free. Install RustDesk on both machines, use Tailscale (a mesh VPN) for secure direct connections. For WoL, combine with a script or app to wake first (Tailscale keeps devices "connected" virtually).
   - **Pros:** Easy GUI, cross-platform, handles remote wake. **Cons:** Third-party service; potential privacy concerns (though end-to-end encrypted).

### 3. **Using RDP/VNC with Gnome Extensions for Locked Access**
   If you prefer native Ubuntu tools for graphical access, set up RDP or VNC, then wake with WoL.

   **Step-by-Step:**
   - **Enable Remote Desktop on Ubuntu (Ubuntu 22.04+):**
     1. Go to Settings > Sharing > Remote Desktop > Enable.
     2. Set username/password.
     3. For locked screen access: Install Gnome Extension Manager (`sudo apt install gnome-shell-extension-manager`), then add "Allow Locked Remote Desktop" extension.
   - **Client on MacBook:** Use Microsoft Remote Desktop app (free on App Store) for RDP.
   - **Wake with WoL:** As in Method 1, wake first, then connect.
   - **For VNC:** Install vino (`sudo apt install vino`), enable in settings, connect with Remmina or Vinagre on MacBook.
   - **Pros:** Built-in, no extra software. **Cons:** Less secure than SSH; needs wake step.

### Additional Tips
- **Power Management:** Configure Ubuntu to suspend after inactivity (`Settings > Power`), but ensure WoL works from suspend (test it).
- **Security:** Use VPN (e.g., WireGuard) for all remote access to avoid exposing ports. Enable Ubuntu firewall (`sudo ufw enable`).
- **Electricity Savings:** With WoL, the PC only runs when needed. A Raspberry Pi gateway uses ~3-5W vs. a PC's 50-100W idle.
- **Testing:** Start with local network tests before going remote.
- **If WoL Isn't Feasible:** Consider migrating to a cloud VM (e.g., AWS Lightsail with Ubuntu, ~$5/month), but this isn't using your local hardware.

These methods should allow comfortable access from your bed via MacBook while minimizing electricity use.

References:  

- [https://medium.com/@ryanym/cloud-is-not-free-wakeup-and-ssh-to-your-home-computer-remotely-7d4f3b37ce0](https://medium.com/@ryanym/cloud-is-not-free-wakeup-and-ssh-to-your-home-computer-remotely-7d4f3b37ce0)  
- [https://www.youtube.com/watch?v=pXXzWkNkKuQ](https://www.youtube.com/watch?v=pXXzWkNkKuQ)  
- [https://forums.lawrencesystems.com/t/different-ubuntu-remote-desktop-question/22472](https://forums.lawrencesystems.com/t/different-ubuntu-remote-desktop-question/22472)  
- [https://tailscale.com/blog/tailscale-rustdesk-remote-desktop-access](https://tailscale.com/blog/tailscale-rustdesk-remote-desktop-access)  
- [https://www.itpro.com/mobile/remote-access/368102/how-to-remote-desktop-into-ubuntu](https://www.itpro.com/mobile/remote-access/368102/how-to-remote-desktop-into-ubuntu)