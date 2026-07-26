---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过USB的VMD可疑对象
translated: true
type: note
---

问题：另一位代理说USB是有效的，真正的问题是联想VMD/RST。这个结论正确吗？

答案：

是的——**另一位代理的结论现在比我之前怀疑USB的原因要强得多**。

新信息改变了诊断：

你的USB有：

```
sources/boot.wim       ✅
sources/install.swm    ✅
sources/install2.swm   ✅
sources/install3.swm   ✅
```

这意味着：

* Windows PE 启动 ✅
* 安装环境加载 ✅
* Windows 映像存在 ✅
* 拆分WIM正确 ✅

所以**不要重新制作USB**。

失败很可能发生在镜像部署之后，VMD/RST成为头号怀疑对象。

---

## 为什么VMD会导致这种模式

现代联想笔记本通常配备：

```
BIOS
 |
Intel VMD Controller
 |
NVMe SSD
```

Windows安装程序WinPE有时能看到磁盘，因为它有额外的驱动程序。

但在第一次重启后：

```
Windows已安装
 |
从NVMe启动
 |
未加载Intel VMD驱动
 |
NVMe消失
 |
启动失败
 |
恢复/回滚
 |
0xC19001F4
```

日志顺序匹配：

```
Setup Phase [4]
...
User has requested to launch the recovery environment
...
0xC19001F4
```

失败并非发生在复制阶段，而是发生在向已安装操作系统过渡时。

---

## 首先检查BIOS

在联想小新上：

进入BIOS：

```
F2
```

查找：

```
Configuration
    Storage
        Intel VMD Controller
```

更改为：

```
Enabled -> Disabled
```

或：

```
RST Premium -> AHCI
```

名称因型号而异。

保存：

```
F10
```

然后用同一个USB重新安装。

---

## 但有一个注意事项

在更改VMD之前，检查一件事：

当Windows安装程序显示磁盘列表时：

按下：

```
Shift + F10
```

运行：

```cmd
diskpart

list disk
```

如果看到：

```
Disk 0   512 GB
```

说明WinPE能看到NVMe。

在安装失败后，再次检查：

```cmd
diskpart

list disk
```

如果SSD消失了，那几乎就是VMD驱动问题。

---

## 我更新的概率

在确认USB有效后：

| 原因                      | 概率      |
| ------------------------- | ---------: |
| Intel VMD/RST模式         |         60% |
| EFI/旧分区元数据          |         25% |
| 驱动程序问题              |         10% |
| USB/ISO                   |         <5% |

另一位代理的论点此时更强。

我不会**动USB**。首先更改BIOS中的VMD/AHCI。这是最快的实验，并且不会破坏数据。