---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Fedora Linux 安装指南 2026
translated: true
type: note
---

**Question:** 如何安装 Fedora Linux？

**Answer:**

这是一份清晰的分步指南，用于安装 **Fedora Linux**（截至 2026 年，该过程与最近的版本——Fedora 41 / 42 时代非常相似）。

### 安装 Fedora 的两种主要方式

1. **Workstation**（推荐大多数台式机/笔记本电脑用户使用 —— GNOME 桌面）
2. **Spins** / **Kinoite** / **Silverblue** / **Server** / 等（如果你想要 KDE、XFCE、immutable system、服务器版本等，请选择这些）

### 2025/2026 年推荐方法：Fedora Workstation (GNOME)

#### 步骤 1 – 下载 Fedora

- 访问官方网站：
  <https://getfedora.org/>

- 选择 **Fedora Workstation**（最受欢迎的选择）

- 下载 ISO 文件 (~2.0–2.5 GB)

#### 步骤 2 – 制作启动 USB (bootable USB)

使用以下工具之一（均为免费）：

| 您当前的 OS | 推荐工具 | 备注 |
| --------------------- | ------------------------------------ | --------------------------------------- |
| Windows | Rufus (最佳) 或 Fedora Media Writer | 如果需要，在 Rufus 中使用 “DD mode” |
| macOS | Fedora Media Writer 或 balenaEtcher | Fedora Media Writer 是官方工具 |
| Linux | Fedora Media Writer, `dd`, Ventoy, balenaEtcher | `dd` 命令非常可靠 |

**快速 dd 命令示例 (Linux):**

```bash
sudo dd if=Fedora-Workstation-Live-x86_64-42-1.2.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

将 `/dev/sdX` 替换为您的 USB 设备（使用 `lsblk` 检查 —— **请务必小心！**）

#### 步骤 3 – 从 USB 启动

- 插入 USB
- 重启电脑
- 进入 **boot menu**（通常是 F12, F11, Esc, F2, Del —— 取决于制造商）
  - 常见按键：
    - Dell      → F12
    - Lenovo   → F12 或 Fn+F12
    - HP       → F9 或 Esc → F9
    - ASUS     → F8 或 Esc
- 选择 USB 驱动器

如果它没有出现 → 进入 BIOS/UEFI（通常是 Del, F2, F10）并：

- 禁用 **Secure Boot**（建议首次安装时关闭）
- 将 USB 设置为第一启动设备或启用 “UEFI USB boot”

#### 步骤 4 – 启动 Fedora Live 系统

- 选择 **Try Fedora**（推荐）或 **Install to Hard Drive**

- 测试各项功能是否正常（Wi-Fi、声音、触控板、屏幕亮度）

#### 步骤 5 – 启动安装程序 (Anaconda)

点击桌面上的 **“Install to Hard Drive”** 图标。

图形化安装程序包含以下主要步骤：

1. **Language** → 选择您的语言
2. **Keyboard** → 如果需要，添加布局
3. **Time & Date** → 通常会自动检测
4. **Installation Destination**
   - 选择您的硬盘
   - 两个简单的选择：
     - **Automatic** 分区（推荐初学者使用）
     - **Custom**（如果您想要独立的 /home、encryption 等）
5. **Network & Hostname**（可选）
6. **Root Password** & **User Creation**
   - 创建至少一个用户（您可以将其设为管理员）
   - 设置 root 密码（或启用 root 登录 —— 不推荐）
7. 开始安装 → 等待 3–15 分钟

#### 步骤 6 – 完成并重启

- 根据提示拔掉 USB
- 点击 **Reboot**

首次启动：

- 出现 GNOME 欢迎界面 / 导览
- 如果需要，连接 Wi-Fi
- 使用您创建的用户登录

### 快速技巧与常见选择 (2026)

| 问题 | 适合大多数人的推荐 | 替代方案 |
| --------------------------------- | -------------------------------------- | --------------------------------- |
| 桌面环境 (Desktop environment) | GNOME (Workstation) | KDE (Fedora KDE Spin) |
| 不可变/原子系统 (Immutable / atomic system) | Fedora Silverblue 或 Kinoite | Traditional (Workstation) |
| 全盘加密 (Full disk encryption) | 是 (LUKS) | 否 (速度更快，但安全性较低) |
| 分区 (Partitioning) | Automatic | Custom (如果是双系统/dual-boot) |
| 安全启动 (Secure Boot) | 安装期间禁用 (Disabled) | 以后可以重新启用 |
| 第三方编解码器/驱动程序 | 安装后通过命令行安装 | — |

**安装后有用的命令：**

```bash
# 更新系统
sudo dnf update --refresh

# 安装常用的实用软件包 (多媒体等)
sudo dnf install ffmpeg gstreamer1-plugins-{bad-\*,good-\*,ugly-\*,base} gstreamer1-plugin-openh264

# 启用 RPM Fusion (以获取更多软件)
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

尽情享受 Fedora 吧！
它是目前最先进、最及时、最纯净的 Linux 发行版之一。

**参考资料：**

- [https://getfedora.org/](https://getfedora.org/)
- [https://docs.fedoraproject.org/en-US/fedora/latest/install-guide/](https://docs.fedoraproject.org/en-US/fedora/latest/install-guide/)
