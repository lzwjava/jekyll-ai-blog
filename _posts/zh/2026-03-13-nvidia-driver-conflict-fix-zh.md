---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 NVIDIA 驱动包冲突
translated: true
type: note
---

问题：如何在 Ubuntu 上安装 NVIDIA 驱动程序时修复 `nvidia-compute-utils-535` 和 `nvidia-persistenced` 之间的冲突？

答案：

## 根本原因

`nvidia-compute-utils-535` **包含**内置的 `nvidia-persistenced` 功能，但系统中还安装了**独立的** `nvidia-persistenced` 软件包。它们冲突是因为两者都提供相同的二进制文件/服务。

```
nvidia-compute-utils-535  ←  ships nvidia-persistenced binary internally
nvidia-persistenced        ←  standalone package, same binary = CONFLICT
```

---

## 修复方法：先移除冲突的软件包

### 步骤 1：移除 `nvidia-persistenced`

```bash
sudo apt remove --purge nvidia-persistenced
sudo apt remove --purge nvidia-persistenced:i386
```

### 步骤 2：修复损坏状态

```bash
sudo dpkg --configure -a
sudo apt --fix-broken install
```

### 步骤 3：现在重试安装

```bash
sudo apt install nvidia-compute-utils-535
```

---

## 如果步骤 1 失败（依赖关系阻止）

直接通过 dpkg 强制移除：

```bash
sudo dpkg --remove --force-depends nvidia-persistenced
```

然后清理：

```bash
sudo apt --fix-broken install
sudo apt autoremove --purge
```

---

## 如果仍有被保留的软件包

检查被保留的内容：

```bash
sudo apt-mark showhold
dpkg -l | grep ^h
```

取消所有 NVIDIA 相关的保留：

```bash
sudo apt-mark unhold nvidia-* libnvidia-* cuda-*
```

然后重试：

```bash
sudo apt --fix-broken install
sudo apt upgrade
```

---

## 您当前情况的全貌

根据您迄今遇到的所有错误，您的系统积累了来自**3 个来源混合**的冲突：

| 软件包来源 | 版本后缀 | 示例 |
|---|---|---|
| Ubuntu 官方仓库 | `-0ubuntu1` | `535.288.01-0ubuntu1` |
| NVIDIA CUDA 仓库 | `-0ubuntu0.22.04.1` | `535.288.01-0ubuntu0.22.04.1` |
| 独立的旧软件包 | 各异 | `nvidia-persistenced` |

最干净的长期修复方案仍然是**完全清除并从单一来源重新安装**，前提是您先清除此冲突：

```bash
# 核选项 - 仅在上述步骤失败时使用
sudo apt purge nvidia-* libnvidia-* cuda-* --allow-remove-essential
sudo apt autoremove --purge
sudo apt clean
sudo apt update
sudo apt install nvidia-driver-535
```

参考资料：

- [Ubuntu Manpage: apt-mark](https://manpages.ubuntu.com/manpages/focal/man8/apt-mark.8.html)
- [NVIDIA CUDA Toolkit Download](https://developer.nvidia.com/cuda-downloads)
