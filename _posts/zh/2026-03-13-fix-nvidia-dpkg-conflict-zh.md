---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 快速修复 NVIDIA dpkg 文件冲突
translated: true
type: note
---

**问题：** 如何修复由 `nvidia-kernel-common-535` 和 `nvidia-firmware-535-535.288.01` 包冲突引起的 dpkg 错误“trying to overwrite `/lib/firmware/nvidia/535.288.01/gsp_ga10x.bin`”在 Ubuntu 上？

**答案：**

## 根本原因

这是一个已知冲突：当 `nvidia-kernel-common-535` 和 `nvidia-firmware-535-535.288.01` 包恰好处于相同的上游版本时，它们都会在磁盘上的同一路径提供相同的固件文件。当用户尝试同时安装两者时，会导致 dpkg 文件冲突。

这两个来自不同来源（Ubuntu 仓库 vs. NVIDIA 自己的仓库）的包都试图拥有同一文件：`/lib/firmware/nvidia/535.288.01/gsp_ga10x.bin`。

---

## 修复选项（按优先级顺序）

### 选项 1：先移除冲突的 `nvidia-firmware` 包（推荐）

最干净的方法是先移除独立的固件包，然后让 `nvidia-kernel-common-535` 拥有这些固件文件：

```bash
sudo apt remove nvidia-firmware-535-535.288.01
sudo apt --fix-broken install
sudo apt upgrade
```

### 选项 2：使用 `dpkg --force-overwrite` 强制覆盖

这会告诉 dpkg 继续并覆盖冲突文件。请注意，`--force-overwrite` 命令仅推荐给有经验的 Linux 用户，如果操作不当可能会进一步破坏系统。

```bash
# Force-overwrite the two conflicting packages
sudo dpkg -i --force-overwrite /tmp/apt-dpkg-install-wlv4CV/07-nvidia-kernel-common-535_535.288.01-0ubuntu1_amd64.deb
sudo dpkg -i --force-overwrite /tmp/apt-dpkg-install-wlv4CV/01-libnvidia-extra-535_535.288.01-0ubuntu1_amd64.deb

# Then fix broken dependencies
sudo apt --fix-broken install
```

或者如果文件在 apt 缓存路径中，使用：
```bash
sudo dpkg -i --force-overwrite /var/cache/apt/archives/nvidia-kernel-common-535_535.288.01-0ubuntu1_amd64.deb
sudo apt --fix-broken install
```

### 选项 3：完全干净重装 NVIDIA 驱动

如果上述方法无效，进行完全清除并重装：

```bash
# Remove all NVIDIA packages
sudo apt purge nvidia-* libnvidia-* cuda-drivers* --autoremove
sudo apt autoremove
sudo apt autoclean

# Update and reinstall
sudo apt update
sudo apt install nvidia-driver-535
```

---

## 修复后

始终在最后运行这些清理命令：

```bash
sudo apt --fix-broken install
sudo apt upgrade
sudo reboot
```

重启后，验证驱动是否已加载：
```bash
nvidia-smi
```

---

## 为什么会发生这种情况

您很可能同时安装了来自**两个不同来源**的包：
- Ubuntu 官方仓库包：`...-0ubuntu1`
- NVIDIA 自己的仓库包：`...-0ubuntu0.22.04.1`

版本后缀的差异（`0ubuntu1` vs `0ubuntu0.22.04.1`）表明包来源不同。最安全的长期修复方法是**仅固定到一个来源** — 要么是 Ubuntu 的 `ubuntu` 仓库，要么是 NVIDIA 官方仓库，但不要混用两者。

参考资料：

- [Ubuntu Bug #2025565 - nvidia-firmware conflict](https://bugs.launchpad.net/bugs/2025565)
- [Ubuntu Bug #2026622 - nvidia-firmware-535-server conflict](https://bugs.launchpad.net/ubuntu/+source/nvidia-graphics-drivers-535-server/+bug/2026622)
- [NVML Driver/Library Version Mismatch Fix Guide](https://hychiang.info/blog/2024/nvml_mismatch/)
