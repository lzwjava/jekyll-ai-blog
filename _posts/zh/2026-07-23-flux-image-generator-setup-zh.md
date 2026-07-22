---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX图像生成器设置
translated: true
type: note
---

完成！以下是 `flux/` 目录中的内容：

| 文件 | 用途 |
|------|---------|
| `run_flux_schnell.py` | 主脚本 — 下载并生成图像 |
| `requirements.txt` | Python 依赖项（diffusers、torch 等） |
| `README.md` | 完整文档 |

---

### 快速开始

```bash
cd /mnt/data/zz/flux

# 安装依赖
python3 -m pip install --break-system-packages -r requirements.txt

# 使用您的 HF Token 运行
python3 run_flux_schnell.py --token hf_YOUR_TOKEN_HERE
```

### 脚本功能说明

1. **下载** 来自 Hugging Face 的 12B 参数 **FLUX.1-schnell** 模型
2. **生成** 基于文本提示的图像（默认提示：举牌子的猫、赛博朋克街道、奇幻龙）
3. **保存** PNG 文件到 `./outputs/` 目录

### 重要提示

⚠️ 该模型为 **受限访问** — 您必须：
- 访问 https://huggingface.co/black-forest-labs/FLUX.1-schnell
- 点击 **"同意并访问仓库"**
- 在 https://huggingface.co/settings/tokens 创建 Token

然后通过 `--token hf_xxxx` 参数或 `export HUGGING_FACE_HUB_TOKEN=hf_xxxx` 环境变量传入。

### 关键参数

| 参数 | 默认值 | 说明 |
|-----|---------|-------------|
| `prompts...` | 3 个默认提示 | 文本提示 |
| `--token` | 环境变量 | Hugging Face Token |
| `--steps` | 4 | 推理步数（1–4） |
| `--seed` | 0 | 基础随机种子（每个提示自动递增） |

该脚本使用 **bfloat16** + **CPU 卸载** 技术，使 12B 模型能够在有限的显存中运行。Schnell 是蒸馏模型 — 只需 **1–4 步** 配合 `guidance_scale=0.0` 即可生成出色结果。