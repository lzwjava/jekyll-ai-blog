---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复MODS GPU测试命令错误
translated: true
type: note
---

**问题：** 这个 MODS GPU 测试错误是什么意思，如何修复？

**回答：**

屏幕上显示的是 MODS（NVIDIA GPU 诊断工具）运行时的无效命令行，导致出现**错误代码 0x000000005（错误的命令行参数）**。

**错误原因：**

使用的命令是：

```
./mods gputest.js -skip_rm_state_init -notest -notest
```

存在两个问题：

1. **`-notest` 被重复传递了两次** —— MODS 警告：*"出现多个 '-notest' 但未设定 PARAM_MULTI_OK，将仅处理最后一个"*
2. **无效的测试模式 0** —— 错误提示必须使用 `-mfg`、`-slt` 或 `-oqa` 之一来指定有效的测试模式。运行时未包含这些模式标志会导致失败。

**修复方法：**

使用有效的测试模式标志。例如：

```bash
# 生产模式
./mods gputest.js -skip_rm_state_init -mfg

# SLT（系统级测试）模式
./mods gputest.js -skip_rm_state_init -slt

# OQA 模式
./mods gputest.js -skip_rm_state_init -oqa
```

- 删除重复的 `-notest` 标志。
- 根据测试场景（生产线、系统测试或质量验证）从 `-mfg`、`-slt`、`-oqa` 中**选择其一**。

红色 "FAIL" 图标确认测试因参数错误未成功运行 —— 并非硬件故障。

**参考：**

- [NVIDIA MODS 文档](https://developer.nvidia.com/mods)
