---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过禁用用户站点修复ABI不匹配
translated: true
type: note
---

一切端到端工作正常。以下是完整情况：

## 发生了什么

**安装成功**（torch 2.9.1+cu128，transformers 4.57.3，flashinfer 0.6.16，sgl-kernel 0.3.21，minisgl 可编辑模式 — 全部位于 `/usr/local/lib/python3.12/dist-packages`）。之前的运行因 `ENOSPC` 失败，仅仅是因为测试架的输出缓冲区在根目录 `/` 遇到了临时的磁盘满状态（现在有 15G 空闲）。

## 发现的真正问题

在运行时，Python 从用户站点加载了 **torch 2.11.0**（`/home/lzw/.local/lib/python3.12/site-packages` — 一个包含 nano_vllm、flash_attn 等的独立环境），这会覆盖项目中的 torch 2.9.1。`sgl_kernel` 0.3.21 的 `common_ops.abi3.so` 是针对 torch 2.9 的 `c10_cuda` ABI 构建的，因此失败并报错：

```
undefined symbol: _ZN3c104cuda29c10_cuda_check_implementationEiPKcS2_ib
```

我通过 `cuobjdump` 确认，sm100 构建是一个包含 **sm_89 cubins** 的胖二进制文件（适用于 RTX 4070），并且 torch 2.9.1 的 `libc10_cuda.so` 导出了所需的符号 — 因此 ABI 不匹配是 *唯一* 的问题。

## 修复

禁用用户站点（项目自身的 `torch<2.10.0` 约束已经预见到了这一点）：

```bash
PYTHONNOUSERSITE=1 /usr/bin/python3.12 ...   # or: /usr/bin/python3.12 -s ...
```

我在 **`/mnt/data/mini-sglang/run_python.sh`** 添加了一个包装脚本，这样你就不必记住它了。

## 验证（全部通过）

- torch 2.9.1+cu128，CUDA 可用，检测到 RTX 4070
- sgl_kernel 导入 + **采样内核在 GPU 上运行** ✓
- flashinfer **paged-KV 预填充在 GPU 上运行** ✓
- `./run_python.sh -m minisgl --help` → MiniSGL 服务器 CLI 正常工作 ✓

⚠️ 一个注意事项：该项目的每个 python 调用都必须使用 `-s` / `PYTHONNOUSERSITE=1`（或 `run_python.sh`），否则 sgl_kernel 会再次出错。用户站点的 torch 2.11 环境保持不变。
