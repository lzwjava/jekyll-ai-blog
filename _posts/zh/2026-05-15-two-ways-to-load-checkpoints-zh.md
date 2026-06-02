---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 加载检查点的两种方法
translated: true
type: note
---

有两种情况，具体取决于你下载的是哪种检查点。

## 1. OpenAI GPT-2 权重（已支持）

`model.py:229`（`GPT.from_pretrained`）已封装了 HF Transformers，因此只需运行：

```bash
python sample.py --init_from=gpt2          # 或 gpt2-medium / gpt2-large / gpt2-xl
```

首次运行时会自动将权重拉取到 `~/.cache/huggingface/` 目录下。需要安装 `transformers`。仅适用于这四个模型名称，因为 `from_pretrained` 中的键映射是硬编码为 GPT-2 的。

## 2. 上传到 HF 的 nanoGPT 风格 `ckpt.pt`

类似 Karpathy 的复现版或社区 124M/350M 运行结果，通常是一个原始的 `torch.save({'model': ..., 'model_args': ...})` 字典（即 `train.py` 写入的内容）。下载后，将 `sample.py` 指向该目录：

```bash
pip install huggingface_hub
huggingface-cli download <user>/<repo> ckpt.pt --local-dir out-hf

python sample.py --init_from=resume --out_dir=out-hf --start="Hello"
```

`sample.py:35-46` 会加载 `<out_dir>/ckpt.pt`，构建 `GPTConfig(**checkpoint['model_args'])`，并调用 `load_state_dict`。因此，仓库必须发布一个兼容的 `ckpt.pt`，且同时包含 `'model'` 和 `'model_args'` 键。如果只有 `'model'`，你需要在构建 GPT 时自行传入配置（n_layer、n_head、n_embd、block_size、vocab_size）。

## 3. Hugging Face `transformers` 检查点（safetensors / pytorch_model.bin）

这些检查点使用的参数名称和布局与 nanoGPT 不同。最干净的做法是：逆转 `model.py:229-280` 中的映射关系。该代码负责将 HF → nanoGPT 的键进行复制（转置 Conv1D 权重）。你可以编写逆向映射，将任意 GPT-2 架构的 HF 模型加载到 nanoGPT 中——同样的技巧适用于任何真正具有 GPT-2 形状（相同的 n_layer/n_head/n_embd，相同的 tokenizer）的模型。不同的架构（LLaMA、Mistral 等）则无法加载。

如果你告诉我你想运行哪个具体的 HF 仓库，我可以给你精确的命令。
