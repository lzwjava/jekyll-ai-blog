---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X ROCm llama.cpp 已验证
translated: true
type: note
---

全部完成。以下是完整摘要：

---

**通过 SSH 连接到** `root@165.245.137.138` — Ubuntu 24.04，235 GB 内存，611 GB 可用磁盘空间

**检测到 GPU**：**AMD MI300X VF**（设备 `0x74b5`，gfx942）
- 256 GB HBM3，PCIe 5.0 x16（32 GT/s）
- 已安装 ROCm 7.2.0，`rocm-smi` 可识别该 GPU
- `amdgpu` 内核模块已加载（版本 6.16.13）

**llama.cpp 配置**：
1. 将 `https://github.com/ggerganov/llama.cpp.git` 克隆至 `/root/llama.cpp/`
2. 安装 `cmake`（之前缺失）
3. 使用 `-DGGML_HIP=ON -DAMDGPU_TARGETS=gfx942` 构建 — **检测到并编译了 HIP 后端**
4. 将 Qwen2.5-0.5B Q4_K_M（469 MB）下载至 `/root/llama.cpp/models/`

**冒烟测试结果** — 在 MI300X 上通过 ROCm 进行推理：

```
Of course! I am Qwen, a large language model created by Alibaba Cloud...

[ 提示：748.7 t/s  |  生成：484.2 t/s ]
```

**已确认**：HIP/ROCm 后端端到端工作。MI300X 在 llama.cpp 上完全可用于推理。