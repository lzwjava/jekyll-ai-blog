---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用更多并行作业重新启动构建
translated: true
type: note
---

是的，完全没有问题——您已经在使用 2 个并行任务（`-j 2`），而这台机器还能承载更多：

**主机规格：**

- **4 个 CPU 核心**
- **7.7 GB 内存**（约 6.0 GB 可用）

**建议：`-j 4`**（每个核心一个任务），不过如果担心内存压力，`-j 3` 是更稳妥的选择。在处理大型 mmq 模板时，每个 `nvcc` 实例可能消耗 1–2 GB 内存，而可用内存为 6 GB——4 个任务虽可运行，但 3 个任务能留出更多余量。

**好消息：** 构建是增量式的——已编译的约 128 个 `.o` 文件会被保留。如果您终止当前构建并以更高并行度重新启动，只有正在编译的 1–2 个 `nvcc` 实例会被丢弃。

您希望我：

1. **终止当前构建**（PID 9650/9651）并用 `cmake --build build -j 4` 重新启动？
2. 还是保留当前构建（毕竟 CUDA 阶段已经完成约 68%，重新启动主要有助于剩余的约 61 个模板实例 + CPU 端二进制文件）？

如果您想重新启动，命令如下：

```bash
ssh lzw@192.168.1.137 '
cd ~/projects/llama.cpp
kill 9651 9650 2>/dev/null  # 停止当前构建
sleep 2
cmake --build build -j 4 2>&1 | tail -50
echo "=== BUILD EXIT DONE ==="
ls -la build/bin/ 2>/dev/null
'
```

要运行吗？（您发话，我就终止并重新以 `-j 4` 启动。）
