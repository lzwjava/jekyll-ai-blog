---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu 26.04 代号非坚定
translated: true
type: note
---

**问题：** Ubuntu 26.04 是否使用与屏幕上显示的相同的“resolute”代号和持久化设置？

**答案：**

**不是**，Ubuntu 和 Kali Linux 是不同的发行版。以下是对比：

---

**代号系统——不同：**

| 发行版 | 代号风格 | 示例 |
|---|---|---|
| **Kali Linux** | 形容词 | `resolute`、`kali-rolling` |
| **Ubuntu** | 动物名称（形容词 + 动物） | `noble` (24.04)、`oracular` (24.10) |

**Ubuntu 26.04 代号** 将遵循该模式——很可能类似于 **“P____ P____”**（以 P 开头，目前尚未正式公布）。

---

**持久化设置——也不同：**

| 功能 | Kali Live USB | Ubuntu Live USB |
|---|---|---|
| 持久化标签 | `writable` | `casper-rw` |
| 持久化文件夹 | `/log-persistence` | `/casper-rw` |
| 默认用户 | `kali/kali` | `ubuntu`（无密码） |
| APT 源标签 | `resolute`（Kali 代号） | `noble`、`oracular` 等 |

---

**底线：**

你屏幕上显示的**绝对是 Kali Linux**，不是 Ubuntu。启动日志中的 **“resolute”** 一词就是证据——这是 Kali 的发布代号，Ubuntu 从未使用过这个名称。

如果你想改用 Ubuntu，你需要使用 **Balena Etcher** 或 **Rufus** 等工具单独刷写 `ubuntu-26.04-desktop-amd64.iso`。

---

**参考资料：**
- [Kali Linux 2024.4 “resolute” 发布](https://www.kali.org/blog/kali-linux-2024-4-release/)
- [Ubuntu 发布代号列表](https://wiki.ubuntu.com/DevelopmentCodeNames)
- [Balena Etcher —— USB 刷写工具](https://etcher.balena.io/)