---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WSL 2 需要手动设置吗？
translated: true
type: note
---

问题：**在安装 WSL 2 之前，我们需要手动启用 Windows Linux 功能吗？**

答案：

是的，从概念上讲，**WSL 2 需要启用 Windows 功能**，但在现代 Windows 上，命令：

```powershell
wsl --install
```

会自动完成这些操作：

* 启用 **Windows Subsystem for Linux**
* 启用 **Virtual Machine Platform**
* 安装 WSL 2 Linux 内核
* 将 WSL 2 设置为默认版本
* 安装 Ubuntu

因此，您通常**不需要打开 Windows 功能 GUI**。

---

如果您想手动操作：

1. 按下：

```
Win + R
```

2. 运行：

```
optionalfeatures.exe
```

3. 启用：

✅ **Windows Subsystem for Linux**

✅ **Virtual Machine Platform**

像这样：

```
[✓] Windows Subsystem for Linux
[✓] Virtual Machine Platform
```

然后重启。

---

重启后：

以管理员身份打开 **PowerShell**：

```powershell
wsl --set-default-version 2
```

然后安装 Linux：

```powershell
wsl --install -d Ubuntu
```

---

对于 Windows 11，还要确保 CPU 虚拟化已启用：

任务管理器 → 性能 → CPU：

```
Virtualization: Enabled
```

如果显示 Disabled，请启用：

* Intel VT-x / Intel Virtualization Technology
* AMD SVM

在 BIOS 中。

对于您的 Lenovo Xiaoxin 14，这通常已经启用，但如果 WSL2 提示虚拟化问题，值得检查一下。
