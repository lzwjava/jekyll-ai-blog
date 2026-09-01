---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Windows 7上安装SSH服务器
translated: true
type: note
---

**问题：** 如何在 Windows 7 上安装 SSH 服务器，以便我可以复制文件或使用 AI 代理远程操作该计算机？

---

**回答：**

Windows 7 没有内置 SSH 服务器，但你可以从 Microsoft 的 GitHub 安装 **Win32-OpenSSH**。Win32-OpenSSH GitHub 发布版支持 Windows 7 及以上版本。以下是完整流程：

---

## 第 1 步 — 下载 Win32-OpenSSH

访问：**<https://github.com/PowerShell/Win32-OpenSSH/releases>**

下载 `OpenSSH-Win64.zip`（64 位）或 `OpenSSH-Win32.zip`（32 位）。

---

## 第 2 步 — 安装

将内容解压到 `C:\Program Files\OpenSSH`。确保该文件夹的写入权限仅限 SYSTEM 和 Administrators 组——已验证用户应仅具有读取和执行权限。

然后以**管理员身份打开 PowerShell** 并运行：

```powershell
cd "C:\Program Files\OpenSSH"
powershell.exe -ExecutionPolicy Bypass -File install-sshd.ps1
```

---

## 第 3 步 — 打开防火墙（Windows 7 方法）

对于 Windows 7（客户端桌面 / Windows 2008 R2 及更低版本），使用以下命令代替 `New-NetFirewallRule`：

```cmd
netsh advfirewall firewall add rule name=sshd dir=in action=allow protocol=TCP localport=22
```

或者前往**控制面板 → Windows 防火墙 → 高级设置 → 入站规则**，为 TCP 端口 22 添加一条新规则。

---

## 第 4 步 — 启动 SSH 服务

```powershell
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

---

## 第 5 步 — 连接与使用

**从另一台机器复制文件**，使用 SCP 或 SFTP：

```bash
# 将文件复制到 Windows 7 机器
scp myfile.txt username@192.168.1.x:/C:/Users/username/Desktop/

# 或者使用 SFTP 客户端，如 WinSCP 或 FileZilla
```

**通过 SSH 远程运行命令**：

```bash
ssh username@192.168.1.x
```

---

## 使用 AI 代理远程操作

一旦 SSH 运行起来，AI 代理（如通过 Claude Code 的 Claude，或任何自动化工具）即可通过 SSH 连接并执行：

- 执行 shell 命令
- 通过 SFTP 读写文件
- 运行脚本或程序

对于 **Claude 来说**，Claude Code 支持基于 SSH 的远程操作——你只需将指向 Windows 7 机器的 IP，并提供凭据或 SSH 密钥即可。或者，像 **Fabric**、**Paramiko**（Python）或 **Ansible** 这样的工具也可以通过 SSH 脚本化操作。

> ⚠️ **安全提示：** Windows 7 已停止支持（自 2020 年起无安全更新）。将 SSH 暴露在公网 IP 上是有风险的。请仅在本地/私有网络中使用，或通过 VPN 访问。

---

参考资料：

- [安装 Win32-OpenSSH（GitHub Wiki）](https://github.com/PowerShell/Win32-OpenSSH/wiki/Install-Win32-OpenSSH)
- [Win32-OpenSSH 发布版](https://github.com/PowerShell/Win32-OpenSSH/releases)
- [WinSCP：在 Windows 上安装 SSH 服务器](https://winscp.net/eng/docs/guide_windows_openssh_server)
- [如何在 Windows 7/10 上安装 OpenSSH – Fred_151](https://fred151.net/site/2018/09/23/how-to-install-openssh-on-windows-7-10/)
