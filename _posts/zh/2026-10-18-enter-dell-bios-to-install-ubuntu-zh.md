---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 进入戴尔BIOS安装Ubuntu
translated: true
type: note
---

**问题：** 如何重启戴尔笔记本电脑并进入BIOS以安装Ubuntu？

---

**回答：**

## 步骤 1 — 重启并进入BIOS

| 方法 | 按键 | 按下时机 |
| -------- | ----- | --------------- |
| **BIOS设置** | `F2` | 戴尔Logo出现时立即按下 |
| **启动菜单**（推荐用于Ubuntu安装） | `F12` | 戴尔Logo出现时立即按下 |

> **提示：** 按下电源按钮后立即反复点按该按键——不要按住不放，每半秒点按一次，直到菜单出现。

---

## 步骤 2 — 准备Ubuntu USB启动盘（请先在另一台电脑上完成此操作）

1. 从 [ubuntu.com](https://ubuntu.com/download) 下载Ubuntu ISO镜像
2. 使用以下工具将其写入USB启动盘（8 GB及以上）：
   - **Windows：** [Rufus](https://rufus.ie) — 选择ISO镜像，分区类型：**GPT**，目标系统：**UEFI**
   - **Mac/Linux：** [balenaEtcher](https://etcher.balena.io)

---

## 步骤 3 — 需要检查的BIOS设置（按F2进入）

进入BIOS并确认以下设置：

| 设置项 | 所需值 |
| --------- | ---------------- |
| **Secure Boot**（安全启动） | **Disabled**（禁用）（或设置为"Other OS"） |
| **SATA Mode**（SATA模式） | **AHCI**（非RAID） |
| **Boot Mode**（启动模式） | **UEFI** |

按 `F10` 保存并退出。

---

## 步骤 4 — 从USB启动（按F12）

1. 开机时按 **F12** → 出现 **一次性启动菜单（One Time Boot Menu）**
2. 在 **UEFI Boot**（UEFI启动）部分选择您的USB启动盘
3. Ubuntu安装程序将启动
4. 按照屏幕上的步骤完成安装

---

## 快速摘要

```
开机 → 点按F12 → 选择USB → 安装Ubuntu
             （或先按F2修改BIOS设置）
```

---

**参考资料：**

- [戴尔BIOS设置指南](https://www.dell.com/support/kbdoc/en-us/000126121/how-to-enter-system-bios-setup-on-a-dell-laptop-desktop-or-workstation)
- [Ubuntu安装教程](https://ubuntu.com/tutorials/install-ubuntu-desktop)
- [Rufus – 可启动USB制作工具](https://rufus.ie)
