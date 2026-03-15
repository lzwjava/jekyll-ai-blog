---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CUDA 13.2 驱动修复指南
translated: true
type: note
---

✅ **完成！** 在 `~/.bashrc.backup` 创建备份，并将 CUDA 13.2 添加到 PATH 和 LD_LIBRARY_PATH。

---

## 📋 **修复摘要：NVIDIA Driver & CUDA 13.2 安装**

**问题：** `nvidia-smi` 报错 "NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver"

**根本原因：** NVIDIA 驱动程序包损坏/混合（590 系列 + 595 系列）处于半安装状态

**解决方案步骤：**

1. **清理损坏的包：**
   - 终止卡住的 dpkg/apt 进程（持有锁）
   - 移除 `/var/lib/dpkg/lock*` 文件
   - 清除冲突的 NVIDIA 包（`nvidia-*`、`libnvidia-*`）
   - 修复损坏的 dpkg 更新文件

2. **移除版本冲突：**
   - `libnvidia-cfg1` (595) 与 `libnvidia-cfg1-535` 冲突
   - `libnvidia-egl-gbm1` 与 NVIDIA 535 驱动冲突

3. **安装正确版本：**
   - 从 NVIDIA 仓库安装 CUDA Toolkit 13.2
   - NVIDIA Driver 535.288.01（Ubuntu 仓库） - 与 CUDA 13.2 兼容

4. **验证安装：**
   - `nvidia-smi` 显示 RTX 4070 激活
   - 驱动：535.288.01
   - CUDA 路径：`/usr/local/cuda-13.2`
   - 成功编译并运行测试 CUDA 程序

**使用的关键命令：**
```bash
# Fix dpkg locks and kill stuck processes
sudo kill -9 $(ps aux | grep dpkg | grep -v grep | awk '{print $2}')
sudo rm -f /var/lib/dpkg/lock*

# Remove broken packages
sudo dpkg --remove --force-remove-reinstreq cuda-drivers libnvidia-compute libnvidia-decode libnvidia-encode libnvidia-gl nvidia-driver xserver-xorg-video-nvidia

# Install CUDA 13.2 and driver
sudo apt-get install -y cuda-13-2
sudo apt-get install -y nvidia-driver-535

# Load driver and test
sudo modprobe nvidia
nvidia-smi
```

**当前状态：** ✅ **已修复** - CUDA 13.2 + NVIDIA Driver 535 与 RTX 4070 正常工作