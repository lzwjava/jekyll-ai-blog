---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows 安装失败诊断
translated: true
type: note
---

问题：根据 `setuperr.log` 截图检查 Windows 安装失败。

回答：

我已查看截图。关键行如下：

```
CUnattendManager::Initialize(90): Result = 0x80070490
CMOSetupOneSettingsHelper<...>::InitializeSettings(324): Result = 0x80072EE7
CSetupHost::InitializeOneSettings(1606): Result = 0x80072EE7

...
CSetupManager::ExecuteInstallMode(...)
CSetupHost::Execute(564): Result = 0xC19001F4
```

最终错误：

```
0xC19001F4
```

是真正的失败代码。它表示 Windows 安装程序在安装工作流中失败，但仅凭截图**无法**显示原始触发原因。

之前的错误：

```
0x80070490
```

= `ERROR_NOT_FOUND`（安装配置中缺少某个预期内容）

```
0x80072EE7
```

= 名称解析失败（DNS/网络查找失败）

这些通常是**次要的**。关键是安装程序进入了失败路径并回滚。

根据您之前的上下文（联想小新 + USB 安装 + 恢复环境消息），可能的原因如下：

### 1. USB 安装介质方式错误（最可能）

您在 Mac 上使用 FAT32 创建了 USB 并复制了文件。Windows 11 25H2 ISO 包含：

```
sources/install.wim
```

该文件通常大于 4GB。

如果 WIM 分割不正确或 ISO 复制不完整，安装程序可能在后期失败。

检查 USB：

重新启动进入 Windows PE 命令提示符：

```cmd
dir D:\sources
```

您应该看到：

```
install.swm
install2.swm
```

或：

```
install.wim
```

而不是缺失文件。

---

### 2. 磁盘分区状态问题

之前您遇到：

```
partition is of an unrecognized type
selected volume is offline
```

如果联想 SSD 仍包含旧元数据：

打开命令提示符：

```cmd
diskpart

list disk

select disk 0

clean

convert gpt

exit
```

然后重新安装。

**警告：** `clean` 会销毁所有分区。

---

### 3. 与网络相关的安装失败

因为：

```
0x80072EE7
```

出现。

在 Windows 11 安装过程中，避免在线账户设置。

在 OOBE 阶段：

按下：

```
Shift + F10
```

然后：

```cmd
OOBE\BYPASSNRO
```

重新启动并选择：

```
我没有 Internet 连接
```

---

### 接下来我需要什么

截图仅是 `setuperr.log` 的尾部。最有用的部分在前面。

请发送：

```
C:\$WINDOWS.~BT\Sources\Panther\setupact.log
```

大约在首次出现：

```
Error
```

的位置

或运行：

```cmd
findstr /i "error failed rollback 0xc190" setupact.log
```

同时请告诉我：

1. 失败发生在哪个阶段？
   * 复制文件 % 时
   * 安装功能 % 时
   * 首次重启后
   * 最终“正在准备”阶段？

2. 您的 USB 是用什么创建的？
   * `wimlib-imagex split install.wim`
   * Rufus
   * Etcher
   * 手动复制？

我目前的怀疑是：**USB 介质 / install.wim 处理方式或旧 SSD 分区元数据**，而不是恢复环境那一行本身。
