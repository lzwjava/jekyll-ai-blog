---
audio: false
generated: true
image: false
lang: zh
layout: post
title: M3 CPU 极限运行 Qwen2 推理
translated: true
type: note
---

全部已推送。总结：

## 完成 — `lzw@192.168.1.137` → `github.com/lzwjava/mini-llama.cpp`

**提交 `fad109a`**（11 个文件更改，+591/−18）已变基到远程较新的 `eb4b536` 之上：

```
fad109a feat: M3 - CPU Qwen2 inference: tokenizer + quantized forward pass
eb4b536 chore: remove mini-llama-m2 binary, add to .gitignore   (was on remote)
33853e3 feat: M2 - block dequant (Q5_0/Q8_0/Q4_K/Q6_K) + VRAM upload + real GEMM
```

工作树干净，`main` 与 `origin/main` 同步。

## 问题所在（在你要求提交之前）

1. **里程碑 3 的工作滞留未提交** —— 新的 CPU 推理代码（`tokenizer.c/h`、`qwen2.c/h`、`m3_cpu.c`）未被跟踪，加上 `gguf.c/h`（`tokenizer.ggml.*` 的数组类型 KV、次正规 fp16）和 `quant.c/h`（Q4_K 文件布局的 scale 解包）中的修复。
2. **`mini-llama-m2` ELF 二进制文件被意外提交**到 M2 提交中，随后又被重新构建，在工作树中留下了脏二进制文件。已修复：执行 `git rm --cached`，并补上了 `.gitignore` 的缺口（`mini-llama-m2`/`mini-llama-m3` 之前缺失）。
3. **`make` 构建在 `nvcc` M2 目标上停滞**（sm_52 CUDA 编译）—— 这就是 `make` 看似卡住的原因；CPU 路径本身很快。
4. **两个潜在的构建问题**（不阻塞提交，但标记出来供你下次会话处理）：
   - `Makefile` 没有针对 `m3_cpu.c` 的 CPU 驱动目标，也没有链接 `-lm`，因此 `qwen2.c` 在链接阶段失败：未定义 `sqrtf`、`pow`、`sincosf`、`expf`
   - `quant.c:105` 误导性缩进警告（for 循环 + 单行上的裸 `return 0`）

需要我作为后续工作，把 M3 CPU 目标接入 `Makefile`（加上 `-lm`）吗？
