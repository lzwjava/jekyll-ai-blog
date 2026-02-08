---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Check SSH Status on Ubuntu
translated: false
type: note
---

**Question:** How can I check whether the SSH service is running/open on my Ubuntu system?

**Answer:**

Here are the most reliable and commonly used ways to check if SSH (usually OpenSSH server) is running and listening on your Ubuntu machine (2024–2026 editions):

### Quickest & Recommended Methods

1. **Check service status (most recommended)**  
```bash
sudo systemctl status ssh
```
or
```bash
systemctl status ssh
```

Look for these key lines:
- `Active: active (running)` → SSH is **running**
- `Active: inactive (dead)` → SSH is **stopped**
- `Active: failed` → SSH failed to start (look at the error below)

Alias note: on Ubuntu the service is usually called `ssh` (not `sshd`)

2. **Even shorter – just check if it's active**
```bash
systemctl is-active ssh
```
Output:
- `active`   → running
- `inactive` → stopped
- `failed`   → crashed

3. **Check if SSH port is listening (very reliable)**
```bash
# Most popular & clean way (recommended)
ss -tuln | grep :22

# Alternative commands (all work)
sudo netstat -tuln | grep :22
sudo lsof -i :22
sudo ss -tuln  | grep ':22.*LISTEN'
```

If you see output similar to this → SSH **is listening**:
```
tcp   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*
# or
tcp   LISTEN 0      128             [::]:22           [::]:*
```

No output → SSH is **not listening** (either not installed or not running)

### One-line "am I reachable via SSH right now?" checks

```bash
# Method A - very clear
sudo systemctl is-active --quiet ssh && echo "SSH is RUNNING" || echo "SSH is STOPPED"

# Method B - port check style
ss -tuln | grep -q ':22 ' && echo "Port 22 is OPEN" || echo "Port 22 is CLOSED"
```

### Summary – fastest commands to remember

Command                              | What it tells you                  | Recommendation
-------------------------------------|------------------------------------|---------------
`systemctl is-active ssh`           | Running or not                     | ★★★ best daily check
`ss -tuln \| grep :22`              | Actually listening on port 22      | ★★★ very trustworthy
`sudo systemctl status ssh`         | Full status + recent logs          | Best when something is wrong

### Bonus – If you want to see from outside

Run this **from another computer**:

```bash
# Replace 192.168.1.100 with your Ubuntu machine's IP
nc -zv 192.168.1.100 22
```

Output:
- `succeeded!` → SSH port is open and reachable
- `Connection refused` / timeout → SSH is off, firewalled, or network issue

Pick whichever style you like most — most Ubuntu users just use:

```bash
systemctl is-active ssh && ss -tuln | grep -q :22 && echo "SSH looks good ✓" || echo "SSH has problem ✗"
```

**References:**

- None needed (standard Ubuntu commands, valid in 2024–2026)