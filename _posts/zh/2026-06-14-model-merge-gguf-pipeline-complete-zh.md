---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模型合并GGUF流水线完成
translated: true
type: note
---

全部完成。以下是摘要：

```
╭─ 流水线完成 ───────────────────────────────────────────────────╮
│                                                                 │
│  ✓ 合并:   /mnt/data/zz/finetune/lzw-notes-merged/             │
│  ✓ GGUF:    /mnt/data/zz/finetune/lzw-notes-merged_gguf/       │
│             └── lzw-notes-merged.Q4_K_M.gguf  (2.4 GB)        │
│                                                                 │
│  注意: unsloth 将GGUF保存到 lzw-notes-merged_gguf/               │
│  (而非脚本预期的 lzw-notes-gguf/)                                │
│                                                                 │
│  通过 ollama 提供服务:                                           │
│    1. 创建 Modelfile:                                          │
│       FROM /mnt/data/zz/finetune/lzw-notes-merged_gguf/        │
│           lzw-notes-merged.Q4_K_M.gguf                         │
│       PARAMETER temperature 0.7                                 │
│       PARAMETER num_ctx 4096                                    │
│    2. ollama create lzw-notes -f Modelfile                      │
│    3. ollama run lzw-notes                                      │
│                                                                 │
│  或直接通过 llama.cpp:                                          │
│    llama-cli --model ...Q4_K_M.gguf -p "你的提示"               │
╰─────────────────────────────────────────────────────────────────╯
```

需要我设置ollama模型或用快速推理测试吗？