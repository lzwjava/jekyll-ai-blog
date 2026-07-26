---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在小新14上安装x64 PowerToys
translated: true
type: note
---

问题：**对于联想小新14，我应该安装PowerToys x64.exe还是ARM64.exe？**

回答：

安装 **x64.exe**。

联想小新14笔记本电脑使用**Intel或AMD x86-64 CPU**，而非ARM处理器。正确的架构是：

```
PowerToysSetup-x64.exe
```

**不要**安装：

```
PowerToysSetup-arm64.exe
```

ARM64适用于以下设备：

* Microsoft Surface Pro X
* 搭载骁龙处理器的Windows笔记本
* Windows on ARM设备

您可以确认自己的CPU：

1. 按下 `Win + R`
2. 运行：

```cmd
msinfo32
```

检查：

```
系统类型: 基于x64的电脑
```

或：

```cmd
wmic cpu get name
```

常见的小新14 CPU：

* Intel Core i5/i7 → x64 ✅
* AMD Ryzen → x64 ✅
* 骁龙/ARM → ARM64 ❌

因此，在您的联想小新14上安装Windows时：

```
Windows 10/11 x64
+
PowerToys x64
```

是正确的组合。