---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GT 730测试用MODS版本
translated: true
type: note
---

**问题：** 测试 GT 730 (GK208/Kepler) 应使用哪个 MODS 版本？

**答案：**

根据研究，以下是版本兼容性说明：

**推荐版本：MODS 367.38.1**

目前有两个公开版本——**367.38.1**（完整包，包含所有工具和文档）和 **400.184**（部分包，仅包含 `mods` 和 `mats` 工具）。367.38.1 版本不支持 Turing 架构显卡，因此对于像 GT 730 这类较老的 Kepler 显卡，**367.38.1 是正确且完整的版本。**

**当前 MODS 400.250 失败的原因：**

您看到的错误：
```
391/gpu_drv/r400/r400_00-626s  No such file or directory
Error Code = 467
```

MODS 400.x 主要面向**较新的 GPU 架构（Turing/Ampere）**。针对 GK208（GT 730）的板级脚本 `r400_00-626s` 在 400.250 版本中缺失或不兼容。

**版本兼容性总结：**

| MODS 版本 | GT 730 (Kepler GK208) | GTX 16xx / RTX (Turing+) |
|---|---|---|
| **367.38.1** | ✅ 完全支持 | ❌ 不支持 |
| **400.184 / 400.250** | ❌ 缺少板级脚本 | ✅ 支持 |

**操作步骤：**

1. 下载 **MODS 367.38.1**（可在 GPU 维修论坛或俄语硬件网站上搜索）
2. 使用 Rufus 制作 FreeDOS 启动 U 盘，解压 MODS 压缩包并将内容复制到 U 盘
3. 重新运行 GPU 测试——在 367.38.1 版本中应能找到 `r400_00-626s` 板级脚本

**参考链接：**
- [Nvidia Modular Diagnostic Software - MODS (rkblog.dev)](https://rkblog.dev/posts/pc-hardware/nvidia-modular-diagnostic-software-mods/)
- [NVIDIA MODS Kernel Driver (GitHub)](https://github.com/NVIDIA/mods-kernel-driver)