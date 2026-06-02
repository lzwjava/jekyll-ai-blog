---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: "Securing SSH: Root Login Best Practices"
translated: false
type: note
---

**Question:** How to remove an SSH root key (from authorized_keys), and what does "PermitRootLogin" mean? What are the benefits of disabling root login via SSH?

**Answer:**

There are two related but different things here:

1. **Removing a specific SSH public key** for the root user (so root can no longer log in with that particular key).
2. **Disabling root login completely** (or restricting it) via the `PermitRootLogin` setting in SSH — this is usually what people mean when they say "remove SSH root login" or "disable root SSH access".

### 1. How to remove a specific SSH public key for root

The public keys that allow login are stored in:

```
/root/.ssh/authorized_keys
```

(or sometimes `/root/.ssh/authorized_keys2` on very old systems)

**Steps to remove one key:**

- SSH into the server as root or with a sudo-capable user
- Open the file:

```bash
sudo nano /root/.ssh/authorized_keys
# or
sudo vim /root/.ssh/authorized_keys
```

- Find the line that starts with `ssh-rsa` or `ecdsa-sha2-nistp256` or `ssh-ed25519` → that is one public key
- Delete the entire line corresponding to the key you want to remove
- Save and exit

**Faster command-line way** (if you know part of the key):

```bash
# Example: remove key containing "AAAAB3NzaC1yc2EAAAADAQABAAABAQ..."
sudo sed -i '/AAAAB3NzaC1yc2EAAAADAQABAAABAQ/d' /root/.ssh/authorized_keys
```

**To remove all keys** (completely stop key-based root login):

```bash
sudo mv /root/.ssh/authorized_keys /root/.ssh/authorized_keys.bak
# or just delete it
sudo rm /root/.ssh/authorized_keys
```

After any change to authorized_keys, you usually **do not** need to restart sshd.

### 2. What is `PermitRootLogin` and how to disable root login

This setting is in `/etc/ssh/sshd_config` (or `/etc/ssh/sshd_config.d/` files on modern systems).

Common values:

- `yes` → root can login with password **or** key (very insecure)
- `prohibit-password` (or old name: `without-password`) → root can login **only** with key, **not** with password
- `forced-commands-only` → root login only with key + forced command (rarely used)
- `no` → root cannot login at all via SSH (recommended for security)

**Recommended secure setting (most servers):**

```bash
sudo nano /etc/ssh/sshd_config
```

Change or add:

```
PermitRootLogin no
```

Then restart SSH:

```bash
# Ubuntu/Debian
sudo systemctl restart ssh

# CentOS/RHEL/AlmaLinux/Rocky
sudo systemctl restart sshd
```

After this change:

- Nobody can `ssh root@server`
- You must first `ssh normaluser@server` → then `sudo -i` or `sudo su -` to become root

### Benefits of disabling root login via SSH (`PermitRootLogin no`)

- **Stops most brute-force attacks** — bots usually only try username "root" + common passwords
- **Makes attacks much slower/harder** — attacker needs valid normal user + password/key **+** then escalate to root (two steps instead of one)
- **Better audit logging** — when using `sudo`, logs show who ran which command (e.g. "user zhiwei ran rm -rf /")
- **Easier to revoke access** — just disable/lock one normal user account instead of changing root password everywhere
- **Follows security best practices** — used by almost every cloud provider (AWS, GCP, DigitalOcean, etc.) and security standards (CIS benchmarks)

**Quick summary — what most secure servers do today:**

- `PermitRootLogin no`
- `PasswordAuthentication no` (only allow key-based login)
- Use a normal user with sudo privileges
- Use strong SSH keys (ed25519 preferred)

This combination stops ~99% of automated SSH attacks.

**References:**

- [https://man7.org/linux/man-pages/man5/sshd_config.5.html](https://man7.org/linux/man-pages/man5/sshd_config.5.html)
- [https://www.baeldung.com/linux/root-login-over-ssh-disable](https://www.baeldung.com/linux/root-login-over-ssh-disable)
- [https://security.stackexchange.com/questions/34915/what-is-the-actual-value-of-disabling-remote-root-login-using-ssh](https://security.stackexchange.com/questions/34915/what-is-the-actual-value-of-disabling-remote-root-login-using-ssh)
