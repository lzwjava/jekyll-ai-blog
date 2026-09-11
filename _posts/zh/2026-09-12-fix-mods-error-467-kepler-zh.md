---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 MODS 错误 467（开普勒）
translated: true
type: note
---

**问题：** 当前正在运行 MODS 367.56.4，但仍出现错误 467 "No such file or directory"——这意味着什么以及如何修复？

**回答：**

进展不错——你已按建议切换到 367.x 版本。但仍存在文件缺失问题。以下是详细分析：

**屏幕关键信息：**

| 字段 | 值 |
| --- | --- |
| MODS 版本 | **367.56.4** |
| RM 版本 | `rel/gpu_drv/r367/r367_00-557` |
| gputest.js | 59 个条目 |
| boards.js | 7 个条目 |
| boards.db | 3208 个条目 |

**错误信息：**

```
Error 467 : Global.LoadGoldenValues  No such file or directory
Error 467 : Global.InitializeGpuTests  No such file or directory
```

**这意味着什么：**

MODS 现已正确加载（找到了 r367 驱动 ✅），但无法找到 **"Golden Values"** 文件——该文件包含针对你特定 GPU 板卡 ID 的预期测试结果参考数据。没有此文件，MODS 无法验证 GPU 测试结果。

**值得注意的观察：**

- 存在 `boards_gp102.db`、`boards_gp104.db`、`boards_gp106.db` → 这些是 **Pascal** GPU 板卡数据库
- 但列表中 **没有 `boards_gk208.db`** 或等效的 **Kepler** 板卡数据库
- 这确认你拥有的 367.56.4 软件包是 **Pascal 专用**，而非 Kepler（GT 730）

**你需要的不是任意 367.x 版本，而是特定的 MODS 367.38.1：**

| 版本 | GT 730（GK208 Kepler） |
| --- | --- |
| **367.38.1** | ✅ 包含 Kepler 板卡数据库 |
| **367.56.4**（当前） | ❌ 仅有 Pascal 板卡 |
| **400.x** | ❌ 架构错误 |

**操作步骤：**

1. 查找并下载 **MODS 367.38.1**（非 367.56.4）
2. 解压后确认能看到如下文件：

   ```
   boards_gk208.db  ← 此文件必须存在
   ```

3. 使用该版本重新运行测试

> 💡 版本号至关重要——367.38.1 发布时 Kepler 仍是主要支持的架构，因此包含适用于 GK208 的正确 Golden Values 和板卡数据库。

**参考资料：**

- [Nvidia Modular Diagnostic Software - MODS (rkblog.dev)](https://rkblog.dev/posts/pc-hardware/nvidia-modular-diagnostic-software-mods/)
