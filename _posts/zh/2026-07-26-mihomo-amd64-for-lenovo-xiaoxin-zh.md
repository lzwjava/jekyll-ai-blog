---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mihomo amd64 适用于联想小新
translated: true
type: note
---

问题：**我应该在联想小新14的Windows 11上下载哪个Mihomo版本？**

答案：

对于**联想小新14 + Windows 11**，几乎肯定选择：

```
mihomo-windows-amd64-alpha-3a779dd.zip
```

原因：

* 联想小新14采用 Intel/AMD x86-64 CPU（Core i5/i7、Ryzen 等）
* 这些笔记本上的 Windows 11 是 **64位 x86**
* `amd64` 代表 **x86-64 架构**，并非仅限 AMD

因此：

✅ 推荐：

```
mihomo-windows-amd64-alpha-3a779dd.zip
```

---

请避免以下版本：

### ❌ arm64

```
mihomo-windows-arm64-alpha-3a779dd.zip
```

仅适用于：

* 搭载骁龙处理器的 Windows 笔记本
* Microsoft Surface Pro X
* 基于 ARM 的 Windows 设备

你的联想小新并非 ARM 架构。

---

### ❌ 386

```
mihomo-windows-386-alpha-3a779dd.zip
```

旧版 32 位 Windows。

Windows 11 通常不会运行纯 32 位系统。

---

### 那 amd64-v1/v2/v3 呢？

例如：

```
mihomo-windows-amd64-v1-alpha.zip
mihomo-windows-amd64-v2-alpha.zip
mihomo-windows-amd64-v3-alpha.zip
```

这些是基于更新的 x86 CPU 指令集优化后的构建版本。

为了最大兼容性：

```
mihomo-windows-amd64-alpha-3a779dd.zip
```

是安全的选择。

如果你想优化：

* 第10代 Intel+ / Ryzen 3000+ 通常支持 v3
* 较旧的 CPU 可能不支持

检查方法：

```powershell
wmic cpu get name
```

或：

```powershell
Get-CimInstance Win32_Processor | Select Name
```

---

下载后：

```powershell
Expand-Archive mihomo-windows-amd64-alpha-3a779dd.zip
cd mihomo-windows-amd64-alpha-3a779dd
.\mihomo.exe -v
```

预期输出：

```
Mihomo Meta version ...
```

然后将你的配置文件：

```
config.yaml
```

放在：

```
mihomo.exe
```

旁边。

运行：

```powershell
.\mihomo.exe -d .
```

对于联想小新14，正常选择就是：

```
✅ mihomo-windows-amd64-alpha-3a779dd.zip
```