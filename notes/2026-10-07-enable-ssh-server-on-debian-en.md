---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enable SSH Server on Debian
translated: false
type: note
---

Question: How to enable SSH server on Debian?

Answer:

On Debian, install and start the OpenSSH server:

```bash
sudo apt update
sudo apt install openssh-server
```

Check status:

```bash
sudo systemctl status ssh
```

If it is not running:

```bash
sudo systemctl start ssh
```

Enable it at boot:

```bash
sudo systemctl enable ssh
```

Check listening port:

```bash
ss -tlnp | grep ssh
```

Default SSH port is **22**.

From another machine, connect:

```bash
ssh username@debian_ip_address
```

Find Debian's IP:

```bash
ip addr
```

Example:

```bash
ssh lzw@192.168.1.100
```

### If firewall is enabled

For `ufw`:

```bash
sudo ufw allow ssh
```

or:

```bash
sudo ufw allow 22/tcp
```

### Useful configuration

Edit SSH server config:

```bash
sudo nano /etc/ssh/sshd_config
```

Common changes:

```text
Port 22
PermitRootLogin no
PasswordAuthentication yes
```

Restart after changes:

```bash
sudo systemctl restart ssh
```

### For AI/GPU machines (common setup)

Usually you want:

```bash
sudo apt install openssh-server tmux htop nvtop
sudo systemctl enable --now ssh
```

Then you can SSH into the Debian box and leave long PyTorch/LLM training jobs running with `tmux`:

```bash
tmux new -s train
python train.py
```

Detach:

```
Ctrl+B then D
```

Reconnect later:

```bash
tmux attach -t train
```

This is the typical workflow for remote GPU servers.
