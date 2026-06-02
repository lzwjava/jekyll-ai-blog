---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5.2
title: Linux Mint 简易安装指南
translated: true
type: note
---

Question: 如何安装 Linux Mint？

Answer:

以下是一份**清晰、适合初学者、循序渐进的 Linux Mint 安装指南**，特别为**父母或非技术用户**编写。这是在普通 PC 或笔记本电脑上安装它最安全、最常用的方式。

---

## 1. 准备工作

### Hardware (硬件)

* 一台电脑（PC 或笔记本电脑）
* 一个 **USB flash drive**（8 GB 或更大）
* 互联网连接（推荐）

### Software (软件)

* Linux Mint ISO 文件
* 一个 USB 写入工具（Balena Etcher 或 Rufus）

---

## 2. 下载 Linux Mint

1. 访问官方网站：
   👉 [https://linuxmint.com](https://linuxmint.com)
2. 点击 **Download**
3. 选择 **Linux Mint Cinnamon**

   * 这是最用户友好、最像 Windows 的版本
4. 选择一个镜像站并下载 `.iso` 文件

💡 *强烈建议为父母选择 Cinnamon 版本。*

---

## 3. 制作启动盘 (Bootable USB)

### 在 Windows / macOS 上

1. 下载 **Balena Etcher**：
   👉 [https://etcher.balena.io](https://etcher.balena.io)
2. 插入你的 USB 驱动器
3. 打开 Etcher 并：

   * 选择 Linux Mint 的 `.iso` 文件
   * 选择对应的 USB 驱动器
   * 点击 **Flash**
4. 等待完成（USB 中的原数据将被擦除）

---

## 4. 从 USB 驱动器启动

1. 将 USB 插入要安装 Mint 的电脑
2. 重新启动电脑
3. 在启动过程中反复按下 **Boot Menu key**：

   * 常见按键：`F12`、`F10`、`ESC`、`DEL`
4. 选择 **USB device**
5. 选择 **“Start Linux Mint”**

👉 Linux Mint 现在将以 **Live Mode** 运行（此时尚未对系统做任何更改）。

---

## 5. 试用 Linux Mint (可选但推荐)

在 Live Mode 中，你可以：

* 检查 Wi-Fi 连接
* 测试声音、键盘、鼠标
* 查看屏幕显示是否正常

如果一切正常 → 双击桌面上的 **“Install Linux Mint”**。

---

## 6. 安装 Linux Mint (主要步骤)

### 第 1 步：语言 (Language)

* 选择你偏好的语言
* 点击 **Continue**

### 第 2 步：键盘布局 (Keyboard Layout)

* 通常会自动检测
* 点击 **Continue**

### 第 3 步：多媒体编解码器 (Multimedia Codecs)

✅ 勾选 **“Install multimedia codecs”**
（这将启用 MP3、视频播放等功能）

### 第 4 步：安装类型 (IMPORTANT)

为父母安装时，请选择以下之一：

#### 选项 A：完全替换 Windows (最简单)

* **“Erase disk and install Linux Mint”**
* 这将完全移除 Windows

#### 选项 B：与 Windows 共存 (Dual-boot)

* **“Install Linux Mint alongside Windows”**
* 你可以在启动时选择操作系统

⚠️ 如果不确定，**请先备份重要文件**。

### 第 5 步：时区 (Time Zone)

* 选择你所在的城市
* 点击 **Continue**

### 第 6 步：用户账号 (User Account)

* Name：父母的姓名
* Computer name：随意填写
* Username：自动生成
* Password：简单但安全
* 如果不想麻烦，请选择 **“Log in automatically”** (自动登录)

---

## 7. 完成安装

* 等待 10–20 分钟
* 点击 **Restart Now**
* 按照提示拔掉 USB

🎉 Linux Mint 现在已经安装完成了！

---

## 8. 安装后的首要事项

### 系统更新 (Update System)

1. 点击 **盾牌图标** (Update Manager)
2. 安装所有更新

### 安装常用 Apps

* Firefox (已预装)
* LibreOffice (Word / Excel 的替代品)
* VLC Media Player
* Zoom / WeChat (通过浏览器或 Flatpak)

### 启用中文输入 (如果需要)

* Settings → Input Methods
* 添加 **Fcitx** + Pinyin

---

## 9. 为什么 Linux Mint 非常适合父母

* 界面布局类似 Windows (开始菜单、任务栏)
* 没有强制更新
* 非常稳定
* 免疫大多数病毒
* 软件安装简单
* 维护成本极低

---

## 我的最终建议

对于父母和家人：

* **Linux Mint Cinnamon**
* 开启自动登录 (Automatic login)
* 开启自动更新 (Auto-updates)
* 简单的桌面图标

如果你需要，我还可以协助：

* Dual-boot 设置
* 旧电脑优化
* 中文语言环境配置
* 适合父母的推荐应用
* 远程协助设置（以便你后续帮助他们）

直接告诉我即可 👍
