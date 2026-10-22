---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 添加了CUDA GPU和GGUF支持
translated: true
type: note
---

完成。位于 `lzw@192.168.1.137:~/mini-llama.cpp` 的所有更改均已提交并推送：

- **`.gitignore`**：添加了 `mini-llama-gpu`（之前未被跟踪的编译后 ELF 二进制文件）
- **`Makefile`**：添加了用于 GPU 构建的 nvcc 目标
- **`src/gguf.c`、`src/gguf.h`**：GGUF 文件解析
- **`src/gpu_mm.cu`**：通过 cuBLAS 进行 GPU 矩阵乘法

提交 `a835b6c` — `feat: add CUDA GPU attention with gguf loader` 已推送到 GitHub 上的 `origin/main`（5 个文件，+315/-6）。

注意：该分支的上游跟踪已丢失（`based on 'origin/main', but the upstream is gone`）。由于推送目标是新建的远程 `main` 分支，你可能需要在本地重新关联：

```bash
git branch --set-upstream-to=origin/main main
```