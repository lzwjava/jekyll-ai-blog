---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Linux Mint上安装Scratch
translated: true
type: note
---

问题：如何在Linux Mint上安装Scratch，它是否支持Linux，还是仅支持Windows？

回答：Scratch完全支持Linux，不仅限于Windows。实际上，它在Linux Mint上运行得非常顺畅。你有几种简便的安装和使用方式。

---

## ✅ 选项1：使用Scratch在线版（无需安装）

最简便的方式是在浏览器中直接使用Scratch：

* 访问：[https://scratch.mit.edu](https://scratch.mit.edu)
* 可在Linux Mint、Windows、macOS甚至Chromebook上使用
* 无需任何设置
* 始终为最新版本

如果你希望快速上手，推荐此方法。

---

## 🧩 选项2：安装Scratch桌面版（离线应用）

### 方法A — Flatpak（推荐用于Linux Mint）

Linux Mint默认支持Flatpak。

1. 打开终端
2. 运行：

```bash
flatpak install flathub edu.mit.Scratch
```

3. 启动应用：

```bash
flatpak run edu.mit.Scratch
```

或在安装后从应用程序菜单中搜索“Scratch”启动。

---

### 方法B — Snap（备选方案）

如果已启用Snap：

```bash
sudo snap install scratch-desktop
```

---

## 🧰 选项3：通过软件管理器安装（图形界面方式）

Linux Mint也提供图形化商店：

1. 打开 **软件管理器**
2. 搜索 **Scratch**
3. 点击 **安装**

---

## 🖥️ 兼容性说明

* ✔ Linux Mint：完全支持
* ✔ Windows：完全支持
* ✔ macOS：完全支持
* ✔ 网页版：适用于所有平台
* ⚠ 桌面应用主要基于网页版封装，但可离线进行基础项目制作

---

## 💡 推荐建议

* 如果你是学习者或教学者 → 使用浏览器版
* 如果你需要离线工作 → 使用Flatpak版
* 如果你追求简单快捷 → 通过软件管理器安装

---

如果你需要，我还可以展示：

* 如何创建你的第一个Scratch项目
* 如何一步步教孩子使用Scratch
* 如何在低配置Linux设备上流畅运行Scratch
