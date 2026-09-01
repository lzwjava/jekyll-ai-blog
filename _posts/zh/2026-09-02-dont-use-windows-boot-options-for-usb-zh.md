---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 不要使用Windows启动选项来引导USB
translated: true
type: note
---

问题：这是什么屏幕，我该如何从这里启动 Debian USB？

回答：这是 **Windows 7 的高级启动选项**，而不是主板 BIOS/启动菜单。

你当前看到的选项包括：

* 修复计算机
* 安全模式
* 启用低分辨率视频
* 调试模式
* 禁用驱动程序签名强制
* **正常启动 Windows**

所以**不要在这里选择任何选项**。按 **Esc** 键退出此菜单。

### 从 USB 启动 Debian

你需要进入 **BIOS/启动设备菜单**，这发生在 Windows 启动*之前*。

1. 完全关闭电脑。
2. 插入你的 Debian USB。
3. 开机。
4. 立即反复按下：

```text
F12
```

如果 F12 不起作用，尝试：

```text
F11
F2
Delete
```

你应该最终会看到类似这样的界面：

```text
启动菜单
------------------
硬盘
USB HDD
CD/DVD
网络
```

选择：

```text
USB HDD
```

或你的 USB 设备的名称。

### 重要区别

```text
开机
   │
   ▼
BIOS / POST
   │
   ├── F12 → 启动设备选择  ← 你需要这个
   │
   ▼
Windows 启动管理器
   │
   └── F8 → 高级启动选项  ← 你当前的屏幕
```

你的照片显示的是 **F8/Windows 引导加载程序阶段**，说明你已经在启动过程中走得太远了。

如果你告诉我**按下电源键后立即按 F12 会发生什么**（或发送一张照片），我可以指导你下一步的具体操作。