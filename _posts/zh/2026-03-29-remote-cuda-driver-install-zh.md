---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 远程 CUDA 驱动程序安装指南
translated: true
type: note
---

### 📋 Review: CUDA Driver Installation on Remote Server

---

**Step 1 — Connect & discover hardware**

通过 SSH 连接到 `root@47.107.70.224`，运行了 `lscpu`, `free`, `lspci`, `nvidia-smi`。发现了 2× RTX 3090 但未加载 Driver。关键点：即使 `nvidia-smi` 无法识别时，`lspci` 仍能在 PCIe 层面显示 GPU（这是一种独立于 Driver 的检查方式）。

**Step 2 — Set up passwordless SSH**

使用 `sshpass` 将本地 ed25519 公钥复制到远程服务器的 `~/.ssh/authorized_keys`。这使我能够链式执行多个命令而无需重复验证。通过 `ssh -o BatchMode=yes` 进行了验证。

**Step 3 — Check available drivers**

在远程服务器上运行 `apt update && ubuntu-drivers devices`。该命令查询 Ubuntu 的 Driver 数据库并列出兼容的 NVIDIA Driver。推荐版本为 `nvidia-driver-580-open`。最终选择了 `nvidia-driver-580`（非 Open 版本，Proprietary —— 具有更好的 CUDA 兼容性）。

**Step 4 — Install NVIDIA driver**

```bash
DEBIAN_FRONTEND=noninteractive apt install -y nvidia-driver-580 nvidia-utils-580
```

- `DEBIAN_FRONTEND=noninteractive` — 抑制所有交互式提示（对于远程/Headless 安装至关重要）
- `nvidia-driver-580` — Kernel Module + User-space Libraries
- `nvidia-utils-580` — 包括 `nvidia-smi` 在内的 CLI 工具
- 通过 `nvidia-smi` 验证 → 双 GPU 可见，Driver 版本 580.126.09，CUDA 13.0 Runtime

**Step 5 — Install CUDA toolkit (the messy part)**

第一次尝试：`apt install cuda-toolkit-12-8` —— **失败**，Package 不在默认的 Ubuntu Repos 中。

通过添加 NVIDIA 官方 Repo 解决：

```bash
wget cuda-keyring_1.1-1_all.deb   # 设置 NVIDIA 的 apt source + GPG key
dpkg -i cuda-keyring_1.1-1_all.deb
apt update
apt install cuda-toolkit-12-8
```

第二次尝试：SSH 连接 **在安装过程中中断**（Exit Code 255 = Connection Killed）。通过 SSH 运行耗时较长的 apt 任务是有风险的。

第三次尝试：使用 `nohup` 在远程后台执行安装：

```bash
nohup apt install -y cuda-toolkit-12-8 > /tmp/cuda-install.log 2>&1 &
```

但遇到了 **Lock Conflict** —— 之前因 SSH 中断而残留的 apt 进程（PID 23704）仍在运行。重复的进程会一直等待 `/var/lib/dpkg/lock-frontend` 释放。

修复：杀掉了重复进程，等待原始 apt 进程结束后，通过 `dpkg -l cuda-toolkit-12-8` 确认安装完成。

**Step 6 — Configure PATH**

CUDA 安装在 `/usr/local/cuda-12.8/bin`，默认不在 PATH 中。将其添加到 `~/.bashrc`：

```bash
export PATH=/usr/local/cuda-12.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:$LD_LIBRARY_PATH
```

---

### 🤔 What went wrong / what I'd do differently

| Issue | Root cause | Better approach |
| ------- | ----------- | ----------------- |
| CUDA package not found | 尝试从 Ubuntu Repos 安装，而非 NVIDIA 官网 Repo | 应该先添加 `cuda-keyring` |
| SSH dropped during install | 通过 SSH 运行长耗时 apt 任务导致连接断开 | 对任何超过 30 秒的安装，**从一开始**就使用 `nohup` 或 `tmux`/`screen` |
| Lock conflict | 两个 apt 实例同时运行 | 在重试前杀掉陈旧进程，或使用 `flock` |
| `nvcc` not found in non-interactive shell | `.bashrc` 在非交互式 SSH Session 中不会被加载 | 在脚本中使用显式的 `export PATH=...`，或添加到 `/etc/environment` |

### ✅ What went well

- 使用 `sshpass` 进行脚本化密码认证 —— 快速且无需手动交互
- 在 SSH 中断后通过 `nohup` 技巧挽救了安装过程 —— 良好的恢复处理
- 开头设置的单 SSH Key 为后续每个命令都带来了便利
- 在 `nvidia-smi` 失效时使用 `lspci` 作为备选 —— 尽早确认了 GPU 的存在

**TL;DR:** 应该从一开始就使用 `nohup`/`tmux` 来安装 CUDA，并应在安装前先添加 NVIDIA Repo。其余过程顺利。教训：**永远不要在没有 Session Wrapper 的情况下通过原始 SSH 运行长耗时的 apt 安装任务。**
