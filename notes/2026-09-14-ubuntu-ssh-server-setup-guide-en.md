---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ubuntu SSH Server Setup Guide
translated: false
type: note
---

**Question:** How do I set up and start an SSH server on Ubuntu?

**Answer:**

Here are the steps to install and enable an SSH server on Ubuntu:

**1. Install OpenSSH Server**
```bash
sudo apt update
sudo apt install openssh-server -y
```

**2. Start and Enable the SSH Service**
```bash
sudo systemctl start ssh
sudo systemctl enable ssh   # Auto-start on boot
```

**3. Check the Service Status**
```bash
sudo systemctl status ssh
```
You should see `active (running)` in the output.

**4. Allow SSH Through the Firewall (UFW)**
```bash
sudo ufw allow ssh
sudo ufw enable        # If UFW is not already enabled
sudo ufw status        # Verify the rule
```

**5. Find Your IP Address (for clients to connect)**
```bash
ip a
# or
hostname -I
```

**6. Connect from Another Machine**
```bash
ssh username@your-server-ip
```

---

**Optional: Basic SSH Configuration**

Edit the config file at `/etc/ssh/sshd_config` to customize settings (e.g., change port, disable root login):
```bash
sudo nano /etc/ssh/sshd_config
```

After any config change, restart SSH:
```bash
sudo systemctl restart ssh
```

---

**References:**
- [Ubuntu SSH Server Documentation](https://ubuntu.com/server/docs/service-openssh)
- [OpenSSH Manual](https://www.openssh.com/manual.html)
- [UFW Firewall Guide](https://help.ubuntu.com/community/UFW)