---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remote CUDA Driver Installation Guide
translated: false
type: note
---

### 📋 Review: CUDA Driver Installation on Remote Server

---

**Step 1 — Connect & discover hardware**

SSH'd to `root@47.107.70.224`, ran `lscpu`, `free`, `lspci`, `nvidia-smi`. Found 2× RTX 3090 but no driver loaded. Key insight: `lspci` showed the GPUs at PCIe level even when `nvidia-smi` couldn't see them (driver-independent check).

**Step 2 — Set up passwordless SSH**

Used `sshpass` to copy the local ed25519 public key to `~/.ssh/authorized_keys` on the remote. This let me chain multiple commands without re-authenticating. Verified with `ssh -o BatchMode=yes`.

**Step 3 — Check available drivers**

Ran `apt update && ubuntu-drivers devices` on the remote. This queries Ubuntu's driver database and lists compatible NVIDIA drivers. The recommended one was `nvidia-driver-580-open`. Chose `nvidia-driver-580` (non-open, proprietary — better CUDA compatibility).

**Step 4 — Install NVIDIA driver**

```bash
DEBIAN_FRONTEND=noninteractive apt install -y nvidia-driver-580 nvidia-utils-580
```

- `DEBIAN_FRONTEND=noninteractive` — suppresses all interactive prompts (critical for remote/headless installs)
- `nvidia-driver-580` — the kernel module + userspace libraries
- `nvidia-utils-580` — CLI tools including `nvidia-smi`
- Verified with `nvidia-smi` → both GPUs visible, driver 580.126.09, CUDA 13.0 runtime

**Step 5 — Install CUDA toolkit (the messy part)**

First attempt: `apt install cuda-toolkit-12-8` — **failed**, package not in default Ubuntu repos.

Fixed by adding NVIDIA's official repo:

```bash
wget cuda-keyring_1.1-1_all.deb   # Sets up NVIDIA's apt source + GPG key
dpkg -i cuda-keyring_1.1-1_all.deb
apt update
apt install cuda-toolkit-12-8
```

Second attempt: SSH connection **dropped mid-install** (exit code 255 = connection killed). Long-running apt over SSH is risky.

Third attempt: Used `nohup` to background the install on the remote:

```bash
nohup apt install -y cuda-toolkit-12-8 > /tmp/cuda-install.log 2>&1 &
```

But hit a **lock conflict** — the earlier apt process (PID 23704) was still alive from the dropped SSH session. The duplicate waited on `/var/lib/dpkg/lock-frontend` forever.

Fix: Killed the duplicate, waited for the original apt to finish, confirmed with `dpkg -l cuda-toolkit-12-8`.

**Step 6 — Configure PATH**

CUDA installs to `/usr/local/cuda-12.8/bin` which isn't in PATH by default. Added to `~/.bashrc`:

```bash
export PATH=/usr/local/cuda-12.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:$LD_LIBRARY_PATH
```

---

### 🤔 What went wrong / what I'd do differently

| Issue | Root cause | Better approach |
|-------|-----------|-----------------|
| CUDA package not found | Tried installing from Ubuntu repos, not NVIDIA's | Should've added `cuda-keyring` first |
| SSH dropped during install | Long-running apt over SSH killed the connection | Use `nohup` or `tmux`/`screen` **from the start** for any install > 30s |
| Lock conflict | Two apt instances running simultaneously | Kill stale processes before retrying, or use `flock` |
| `nvcc` not found in non-interactive shell | `.bashrc` isn't sourced in non-interactive SSH sessions | Use explicit `export PATH=...` in scripts, or add to `/etc/environment` |

### ✅ What went well

- `sshpass` for scripted password auth — fast, no manual interaction
- `nohup` trick saved the install after SSH dropped — good recovery
- Single SSH key setup at the start paid off for every subsequent command
- `lspci` as fallback when `nvidia-smi` failed — caught the GPUs early

**TL;DR:** Should've used `nohup`/`tmux` from the start for the CUDA install, and should've added NVIDIA's repo before trying to install. The rest was smooth. Lesson learned: **never run long apt installs over raw SSH without a session wrapper.**
