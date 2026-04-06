---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Llama.cpp段错误故障排除
translated: true
type: note
---

从系统日志分析中，以下是完整情况：

**OOM 终止（03:39）**
IQ3_S 实例因内存耗尽被 OOM-killed —— 虚拟内存 37.5B，实际占用约 14.9GB。这是标准的 systemd-oomd 行为。并非崩溃，只是内存耗尽。

**段错误（均发生在 `libllama.so` 中）**
三个不同进程出现段错误，均在 `libllama.so` 的相同地址偏移 `+231000` 处，且都发生在 CPU 31（核心 47）上。这表明是同一段代码路径——很可能在注意力机制或 KV 缓存处理环节。

段错误发生在以下情况：
- `llama-server`（进程号 79686）—— OOM 之前
- `llama-server`（进程号 79767）—— OOM 之后立即发生
- `llama-cli`（进程号 125576 / 125666）—— IQ2_M 在 04:15 运行时

**根本原因推测：** 相同偏移处重复出现段错误，表明该版本存在实际缺陷，而非硬件问题。可能涉及 gemma4 架构中的 MoE 专家索引，或混合 SWA/non-SWA 层的 Flash Attention 实现。

**建议：**
1. **重新编译 llama.cpp** —— 执行 `git pull && cmake --build .` 获取最新修复
2. **或尝试** 使用 `--no-flash-attn` 参数，观察是否可避免崩溃
3. **监控重现情况** —— 若再次崩溃，则段错误是真正问题，而非内存因素

希望我重新编译，还是先尝试用 `--no-flash-attn` 参数启动？