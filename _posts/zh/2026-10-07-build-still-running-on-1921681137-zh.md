---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建仍在192.168.1.137上运行
translated: true
type: note
---

构建在 192.168.1.137 上**仍在运行**（我用了 `.137` — 与之前相同的主机；`.37` 可能是笔误）。

来自 `ps aux` 的状态：

- **你原来的命令仍在运行** — PID 9650 于 **16:01** 启动（`bash -c` 包装器）
- `cmake --build build -j 2` → `gmake` → 运行中（PIDs 9651/9653/9656/9894）
- **当前处于 CUDA 编译阶段** — 两个 `nvcc` 进程（PIDs 13014、13032，启动于 16:09）正在编译 `mmq-instance-iq3_s.cu` 和 `mmq-instance-iq3_xxs.cu`

这是 llama.cpp 构建中最慢的部分——它会为 `compute_52` 和 sm_52 循环遍历数百个 CUDA 模板实例（mmq、fa 等）。使用 `-j 2` 时，这个 CUDA 阶段可能需要一段时间。

如果你愿意，我可以继续监控（例如，检查 `build/ggml/src/ggml-cuda` 中已编译的 `.o` 文件数量来评估进度），或者稍后重新检查 `ps`。需要我检查进度百分比吗？
