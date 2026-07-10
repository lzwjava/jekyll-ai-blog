---
audio: false
generated: true
image: false
lang: en
layout: post
title: Base Model Code Generation Setup
translated: false
type: note
---

The `chat_cli` uses SFT chat tokens (`<|user_start|>`, `<|assistant_start|>`) that our base model wasn't trained on. For the base model, prompt it directly:

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

Change the `prompt = '...'` line to try different Python prompts. The key params:
- **temperature=0.3** — low for deterministic code, bump to 0.6 for more creative
- **max_tokens=256** — generation length
- **prepend='<|bos|>'** — required for base model generation