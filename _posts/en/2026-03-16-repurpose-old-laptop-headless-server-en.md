---
audio: false
generated: true
image: false
lang: en
layout: post
title: Repurpose Old Laptop as Headless Server
translated: false
type: note
---

**Question:** Can I install Ubuntu Server on an old laptop, and then use it entirely via SSH — even if the keyboard or screen is broken — to utilize its CPU and memory for lightweight deployments?

**Answer:**

## Yes — Absolutely! This Is a Classic "Headless Server" Setup

Your idea is completely valid and widely practiced. Installing **Ubuntu Server** on an old laptop and managing it entirely via **SSH** is called a **headless server** setup. You never need to touch the laptop's keyboard or screen again after initial setup.

---

## Step 1: Choose the Right OS

Because a headless server does not need to render graphical elements, you can use Ubuntu Server 24.04 LTS and allocate minimal resources — bypassing the GUI entirely saves significant RAM and CPU.

**Recommended options:**

- **Ubuntu Server 24.04 LTS** — best documentation, most community support, beginner-friendly
- **Debian 12** — even lighter, very stable
- **DietPi** — requires only 512 MB of RAM, consuming the least resources so you can divert all processing power to server-oriented tasks

---

## Step 2: Install Ubuntu Server (With or Without Screen)

Ubuntu Server supports several methods for headless installation, ranging from serial console access to fully automated installs that require no interaction at all.

**If you still have a screen for first-time setup (recommended approach):**

1. Download **Ubuntu Server ISO** (not Ubuntu Desktop)
2. Flash it to a USB drive using Rufus or Balena Etcher
3. Boot the laptop from USB, follow the text installer
4. **Critically: select "Install OpenSSH Server"** during installation
5. Configure a static IP during the networking setup — this is necessary to facilitate management and control of the device.

**If you have NO screen at all (fully headless):**

Using Ubuntu's Autoinstall feature, the machine installs itself without any prompts — you embed a `user-data` YAML config file into the ISO that specifies hostname, username, password hash, SSH keys, and network settings.

---

## Step 3: Enable and Connect via SSH

After installation, from any other computer on the same network:

```bash
ssh username@<laptop-ip-address>
```

For better security, disable password authentication and use SSH key-based login instead. Generate a key on your client machine with `ssh-keygen -t ed25519`, then copy it to the server with `ssh-copy-id`.

Also enable the firewall and allow SSH:

```bash
sudo ufw allow ssh
sudo ufw enable
```

---

## Step 4: Handle the Laptop Lid Problem

One key challenge is the laptop's tendency to enter sleep mode when the lid is closed. To fix this, edit `/etc/systemd/logind.conf`, change `HandleLidSwitch=suspend` to `HandleLidSwitch=ignore`, and restart the service with `sudo service systemd-logind restart`.

Also check your BIOS: some computers have BIOS/UEFI configurations which stop the boot process if there's no keyboard or display plugged in — go through BIOS settings and disable that feature.

---

## Step 5: What Lightweight Services Can You Deploy?

A home server on an old laptop can run: a NAS for file storage, network-wide ad blocking with AdGuard, a media server with Jellyfin, and more — multiple services running smoothly.

Popular lightweight deployments via **Docker** (highly recommended):

| Service | Purpose |
|---|---|
| **Nginx / Caddy** | Web server / reverse proxy |
| **Pi-hole / AdGuard Home** | Network-wide ad blocker |
| **Jellyfin** | Media server |
| **Nextcloud** | Personal cloud storage |
| **Portainer** | Docker web UI |
| **Gitea** | Self-hosted Git |
| **Home Assistant** | Smart home automation |
| **Uptime Kuma** | Service monitoring |

With Ubuntu Server installed, Docker is a great starting point — it runs containers in a sandboxed environment and is great for self-hosting a wide variety of services.

---

## Bonus: Assign a Static IP via Your Router

Assign a **DHCP reservation** in your router settings (using the laptop's MAC address). This ensures the laptop always gets the same IP, so your SSH command never changes — even after reboots.

---

## Summary Checklist

1. ✅ Download Ubuntu Server 24.04 LTS ISO
2. ✅ Flash to USB, boot and install — check "OpenSSH Server" during install
3. ✅ Set static IP (router reservation or manual netplan config)
4. ✅ Disable lid-close suspend in `logind.conf`
5. ✅ SSH in from any device: `ssh user@<ip>`
6. ✅ Install Docker: `sudo apt install docker.io docker-compose`
7. ✅ Deploy lightweight services as needed

---

**References:**

- [Deploying a Headless Ubuntu Server (Medium)](https://medium.com/@pacegaming/deploying-a-headless-ubuntu-server-fe4ffa0bf8e1)
- [How to Install Ubuntu Server Without a Monitor](https://oneuptime.com/blog/post/2026-03-02-install-ubuntu-server-without-monitor-headless/view)
- [Transforming an Old Laptop into Ubuntu Server Homelab](https://medium.com/@azhar9/transforming-an-old-asus-laptop-into-a-ubuntu-server-for-my-homelab-setup-e3c99f076080)
- [Building My Home Server from an Old Laptop (DEV Community)](https://dev.to/strikeraryu/building-my-home-server-from-an-old-laptop-4b39)
- [New Life for an Old Laptop as a Linux Home Server](https://medium.com/@rghv064/new-life-for-an-old-laptop-as-a-linux-home-server-8e4557d5cc8c)
- [Setting Up a Headless Linux Server (LinkedIn)](https://www.linkedin.com/pulse/setting-up-headless-linux-server-jose-chapa)
