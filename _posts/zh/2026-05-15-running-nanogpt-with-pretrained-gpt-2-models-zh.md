---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用预训练GPT-2模型运行nanoGPT
translated: true
type: note
---

你需要先安装 `transformers`。一行命令搞定：

```bash
cd /mnt/data/nanoGPT
source venv/bin/activate
pip install transformers
python sample.py --init_from=gpt2-medium --start="Hello, my name is" --num_samples=3 --max_new_tokens=200
```

这就行了。`sample.py:47-49` 将 `--init_from=gpt2*` 路由到 `GPT.from_pretrained`，该方法内部调用 `transformers.GPT2LMHeadModel.from_pretrained('gpt2-medium')`（`model.py:260`）。首次运行会下载约 1.4 GB 的权重到 `~/.cache/huggingface/`，后续运行会复用这些文件。

其他有效取值：`gpt2`（124M）、`gpt2-medium`（350M）、`gpt2-large`（774M）、`gpt2-xl`（1558M）。

常用参数：
- `--device=cuda`（默认）或 `--device=cpu`
- `--temperature=0.8 --top_k=200`（采样）
- `--start="FILE:prompt.txt"` 从文件读取提示