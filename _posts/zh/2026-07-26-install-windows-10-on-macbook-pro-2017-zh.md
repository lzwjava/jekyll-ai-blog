---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在MacBook Pro 2017上安装Windows 10
translated: true
type: note
---

问题：**对于MacBook Pro 2017，如何从`/home/lzw/Downloads/Win10_22H2_English_x64v1.iso`安装Windows 10？**

回答：

对于**MacBook Pro 2017（Intel）**，最佳方法是使用**Boot Camp助理**，而非手动创建USB。苹果官方支持通过Boot Camp在Intel Mac上安装Windows 10。（[Apple支持][1]）

你的ISO文件：

```
/home/lzw/Downloads/Win10_22H2_English_x64v1.iso
```

是Linux路径。如果该文件当前在你的Ubuntu系统上，请先将其复制到Mac。

示例：

```bash
scp Win10_22H2_English_x64v1.iso user@mac:/Users/user/Downloads/
```

然后在macOS上：

## 1. 检查ISO

打开终端：

```bash
ls -lh ~/Downloads/Win10_22H2_English_x64v1.iso
```

你应该会看到一个约5-6 GB的文件。

## 2. 打开Boot Camp助理

macOS：

```
应用程序
 └── 实用工具
      └── Boot Camp助理
```

运行：

```text
继续
```

选择：

```
ISO映像：
~/Downloads/Win10_22H2_English_x64v1.iso
```

Boot Camp将：

1. 创建BOOTCAMP分区
2. 下载Apple Windows驱动程序
3. 启动Windows安装程序

（[Apple支持][1]）

## 3. 分区大小

对于2017款MacBook Pro：

最低：

```
Windows：64 GB
```

推荐：

```
Windows：100-150 GB
```

因为Windows更新会占用空间。

## 4. Windows安装程序

当Windows设置界面出现时：

选择：

```
BOOTCAMP
```

分区。

点击：

```
格式化
```

然后：

```
下一步
```

**不要**删除EFI/APFS分区。

## 5. 安装Boot Camp驱动程序

第一次启动Windows后：

运行：

```
D:\BootCamp\Setup.exe
```

或等待自动安装程序。

这将安装：

* WiFi
* 触控板
* 键盘
* AMD/NVIDIA显卡
* Thunderbolt
* Apple键盘快捷键

（[Apple支持][1]）

---

### 如果你的MacBook Pro 2017当前只有Ubuntu

鉴于你之前提到你的MacBook Pro 2017正在运行Ubuntu，并且Linux内核实验导致无法启动，你有两个选择：

### 选项A（推荐）：先重新安装macOS

启动：

```
Command + R
```

互联网恢复：

```
磁盘工具
→ 将SSD擦除为APFS
→ 重新安装macOS
```

然后使用Boot Camp。

### 选项B：直接安装Windows

可行，但更困难：

* 创建GPT/UEFI Windows USB
* 手动安装Apple Boot Camp驱动程序
* 修复键盘/触控板/WiFi

对于2017款MacBook Pro，使用Boot Camp会顺畅得多。（[Apple支持][1]）

---

你的流程应为：

```
Ubuntu
  |
  | 复制ISO
  v
macOS恢复
  |
  v
macOS
  |
  v
Boot Camp助理
  |
  v
Windows 10 22H2
```

这也是一个很好的诊断：如果Windows 10安装成功，那么你的Mac硬件（SSD/RAM/UEFI）很可能没有问题。

[1]: https://support.apple.com/en-ke/guide/bootcamp-assistant/-bcmp173b3bf2/mac?utm_source=chatgpt.com "在更新的Mac上使用Boot Camp安装Windows - Apple支持（KE）"
