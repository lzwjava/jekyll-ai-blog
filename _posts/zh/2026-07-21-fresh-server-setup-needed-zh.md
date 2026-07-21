---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 需要全新服务器设置
translated: true
type: note
---

服务器正在运行，但处于**裸机状态**——没有模型文件，没有 API 服务器，只有 Jupyter Lab。以下是完整情况：

**服务器状态：✅ GPU 运行中**

| 测试项 | 结果 |
|--------|------|
| GPU 计算 (HIP) | ✅ 向量加法通过，48GB VRAM，gfx1100 |
| ROCm 驱动 | ✅ 7.2.1 |
| Jupyter Lab | ✅ 在端口 8888 上运行 (base_url: `/instances/u-9758-811746f0/`) |
| API 端点 | ❌ "实例不可用" — 端口 8000 上无服务 |
| 模型文件 | ❌ 缓存为空，未下载 Qwen3-8B |
| vLLM / API 包 | ❌ 未安装 |

之前成功的 API 调用来自另一个会话。此容器是全新的——它启动 Jupyter，但模型和 API 服务器需要设置。需要我安装 vLLM 并下载 Qwen3-8B 模型来启动 API 吗？