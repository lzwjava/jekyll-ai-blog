---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Llama-Server 导致的 GPU 内存耗尽
translated: true
type: note
---

是的 — 是 llama.cpp。PID 3148789 是运行 DeepSeek-R1-0528-Qwen3-8B（Q4_K_M）的 `llama-server`，参数为 `-ngl 99`（所有层在 GPU 上），占用了你 12 GiB RTX 4070 中的 **10.6 GiB**。留给 PyTorch 的只有大约 1 GB，这就是为什么一个 14 MiB 的分配会失败——在 PyTorch 启动前 GPU 几乎已经满了。

`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` 在这里帮不上忙。问题不是碎片化，而是另一个进程占用了内存。

可选方案：

1. **停止 llama-server**（如果你不需要它）：`kill 3148789`
2. **在 CPU 或更少的层上运行** —— 将 `-ngl 99` 改为例如 `-ngl 20` 来共享 GPU
3. **使用更小的量化** —— 8B 模型的 Q4_K_M 大约是 5 GB 权重 + KV 缓存；其余是上下文。降低 `-c`（上下文大小）以释放内存
4. **在 CPU 上运行 PyTorch** —— 如果工作负载较小，使用 `device="cpu"`

哪个适合你？如果你想同时运行两者，方案 2 或 3 是答案。