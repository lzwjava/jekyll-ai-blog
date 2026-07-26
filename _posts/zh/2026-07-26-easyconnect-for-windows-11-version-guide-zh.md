---
audio: false
generated: true
image: false
lang: zh
layout: post
title: EasyConnect Windows 11 版本指南
translated: true
type: note
---

问题：**在Windows 11上应该安装哪个版本的Sangfor EasyConnect？这两个下载有什么区别？**

回答：

主要区别在于**Sangfor SSL VPN服务器版本的兼容性**，而非Windows版本。

具体如下：

### 1. 适用于M6.9–M7.6.6R1（不含M7.3R4）的EasyConnect

```
适用于M6.9-M7.6.6R1版本（不包含M7.3R4）

支持：
✅ x86 Windows
✅ ARM Windows 8/10
❌ ARM Windows 11
❌ Windows Server

重要提示：
M7.1之前版本不支持win11系统
```

含义：

* 若**公司VPN网关**版本低于M7.1，则此客户端不支持Windows 11。
* 若网关版本为M7.1–M7.6.6R1，则x86架构的Windows 11应可正常工作。

---

### 2. 适用于M7.6.7及以上版本的EasyConnect

```
适用于M7.6.7及以上版本

支持：
✅ x86 Windows
✅ ARM Windows 8/10
❌ ARM Windows 11
❌ Windows Server
```

此为较新版本客户端。

---

## 针对您的设备（联想小新14 + Windows 11）

您的笔记本几乎可以确定是：

```
CPU: Intel/AMD x86_64
操作系统: Windows 11 x64
```

因此您需要：

```
x86 Windows版本
```

而非ARM版本。

具体选择取决于**公司Sangfor网关版本**：

| 公司VPN服务器版本 | 应安装版本                  |
| ----------------- | --------------------------- |
| M7.6.7或更新      | EasyConnect M7.6.7+         |
| M6.9–M7.6.6R1     | EasyConnect 旧版本          |
| 未知              | 先尝试最新版本              |

---

对于Windows 11，我会建议安装：

```
EasyConnect M7.6.7+
```

原因如下：

* 版本较新。
* 明确支持x86架构的Windows 11。
* 包含更多错误修复。

---

您之前反馈的一个重要细节：

您提到：

> EasyConnect在Windows 11上频繁崩溃

这在旧版Sangfor客户端中很常见。旧版EasyConnect基于旧版Windows驱动程序（网络过滤驱动、SSL VPN适配器）。Windows 11改变了驱动签署和网络行为。

如果出现崩溃：

1. 完全卸载旧版EasyConnect：

```powershell
winget uninstall EasyConnect
```

或：

```
设置
 → 应用
 → 已安装的应用
 → EasyConnect
 → 卸载
```

2. 重启电脑。

3. 安装M7.6.7+客户端。

4. 以管理员身份运行一次。

---

同时请检查您的Windows架构：

```powershell
systeminfo | findstr /B /C:"系统类型"
```

预期结果：

```
系统类型: x64-based PC
```

如果显示为ARM64，则这些客户端存在限制（不支持Windows 11 ARM版）。