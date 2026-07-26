---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想小新Windows安装
translated: true
type: note
---

问题：如何给联想小新笔记本安装 Windows？

回答：

对于联想小新（Xiaoxin）笔记本，通常的方法是制作一个 Windows USB 安装盘并从它启动。过程和大多数现代联想笔记本一样。

## 1. 准备 Windows 安装 U 盘

你需要：

* U 盘：**8GB 以上**（推荐 16GB）
* 另一台可用的电脑
* Windows 11/10 ISO 或微软媒体创建工具

官方下载：

* [下载 Windows 11](https://www.microsoft.com/software-download/windows11?utm_source=chatgpt.com)
* [下载 Windows 10](https://www.microsoft.com/software-download/windows10?utm_source=chatgpt.com)

在另一台电脑上：

### 选项 A：微软媒体创建工具

1. 插入 U 盘
2. 运行媒体创建工具
3. 选择：

   ```
   创建安装介质
   → U 盘
   → 选择你的 U 盘
   ```
4. 等待完成。

### 选项 B：Rufus + ISO

下载 Rufus：

[Rufus USB 安装工具](https://rufus.ie?utm_source=chatgpt.com)

设置：

```
设备：你的 U 盘
启动选择：Windows ISO

分区方案：
GPT

目标系统：
UEFI

文件系统：
NTFS
```

点击开始。

---

## 2. 进入联想小新启动菜单

关闭笔记本。

常见的联想按键：

* **F12** → 启动菜单
* **Fn + F12** → 有时需要
* **F2** → BIOS 设置
* **Novo 按钮** → 联想恢复/启动菜单

对于小新，Novo 按钮通常：

* 在电源按钮附近的一个小针孔
* 关机后用回形针按

菜单：

```
Novo 按钮菜单

正常启动
BIOS 设置
启动菜单
系统恢复
```

选择：

```
启动菜单
→ USB HDD
```

---

## 3. 安装 Windows

Windows 安装程序启动。

选择：

```
语言
键盘
现在安装
```

当询问产品密钥时：

如果笔记本原本带有 Windows：

```
我没有产品密钥
```

Windows 通常会在之后自动激活，因为密钥存储在固件中（OEM）。

---

## 4. 磁盘分区

进行全新安装时：

在：

```
你想将 Windows 安装在哪里？
```

你会看到：

```
驱动器 0 分区 1
驱动器 0 分区 2
...
```

如果你想完全重装：

删除所有分区：

```
删除 → 驱动器 0
```

然后：

```
驱动器 0 未分配空间
→ 下一步
```

Windows 会创建：

```
EFI 系统分区
MSR
Windows 分区
恢复分区
```

如果是双系统，不要删除现有分区。

---

## 5. Windows 启动后

安装联想驱动程序：

[联想支持驱动](https://pcsupport.lenovo.com?utm_source=chatgpt.com)

安装：

* 芯片组驱动
* Intel/AMD 显卡驱动
* 无线网卡/蓝牙驱动
* 触摸板驱动
* Lenovo Vantage

你也可以运行：

```powershell
winget upgrade --all
```

---

## 常见小新问题

### U 盘无法识别

进入 BIOS：

```
F2
```

检查：

```
启动模式：
UEFI

USB 启动：
启用
```

有些型号有：

```
安全启动 → 暂时禁用
```

---

### 安装时 SSD 不可见

最近的联想笔记本通常使用 Intel VMD/RST。

症状：

```
未找到驱动器
```

解决方法：

BIOS 中：

```
配置
→ Intel VMD 控制器
→ 禁用
```

或者在安装过程中加载 Intel 存储驱动。

---

### 中文 Windows 切换为英文 Windows

你可以直接安装英文版 Windows。安装后：

```
设置
→ 时间和语言
→ 语言
→ 添加英语
```

---

对于大多数联想小新型号（Air/Pro/14/15/16），最快的方法是：

```
创建 Windows 11 GPT U 盘
        ↓
按 Novo 按钮
        ↓
启动 U 盘
        ↓
删除旧分区
        ↓
安装 Windows
        ↓
安装联想驱动
```

如果你告诉我具体型号（例如 **小新 Pro 14 2022 / 2023 / 2024，Intel 或 AMD**），我可以给出确切的 BIOS 按键和驱动步骤。