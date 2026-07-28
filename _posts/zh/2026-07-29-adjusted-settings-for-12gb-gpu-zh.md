---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 针对12GB GPU的调整设置
translated: true
type: note
---

调整设置后即可正常运行。默认值（`max_model_len=4096`、`max_num_batched_tokens=16384`）对 12GB GPU 来说过大——它们会导致预热峰值内存超出预算，使得 KV 缓存公式产生零个块。

以下是可用的命令：

```bash
cd /mnt/data/nano-vllm
python3 -c "
import os
from nanovllm import LLM, SamplingParams

path = os.path.expanduser('~/huggingface/Qwen3-0.6B/')

# 关键修复：针对 12GB GPU 降低 max_model_len 和 max_num_batched_tokens
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

### 默认值失败的原因

在 `model_runner.py` 第 114 行，KV 缓存公式为：

```python
available = total * 0.9 - used - peak + current
```

使用默认值（`max_model_len=4096`、`max_num_batched_tokens=16384`）时，预热前向传播会产生巨大的中间张量 → **峰值内存**急剧上升 → 公式变为负数 → `num_kvcache_blocks = 0` → 断言失败。

### 如果你需要更大的上下文长度

针对你的 12GB GPU，可尝试以下设置：

| 使用场景 | `max_model_len` | `max_num_batched_tokens` | `max_num_seqs` |
|---|---|---|---|
| 短提示词 | 1024 | 4096 | 128 |
| 中等上下文 | 2048 | 8192 | 64 |
| 长上下文 | 4096 | 16384 | 32 |

权衡：更长的 `max_model_len` 意味着更少的 KV 缓存块 → 更少的并发序列数。