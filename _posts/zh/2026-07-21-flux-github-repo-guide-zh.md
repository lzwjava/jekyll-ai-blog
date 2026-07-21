---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX GitHub 仓库指南
translated: true
type: note
---

Question: FLUX GitHub 仓库是什么？

Answer:

FLUX 官方仓库是：

[Black Forest Labs FLUX GitHub 仓库](https://github.com/black-forest-labs/flux?utm_source=chatgpt.com)

GitHub:

```bash
git clone https://github.com/black-forest-labs/flux
cd flux
pip install -e ".[all]"
```

它包含 Black Forest Labs 的 **FLUX.1 模型官方推理代码**。 ([GitHub][1])

主要结构：

```text
flux/
├── src/flux/
│   ├── model.py
│   ├── sampling.py
│   ├── util.py
│   └── cli.py
├── demo_st.py
├── demo_gr.py
├── pyproject.toml
└── model_licenses/
```

([GitHub][1])

模型系列：

| 模型            | 用途                     | 许可证                |
| ---------------- | ------------------------ | -------------------- |
| FLUX.1-schnell   | 快速生成                 | Apache 2.0           |
| FLUX.1-dev       | 更高质量                 | 非商业许可证          |
| FLUX.1-Fill      | 图像修补/扩展            | 非商业               |
| FLUX.1-Canny     | 边缘控制                 | 非商业               |
| FLUX.1-Depth     | 深度引导生成             | 非商业               |
| FLUX.1-Kontext   | 图像编辑/上下文生成      | 非商业               |

([GitHub][1])

对于你的 AMD Radeon Cloud 机器（`gfx1100`，48GB VRAM），我建议从 **FLUX.1-schnell** 开始。

典型工作流程：

```bash
# 安装
git clone https://github.com/black-forest-labs/flux
cd flux

python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[all]"
```

从 Hugging Face 下载权重：

```text
black-forest-labs/FLUX.1-schnell
black-forest-labs/FLUX.1-dev
```

([GitHub][1])

然后运行：

```bash
python demo_st.py \
  --name flux-schnell \
  --prompt "a cyberpunk city at night, cinematic lighting"
```

对于 AMD ROCm，更简单的路径通常是：

```
FLUX
  |
  +-- diffusers (HuggingFace)
  |
  +-- ComfyUI
  |
  +-- ROCm PyTorch
```

因为 ComfyUI 有许多优化和工作流程。

你的 48GB VRAM 应该可以轻松处理：

```
FLUX.1-schnell 1024x1024     ✅
FLUX.1-dev 1024x1024         ✅
FLUX LoRA 推理               ✅
FLUX 图像编辑                ✅
```

在这块 AMD GPU 上，有意义的 hackathon 方向是：

```
Qwen3-VL / LLM
        |
        v
 提示词 + 规划代理
        |
        v
      FLUX
        |
        v
 生成的图像/视频素材
```

一个本地多模态创意代理非常适合这套硬件。

[1]: https://github.com/black-forest-labs/flux?utm_source=chatgpt.com "GitHub - black-forest-labs/flux: FLUX.1 模型的官方推理仓库 · GitHub"
