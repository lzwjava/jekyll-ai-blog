---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Windows上安装WSL指南
translated: true
type: note
---

问题：如何在 Windows 上安装 WSL？

回答：

WSL（Windows Subsystem for Linux）可让你直接在 Windows 上运行真实的 Linux 环境（如 Ubuntu）。现代安装过程十分简单——微软已基本实现自动化。

---

## 1. 检查 Windows 版本

WSL 2 在以下版本上运行最佳：

* Windows 10 版本 2004+（内部版本 19041+）
* Windows 11（推荐）

检查方法：

```text
Win + R → 输入 winver
```

---

## 2. 安装 WSL（最快方法）

以管理员身份打开 **PowerShell**，运行：

```powershell
wsl --install
```

此命令将自动完成：

* 启用所需 Windows 功能
* 安装 WSL 2
* 下载并安装 **Ubuntu（默认 Linux 发行版）**
* 设置 WSL 2 为默认版本

---

## 3. 重启计算机

安装完成后：

* 重启 Windows 系统

---

## 4. 首次 Linux 设置

重启后：

* Ubuntu 将自动打开
* 系统会提示：

  * 创建 Linux 用户名
  * 设置密码

这即是你 Windows 内的 Linux 环境。

---

## 5. 验证安装

运行：

```powershell
wsl --list --verbose
```

应显示类似信息：

```text
Ubuntu    正在运行    2
```

---

## 6. 升级 WSL（如需）

确保使用 WSL 2：

```powershell
wsl --set-default-version 2
```

---

## 7. 安装其他 Linux 发行版（可选）

查看可用发行版列表：

```powershell
wsl --list --online
```

安装示例：

```powershell
wsl --install -d Debian
```

---

## 8. 如何使用 WSL

可通过多种方式打开：

* 开始菜单 → “Ubuntu”
* VS Code → “WSL 扩展”
* 终端输入：

```bash
wsl
```

---

## 9. 在 VS Code 中使用 WSL（强烈推荐）

安装：

* VS Code 扩展：**WSL**

然后在 WSL 终端中运行：

```bash
code .
```

即可在 VS Code 中直接打开 Linux 环境。

---

## 10. WSL 的优势（尤其适合你）

考虑到你涉及开发 + SSH + AI 工具：

WSL 提供：

* 原生 Linux 工具（`ssh`、`grep`、`curl`、`bash`、`python`）
* 避免 Windows 路径问题
* 更好的服务器兼容性
* 比 Git Bash 更整洁的开发环境

---

## 快速建议

如果你的目标是：

* SSH 连接服务器
* 使用 Copilot
* 稳定运行开发工具

👉 WSL 2 + Ubuntu 是 Windows 上长期使用的最佳配置方案。

---

如果需要，我可以帮你一次性配置 **完整的 WSL 开发环境（Git、SSH 密钥、Docker、Python、Node、VS Code 集成）**。
