---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Windows上安装WSL 2
translated: true
type: note
---

安装 **WSL 2（适用于 Linux 的 Windows 子系统 2）** 在现代 Windows 10 和 Windows 11 上非常简单。

### 选项 1：一键安装（推荐）

1.  以**管理员**身份打开 **PowerShell** 或**命令提示符**。
2.  运行：

```powershell
wsl --install
```

此命令将：

*   启用 WSL
*   安装 WSL 2
*   下载 Linux 内核
*   安装 Ubuntu（默认）
*   自动配置所有内容

如果系统提示，请重启计算机。（[Microsoft Learn][1]）

---

### 验证安装

重启后，打开 PowerShell 并运行：

```powershell
wsl --status
```

要查看已安装的发行版：

```powershell
wsl --list --verbose
```

你应该会看到类似下面的内容：

```text
NAME      STATE    VERSION
Ubuntu    Running  2
```

如果版本是 `2`，则表示你正在使用 WSL 2。（[Microsoft Learn][1]）

---

### 安装不同的 Linux 发行版

要查看可用的发行版：

```powershell
wsl --list --online
```

安装其中一个，例如：

```powershell
wsl --install -d Ubuntu
```

或

```powershell
wsl --install -d Debian
```

---

### 如果你已有 WSL 1

将现有发行版转换为 WSL 2：

```powershell
wsl --set-version Ubuntu 2
```

必要时将 `Ubuntu` 替换为你的发行版名称。（[Microsoft Learn][1]）

---

### 检查 Windows 版本

WSL 2 要求：

*   Windows 11，或者
*   Windows 10 版本 1903 或更高版本（包含所需的内部版本更新）。（[Microsoft Learn][2]）

---

### 官方 Microsoft 指南

有关详细说明和故障排除，请参阅：

[在 Windows 上安装 WSL（Microsoft Learn）](https://learn.microsoft.com/zh-cn/windows/wsl/install)

如果你告诉我：

*   你的 **Windows 版本**（Windows 10 或 11），以及
*   `winver` 的输出

我可以提供针对你系统的具体说明。

[1]: https://learn.microsoft.com/zh-cn/windows/wsl/install "如何在 Windows 上使用 WSL 安装 Linux"
[2]: https://learn.microsoft.com/zh-cn/windows/wsl/install-manual "旧版 WSL 的手动安装步骤"