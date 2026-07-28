---
audio: false
generated: true
image: false
lang: en
layout: post
title: Adjusted Settings for 12GB GPU
translated: false
type: note
---

It worked with adjusted settings. The default values (`max_model_len=4096`, `max_num_batched_tokens=16384`) are too large for the 12GB GPU — they cause warmup peak memory to exceed the budget, making the KV cache formula produce zero blocks.

Here's the working command:

```bash
cd /mnt/data/nano-vllm
python3 -c "
import os
from nanovllm import LLM, SamplingParams

path = os.path.expanduser('~/huggingface/Qwen3-0.6B/')

# Key fix: lower max_model_len and max_num_batched_tokens for 12GB GPU
llm = LLM(
    path,
    enforce_eager=True,
    gpu_memory_utilization=0.95,
    max_model_len=1024,
    max_num_batched_tokens=4096,
    max_num_seqs=128,
)

params = SamplingParams(temperature=0.6, max_tokens=256)
prompts = ['introduce yourself', 'list all prime numbers within 100']

from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained(path)
prompts = [tok.apply_chat_template([{'role':'user','content':p}],
            tokenize=False, add_generation_prompt=True) for p in prompts]

outputs = llm.generate(prompts, params)
for p, o in zip(prompts, outputs):
    print('---')
    print(o['text'])
"
```

### Why the default failed

In `model_runner.py` line 114, the KV cache formula is:

```python
available = total * 0.9 - used - peak + current
```

With defaults (`max_model_len=4096`, `max_num_batched_tokens=16384`), the warmup forward pass creates huge intermediate tensors → **peak memory** skyrockets → formula goes negative → `num_kvcache_blocks = 0` → assertion fails.

### If you want larger context

Try these settings for your 12GB GPU:

| Use case | `max_model_len` | `max_num_batched_tokens` | `max_num_seqs` |
| --- | --- | --- | --- |
| Short prompts | 1024 | 4096 | 128 |
| Medium context | 2048 | 8192 | 64 |
| Long context | 4096 | 16384 | 32 |

The trade-off: longer `max_model_len` means fewer KV cache blocks → fewer concurrent sequences.
