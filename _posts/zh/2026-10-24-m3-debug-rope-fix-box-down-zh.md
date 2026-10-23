---
audio: false
generated: true
image: false
lang: zh
layout: post
title: M3 调试：RoPE 修复，边界框下移
translated: true
type: note
---

## 摘要 — mini-llama.cpp M3 调查/状态

### 发现

**M3（里程碑 3）已 commit 并 push**（`fad109a`，位于 `origin/main`）：tokenizer + Qwen2 CPU forward pass + `m3_cpu.c` driver。

**然后我对 M3 做了端到端验证** —— 它之前从未被构建或运行过。暴露出两个 bug：

1. **乱码输出（根本原因：RoPE 配对方式）**
   - 机器上的参考 `llama.cpp` 生成的是 `"The capital of France is Paris."` ✓
   - 我们的 driver 产生乱码（`));// thá»...ition`），top-5 logits 平坦，约 13–15。
   - 已从参考源码（`ggml-cpu/ops.cpp` + `llama-model.cpp`）确认：**Qwen2 = `LLAMA_ROPE_TYPE_NEOX` = half-split 配对 `(i, i + head_dim/2)`**，其中 `theta_i = pos·base^(−2i/d)`。我们的 `rope_cpu` 配对的是 `(2i, 2i+1)` —— 交错配对，错误。
   - ✅ **修复已应用**（half-split 配对；theta 公式已验证与 ggml 的 `rope_cache_init` 完全一致）。

2. **清理阶段的段错误** —— 生成后在 `tokenizer_free`/堆清理（heap teardown）中崩溃（没有打印 `[cleanup] tokenizer freed`）。很可能是 forward pass 中的堆损坏（heap corruption）（可疑缓冲区：`score` 的大小计算、未使用的 `ctx`）。**仍未解决、未验证** —— 正在用 ASAN 诊断到一半时，事情开始失控。

**构建/代码整洁性修复也已应用，但尚未 commit/push：**

- `Makefile`：添加了 `mini-llama-m3` CPU target（`-lm`）
- `quant.c`：修复 misleading-indentation 警告
- `qwen2.c`：消除 unused-param 警告
- 模型已下载：`~/models/qwen2.5-0.5b-instruct-q8_0.gguf`（675MB，来自 `hf-mirror.com` —— HF 直连被屏蔽）

### 当前紧急状态 ⚠️

**Debian 机器（192.168.1.137）已宕机/不可达** —— ping 不通，SSH 也不通。它是在 GCC 使用 `-fsanitize=address,undefined` 编译时编译器自身发生段错误（内部编译器错误，很可能是 RAM 耗尽）之后消失的。机器很可能已崩溃，或正在剧烈 thrashing（内存抖动）。

### 机器上有丢失风险的内容（未 commit、未 push）

- `src/qwen2.c`（RoPE 修复 + 警告修复）、`Makefile`、`src/quant.c` —— 已 scp 到磁盘 ✅，但 **未 commit**
- 这些源代码改动在本地 Mac 的 `/tmp/ww-m3/` 下是安全的（存在备份副本）

### 后续步骤（等机器恢复后）

1. **首先：commit 待处理的修复**（`git add -A && commit && push`），以免丢失
2. 重新构建 `mini-llama-m3`（普通 `cc -O2`，不带 sanitizers）并重新运行 —— 现在预期会输出 "Paris"
3. 诊断段错误：使用小规模的**代码审查式地址空间检查**，或更轻量的方法（例如仅用 `-fsanitize=address` 加 `-O0`，或添加 guard debug prints），而不是之前压垮机器的重型 UBSan 构建
4. 与参考 logits 对比验证，然后 commit 已验证的修复

需要我继续轮询那台机器，并在它恢复后继续处理吗？
