---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Wimlib SWM Windows 11 USB安全
translated: true
type: note
---

问题：**在 Mac 上使用 wimlib 分割的 `.swm` 方法刷写 Windows 11 USB 是否安全？**

回答：**是的，安全。** 这实际上是从 macOS 创建 Windows 11 安装 U 盘最干净的方法之一。

关键点：你**并没有修改 Windows 本身**，只是更改了 U 盘的布局：

原始 ISO：

```
sources/
 └── install.wim  (7.1GB)
```

FAT32 限制：

```
最大单文件大小 = 4GB
```

因此 wimlib 会转换：

```
install.wim
      |
      v
install.swm
install2.swm
```

示例：

```
sources/
 ├── boot.wim
 ├── install.swm
 └── install2.swm
```

Windows 安装程序原生支持此格式。

安装过程中：

```
USB
 |
 |  读取 install.swm 分块
 |
 v
Windows 安装程序
 |
 v
展开映像
 |
 v
C:\Windows
```

无性能差异。无激活问题。无驱动差异。

---

对于联想小新，这种方法实际上更优，因为：

1. **UEFI 启动兼容性**

你创建的是：

```
GPT 分区表
+
FAT32 文件系统
+
EFI 启动文件
```

与现代联想固件匹配。

2. **避免 NTFS 启动 hack**

有些工具会创建：

```
NTFS U 盘
+
UEFI:NTFS 加载器
```

Rufus 可以做到这一点，但部分笔记本的固件存在 quirks。FAT32 是最通用的方案。

3. **与微软官方安装程序兼容**

微软自身在部署场景中支持分割 WIM 文件（`.swm`）。

---

在重装系统之前，建议检查一项：

进入联想 BIOS：

通常方法：

```
关机
↓
反复按 F2
↓
BIOS 设置
```

查找：

```
Configuration
    Intel VMD Controller
        Enabled
```

更改为：

```
Intel VMD Controller = Disabled
```

或：

```
SATA Mode
    AHCI
```

保存：

```
F10
```

然后从 U 盘启动：

```
F12
→ UEFI USB
```

---

你的错误：

```
0xC19001F4
```

更可能是存储/控制器/升级状态的问题，而非 U 盘创建方法的问题。

诊断逻辑：

| 测试                                        | 结果                     | 含义                     |
| ------------------------------------------- | ------------------------ | ------------------------ |
| 新制作的 FAT32 + wimlib U 盘                | 安装成功                 | 旧 U 盘/映像问题         |
| 新 U 盘仍然失败                             | BIOS/存储问题            |                          |
| 禁用 VMD 后修复                            | Intel RST 驱动问题       |                          |
| Windows 10 可用但 Windows 11 不行           | Win11 兼容性/驱动问题    |                          |

因此，请继续使用 wimlib 刷写。这是一个很好的下一步。**不建议为此 ISO 使用 Etcher**。
