---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 缺少MODS板文件错误
translated: true
type: note
---

**问题：** 这个新的 MODS 错误是什么意思，如何修复？

**回答：**

这是一个与之前**不同的错误**。GPU 硬件初始化问题已经消失——现在是一个**缺少文件错误**。

**屏幕上的系统信息：**

| 字段 | 值 |
| --- | --- |
| MODS 版本 | 400.250 |
| 内核 | 4.17.4-gentoo |
| 内核驱动 | 3.87 |
| SBIOS 版本 | 4.6.5 |
| 主机名 | tinylinux |

**实际错误：**

```
boards.js : 391/gpu_drv/r400/r400_00-626s No such file or directory
Error Code = 0000000467 (No such file or directory)
```

**这意味着什么：**

MODS 正在尝试为 GT 730 加载一个**板卡定义文件**，具体查找的是：

```
r400/r400_00-626s
```

这是 MODS 运行测试所需的 **GPU 驱动配置文件/脚本文件**。它在预期路径中找不到该文件。

**可能的修复方法：**

1. **此 GPU 的 MODS 版本不匹配**
   - MODS 400.250 可能不包含适用于 GK208（GT 730）的正确板卡脚本
   - 尝试使用包含 `r400_00-626s` 的**较旧或匹配的 MODS 版本**

2. **MODS 软件包不完整**
   - MODS 安装可能缺少文件
   - 重新下载/解压完整的 MODS 软件包并验证文件完整性

3. **手动检查 boards 目录：**

   ```bash
   find / -name "r400_00-626s*" 2>/dev/null
   ls ./391/gpu_drv/r400/
   ```

4. **如果文件存在于其他位置，使用正确的脚本路径标志：**

   ```bash
   ./mods gputest.js -skip_rm_state_init --datadir /path/to/correct/dir
   ```

---

> 💡 **关键要点：** 此错误意味着 MODS 现在已**成功与 GPU 通信**（相比之前是进展！），但测试脚本包不完整或与此 GPU 的 PCI 设备 ID（`626s` = GT 730 变体）不匹配。

**参考：**

- [NVIDIA MODS 工具概述](https://developer.nvidia.com/mods)
