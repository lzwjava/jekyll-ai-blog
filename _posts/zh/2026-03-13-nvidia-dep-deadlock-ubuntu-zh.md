---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Ubuntu NVIDIA 依赖死锁
translated: true
type: note
---

## 诊断

你陷入了由 **mixed NVIDIA package versions**（混合 NVIDIA 软件包版本）引起的循环依赖地狱：

- 某些软件包处于 `535.288.01-0ubuntu1` (Ubuntu repo)
- 某些仍处于 `535.274.02-0ubuntu1` 或 `535.288.01-0ubuntu0.22.04.1` (NVIDIA repo)

唯一可靠的逃脱方法是 **full NVIDIA purge and clean reinstall**（完全清除 NVIDIA 并干净重装）。

---

## 逐步修复

### 步骤 1: 先强制覆盖最初失败的两个软件包

```bash
sudo dpkg -i --force-overwrite \
  /var/cache/apt/archives/nvidia-kernel-common-535_535.288.01-0ubuntu1_amd64.deb
```

如果那些 `.deb` 文件已从缓存中消失，请重新下载它们：

```bash
sudo apt-get download nvidia-kernel-common-535 libnvidia-extra-535
sudo dpkg -i --force-overwrite nvidia-kernel-common-535_*.deb
sudo dpkg -i --force-overwrite libnvidia-extra-535_*.deb
```

---

### 步骤 2: 强制移除所有 NVIDIA 和 CUDA 软件包

```bash
sudo dpkg --remove --force-remove-reinstreq \
  $(dpkg -l | grep -E 'nvidia|cuda|libnvidia' | awk '{print $2}' | tr '\n' ' ')
```

或者更保守地，先列出它们：

```bash
dpkg -l | grep -E 'nvidia|cuda|libnvidia' | awk '{print $2}'
```

然后移除列出的所有内容：

```bash
sudo apt purge --allow-remove-essential \
  nvidia-* libnvidia-* cuda-* nvidia-dkms-535 nvidia-kernel-common-535 \
  nvidia-firmware-535-535.288.01 -y
```

---

### 步骤 3: 清理损坏状态

```bash
sudo dpkg --configure -a
sudo apt --fix-broken install
sudo apt autoremove --purge
sudo apt clean
sudo apt autoclean
```

---

### 步骤 4: 移除任何导致版本冲突的剩余 NVIDIA apt 来源

```bash
# 列出所有 NVIDIA 相关来源
grep -r nvidia /etc/apt/sources.list /etc/apt/sources.list.d/ 2>/dev/null
```

如果你看到 **both** `ppa:graphics-drivers` 和 `developer.download.nvidia.com` 的条目，**移除其中一个** 以避免未来冲突：

```bash
sudo rm /etc/apt/sources.list.d/cuda*.list
# 或
sudo add-apt-repository --remove ppa:graphics-drivers/ppa
```

然后更新：

```bash
sudo apt update
```

---

### 步骤 5: 从单一来源干净重装

```bash
sudo apt install nvidia-driver-535 nvidia-dkms-535
```

或者如果你需要 CUDA：

```bash
sudo apt install cuda-12-2
```

---

### 步骤 6: 重启并验证

```bash
sudo reboot
# 重启后：
nvidia-smi
```

---

## 关键原则

| 规则 | 详情 |
| ------ | -------- |
| Never mix sources | Pick Ubuntu repo OR NVIDIA repo, not both |
| Version suffix `-0ubuntu1` | Comes from Ubuntu's official repo |
| Version suffix `-0ubuntu0.22.04.1` | Comes from NVIDIA's own CUDA repo |
| These **conflict** when they share firmware files | Always purge before switching sources |

参考资料：

- [NVIDIA CUDA Installation Guide for Linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)
- [Ubuntu help: broken packages](https://help.ubuntu.com/community/BrokenPackages)
