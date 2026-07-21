---
audio: false
generated: true
image: false
lang: en
layout: post
title: Verify sshd Running After Install
translated: false
type: note
---

**Question: How to verify `sshd` is running after installing OpenSSH server?**

Answer:

On Ubuntu/Debian, check the SSH service status:

```bash
sudo systemctl status ssh
```

Expected output:

```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded
     Active: active (running)
```

For a quick check:

```bash
systemctl is-active ssh
```

Output:

```
active
```

---

Check whether `sshd` is listening on a port:

```bash
sudo ss -tlnp | grep ssh
```

Example:

```
LISTEN 0 128 0.0.0.0:22 0.0.0.0:* users:(("sshd",pid=1234,fd=3))
LISTEN 0 128 [::]:22    [::]:*    users:(("sshd",pid=1234,fd=4))
```

This means SSH daemon is accepting connections on port 22.

---

Check the process directly:

```bash
ps aux | grep sshd
```

Example:

```
root  1234  0.0  sshd: /usr/sbin/sshd -D
```

---

If you manually created `/run/sshd` and ran `which sshd`, you only verified the binary exists:

```bash
which sshd
# /usr/sbin/sshd
```

You still need to start the daemon:

```bash
sudo systemctl start ssh
```

Enable on boot:

```bash
sudo systemctl enable ssh
```

---

For a container/cloud VM environment (common for GPU instances), `systemctl` may not exist. Use:

```bash
sudo /usr/sbin/sshd -t   # validate config
sudo /usr/sbin/sshd      # start sshd
```

Then:

```bash
ps aux | grep sshd
ss -tlnp | grep :22
```

---

To test from another machine:

```bash
ssh username@server_ip
```

or:

```bash
ssh -v username@server_ip
```

`-v` shows the connection handshake and is usually the fastest way to debug SSH issues.
