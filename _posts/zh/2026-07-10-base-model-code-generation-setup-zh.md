---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基础模型代码生成设置
translated: true
type: note
---

`chat_cli` 使用了我们的基础模型未训练过的 SFT 聊天标记（`<|user_start|>`、`<|assistant_start|>`）。对于基础模型，请直接给出提示：

```bash
cd /mnt/data/nanochat && source .venv/bin/activate && python3 -c "
from nanochat.checkpoint_manager import load_model
from nanochat.engine import Engine
import torch

device = torch.device('cuda')
model, tokenizer, meta = load_model('base', device, phase='eval', model_tag='d12')
engine = Engine(model, tokenizer)

prompt = 'def quicksort(arr):'
tokens = tokenizer(prompt, prepend='<|bos|>')
sample, _ = engine.generate_batch(tokens, num_samples=1, max_tokens=256, temperature=0.3)
print(tokenizer.decode(sample[0]))
"
```

修改 `prompt = '...'` 这一行可以尝试不同的 Python 提示词。关键参数：
- **temperature=0.3** — 较低的值用于确定性代码，提高到 0.6 可获得更多创造性
- **max_tokens=256** — 生成长度
- **prepend='<|bos|>'** — 基础模型生成所必需