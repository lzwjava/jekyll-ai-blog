---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows 10 诊断测试
translated: true
type: note
---

问题：**尝试安装 Windows 10 是否有助于诊断或解决联想小新的安装失败问题？**

回答：

是的，尝试安装 Windows 10 实际上是一个合理的诊断步骤，但我会谨慎解读结果。

## 如果 Windows 10 安装成功

那么我们可以了解到：

* SSD 硬件可能没问题 ✅
* 内存可能没问题 ✅
* BIOS/UEFI 配置没问题 ✅
* USB 介质路径没问题 ✅

问题很可能出在 **Windows 11 特有** 的方面，例如：

* Windows 11 安装程序的兼容性检查
* TPM/安全启动的交互问题
* 较新的安装程序行为
* 驱动程序问题（存储/芯片组）

接下来你可以决定：

* 暂时使用 Windows 10
* 之后再升级到 Windows 11

---

## 如果 Windows 10 在相同阶段失败

那么 Windows 版本就不是问题所在。

最可能的原因：

1. U 盘 / ISO 文件问题
2. NVMe SSD 问题
3. 内存问题

因为 Windows 10 和 Windows 11 的安装流程非常相似：

```
WinPE
  |
  v
分区磁盘
  |
  v
应用 install.wim
  |
  v
配置引导加载程序
  |
  v
OOBE
```

在“正在安装 Windows”阶段失败，更指向存储/介质问题，而非操作系统版本问题。

---

## Windows 10 测试的一个优势

Windows 10 ISO 体积更小，有时容错性更好：

Windows 11：

```
install.esd ~5-6GB
+
硬件检查
+
较新的服务堆栈
```

Windows 10：

```
install.wim/esd
+
较旧的安装引擎
```

因此，如果你的 U 盘质量不佳，Windows 10 可能成功，而 Windows 11 却失败。

---

## 我建议的实验顺序

我会这样做：

### 选项 A（最佳诊断）

1. 使用 Rufus 创建 Windows 10 U 盘
2. 安装
3. 观察结果

如果成功：

```
硬件没问题
Windows 11 安装程序问题
```

如果失败：

```
硬件/介质问题
```

---

### 选项 B（仍然比直接切换操作系统更好）

首先创建一个新的 Windows 11 U 盘。

因为你目前已经失败两次，USB 介质有问题的概率仍然很高。

---

对于联想小新，我不认为存在 Windows 11 兼容性问题。过去几年的大多数小新机型都是为 Windows 11 设计的。干净的 UEFI 安装应该可行。

我的猜测：

```
坏的 U 盘/ISO:       60%
NVMe 问题:          25%
内存:               10%
Windows 11 问题:     5%
```

尝试 Windows 10 是一个不错的 **A/B 测试**，但我不会指望它单独就能神奇地修复机器。它之所以有用，主要是结果能告诉我们是否要继续调试硬件还是安装介质。
