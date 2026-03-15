---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 NVIDIA 软件包冲突步骤
translated: true
type: note
---

以下是我修复该 NVIDIA 包冲突的方法：

**1. 诊断冲突**
```bash
dpkg -l | grep -E "nvidia-compute-utils|nvidia-persistenced"
apt-cache show nvidia-compute-utils-535 | grep -i persistenced
```

**2. 删除独立包**
```bash
sudo apt remove --purge nvidia-persistenced
```
这会删除与 nvidia-compute-utils-535 中内置的一个冲突的旧独立包。

**3. 清理并重新配置**
```bash
sudo apt autoremove
sudo apt --fix-broken install
sudo dpkg --configure -a
```

**4. 重试驱动安装**
```bash
sudo apt install nvidia-driver-535
```

**为什么有效：** nvidia-compute-utils-535 已经包含 persistenced 二进制文件和服务。拥有单独的包意味着两个文件试图占用同一路径，dpkg 会拒绝。删除独立包让新包干净地接管。

如果 systemd 中仍有旧的 nvidia-persistenced 服务，我也建议禁用它：
```bash
sudo systemctl disable nvidia-persistenced
sudo systemctl daemon-reload
```

这就是完整的修复方法。