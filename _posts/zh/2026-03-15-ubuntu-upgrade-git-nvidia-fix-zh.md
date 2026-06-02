---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu 升级移除 Git NVIDIA 修复
translated: true
type: note
---

**问题：** 在从 Ubuntu 22.04 运行 `do-release-upgrade` 升级到 24.04 后，在最后一步是否应该选择移除旧的/过时的软件包？现在 `git` 和我的 NVIDIA 驱动都消失了——如何修复？

---

**回答：**

## 理解“移除过时软件包”步骤

在 `do-release-upgrade` 更新所有软件包后，系统会提示您移除不再需要的过时软件包，消息类似于：“Remove obsolete packages? 30 packages are going to be removed. Continue [y/N] Details [d]”

您可以在决定前按 `d` 查看这些软件包的详细信息。过时的软件包不会收到安全更新，因此移除它们通常是合理的——但您可能希望保留它们，以确保系统与旧应用程序继续正常工作。

**简短回答：您应该总是先按 `d` 查看列表，然后再决定是否确认。** 问题是 `do-release-upgrade` 有时会错误地将 `git` 或 NVIDIA 驱动等软件包标记为“过时”——特别是如果它们来自 PPA、第三方仓库（如 NVIDIA 自己的 CUDA repo），或者升级过程中升级工具丢失了它们的跟踪。

---

## 为什么 Git 和 NVIDIA 驱动被移除

有两个常见原因：

**1. 第三方 / PPA 来源**
如果升级工具在新 Ubuntu 24.04 仓库中找不到这些软件包，它就会将它们标记为“过时”。如果您的 NVIDIA 驱动是从第三方来源安装的（例如 `ppa:graphics-drivers/ppa` 或 NVIDIA 的 CUDA repo），它可能不会被识别为有效的 24.04 软件包，从而被标记为移除。

**2. NVIDIA 升级逻辑静默失败**
升级工具的内部日志可能显示类似 `INFO no old nvidia driver installed, installing no new` 的消息——这意味着该工具未检测到已识别的 NVIDIA 驱动，并跳过了自动重新安装，从而导致升级后您没有驱动。

---

## 修复：重新安装 Git

这很简单——`git` 在 Ubuntu 24.04 的默认仓库中可用：

```bash
sudo apt update
sudo apt install git
```

使用以下命令验证：
```bash
git --version
```

---

## 修复：在 Ubuntu 24.04 上重新安装 NVIDIA 驱动

**步骤 1：检查您的 GPU**
```bash
lspci | grep -i nvidia
```

**步骤 2：让 Ubuntu 检测并推荐正确的驱动**
```bash
sudo ubuntu-drivers list
```

**步骤 3：自动安装推荐的驱动**
```bash
sudo ubuntu-drivers autoinstall
```

或者手动安装特定版本（将 `550` 替换为您偏好的版本）：
```bash
sudo apt install nvidia-driver-550
```

**步骤 4：确保安装了内核头文件（DKMS 所需）**
```bash
sudo apt install linux-headers-$(uname -r) build-essential
```

**步骤 5：重启**
```bash
sudo reboot
```

**步骤 6：验证**
```bash
nvidia-smi
```

如果安装后 `nvidia-smi` 缺失，该命令由 NVIDIA 实用工具软件包提供。为您的分支安装匹配的实用工具软件包，例如 `nvidia-utils-<version>`，然后再次运行 `nvidia-smi`。

---

## 如果您有损坏的软件包

如果 `apt install` 报告损坏软件包错误，请先清理：

```bash
sudo apt purge 'nvidia-*' 'libnvidia-*'
sudo apt clean
sudo apt update
sudo apt -f install
sudo ubuntu-drivers autoinstall
```

---

## 未来升级的最佳实践

下次运行 `do-release-upgrade` 前：

1. **总是按 `d`** 在“Remove obsolete packages?” 提示处，并审查将被移除的内容。
2. **记下任何重要软件包**，以便升级后重新安装（特别是 NVIDIA 驱动、`git` 等）。
3. 对于 NVIDIA 用户，升级前切换到开源 `nouveau` 驱动是一个更安全的方法，然后在成功引导到新版本后重新安装专有 NVIDIA 驱动。

---

参考资料：

- [Ubuntu Server Docs - How to upgrade your release](https://documentation.ubuntu.com/server/how-to/software/upgrade-your-release/)
- [How to Install NVIDIA Drivers on Ubuntu 24.04 - Cherry Servers](https://www.cherryservers.com/blog/install-nvidia-drivers-ubuntu)
- [Ubuntu 24.04 + Nvidia Drivers - projectable.me](https://projectable.me/ubuntu-24-04-nvidia-drivers-ollama/)
- [How to Install NVIDIA Drivers on Ubuntu - LinuxCapable](https://linuxcapable.com/install-nvidia-drivers-on-ubuntu-linux/)
- [do-release-upgrade 22.04 to 24.04 - Launchpad Q&A](https://answers.launchpad.net/ubuntu/+source/ubuntu-release-upgrader/+question/822286)
