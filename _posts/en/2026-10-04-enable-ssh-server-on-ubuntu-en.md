---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enable SSH Server on Ubuntu
translated: false
type: note
---

Question: How do I enable and start an SSH server on Ubuntu?

Answer:

1. **Install OpenSSH server**
   ```bash
   sudo apt update
   sudo apt install openssh-server
   ```

2. **Start the service and enable it at boot**
   ```bash
   sudo systemctl enable --now ssh
   ```

3. **Check that it is running**
   ```bash
   sudo systemctl status ssh
   ```
   You should see `active (running)`.

4. **Allow SSH through the firewall (if UFW is enabled)**
   ```bash
   sudo ufw allow ssh
   sudo ufw status
   ```

5. **Find your IP address**
   ```bash
   ip a
   ```

6. **Connect from another machine**
   ```bash
   ssh username@your_server_ip
   ```

**Useful commands**
- Restart after config changes: `sudo systemctl restart ssh`
- Stop the service: `sudo systemctl stop ssh`
- Config file: `/etc/ssh/sshd_config`

**Security tips**
- Use SSH key authentication and set `PasswordAuthentication no` in `sshd_config` once keys work.
- Set `PermitRootLogin no` to block direct root login.
- Optionally change the default port (22) and update the firewall rule to match.

References:
- [Ubuntu Server docs: OpenSSH server](https://documentation.ubuntu.com/server/how-to/security/openssh-server/)
- [Ubuntu Community Help Wiki: SSH](https://help.ubuntu.com/community/SSH)
