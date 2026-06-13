---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Merge GGUF Pipeline Complete
translated: false
type: note
---

All done. Here's the summary:

```
╭─ Pipeline Complete ─────────────────────────────────────────────╮
│                                                                 │
│  ✓ Merge:   /mnt/data/zz/finetune/lzw-notes-merged/            │
│  ✓ GGUF:    /mnt/data/zz/finetune/lzw-notes-merged_gguf/       │
│             └── lzw-notes-merged.Q4_K_M.gguf  (2.4 GB)        │
│                                                                 │
│  Note: unsloth saved the GGUF to lzw-notes-merged_gguf/        │
│  (not lzw-notes-gguf/ as the script expected)                  │
│                                                                 │
│  To serve via ollama:                                           │
│    1. Create Modelfile:                                         │
│       FROM /mnt/data/zz/finetune/lzw-notes-merged_gguf/        │
│           lzw-notes-merged.Q4_K_M.gguf                         │
│       PARAMETER temperature 0.7                                 │
│       PARAMETER num_ctx 4096                                    │
│    2. ollama create lzw-notes -f Modelfile                      │
│    3. ollama run lzw-notes                                      │
│                                                                 │
│  Or via llama.cpp directly:                                     │
│    llama-cli --model ...Q4_K_M.gguf -p "your prompt"            │
╰─────────────────────────────────────────────────────────────────╯
```

Want me to set up the ollama model or test it with a quick inference?
