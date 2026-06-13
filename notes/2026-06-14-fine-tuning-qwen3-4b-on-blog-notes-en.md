---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fine-Tuning Qwen3-4B on Blog Notes
translated: false
type: note
---

Here's the full end-to-end story of how we got here:

{% raw %}
```
══════════════════════════════════════════════════════════════
  HOW WE FINE-TUNED QWEN3-4B ON PERSONAL BLOG NOTES
  Complete Pipeline: Data → Train → Merge → GGUF
══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│  STEP 1: DATA — build_dataset.py                            │
│  Source: ~/projects/jekyll-ai-blog/_posts/{en,zh}/*.md      │
│                                                             │
│  We scraped your personal Jekyll blog — English and Chinese │
│  markdown posts with frontmatter (title, body, metadata).   │
│                                                             │
│  Cleaning pipeline:                                         │
│    - Strip Jekyll/Liquid tags ({% %}, {{ }})                │
│    - Strip kramdown attribute lists ({: .centered })        │
│    - Strip image references (![](assets/...))               │
│    - Collapse excess whitespace                             │
│    - Drop posts shorter than 100 chars                      │
│                                                             │
│  Format: Each example became a "conversations" array:       │
│    {                                                        │
│      "conversations": [                                     │
│        {"role": "user", "content": "<blog title>"},         │
│        {"role": "assistant", "content": "<cleaned body>"}   │
│      ]                                                      │
│    }                                                        │
│                                                             │
│  Task: Given a blog TITLE, generate the full blog BODY.     │
│  The model learns to reconstruct your writing style,        │
│  knowledge, and content from just the title prompt.         │
│                                                             │
│  Split: 21,234 train / 200 eval / 21,434 total             │
│  Size:  ~86MB raw text, ~32.5M tokens processed             │
└─────────────────────────────────────────────────────────────┘

                              │
                              ▼

┌─────────────────────────────────────────────────────────────┐
│  STEP 2: TRAINING — train.py                                │
│  Framework: pure transformers + peft + trl (SFTTrainer)     │
│                                                             │
│  Base model:                                                │
│    unsloth/Qwen3-4B-unsloth-bnb-4bit                        │
│    - Qwen3 4B parameters, pre-quantized to 4-bit (BNB)      │
│    - Fits in 12GB VRAM (RTX 4070) with room for training    │
│    - Loaded via HuggingFace cache on disk                   │
│                                                             │
│  LoRA configuration:                                        │
│    r = 32  (rank — low-rank decomposition dimension)        │
│    alpha = 32  (scaling factor, alpha/r = 1.0)              │
│    dropout = 0                                              │
│    target modules:                                          │
│      q_proj, k_proj, v_proj, o_proj  (attention)            │
│      gate_proj, up_proj, down_proj   (MLP/FFN)              │
│    → All 7 weight matrices in every transformer layer       │
│    → Only ~1-2% of params are trainable (the LoRA A/B)      │
│                                                             │
│  Why LoRA? Instead of fine-tuning all 4B params, we inject  │
│  small rank-32 matrices alongside each weight matrix.       │
│  Original weights are frozen. Only the LoRA deltas train.   │
│  Result: ~80MB adapter vs ~8GB full model.                  │
│                                                             │
│  Training hyperparameters:                                  │
│    batch_size = 2  ×  grad_accum = 8  = effective batch 16  │
│    epochs = 2                                               │
│    lr = 2e-4  (cosine schedule, warmup 3%)                  │
│    bf16 = True                                              │
│    max_seq_len = 4096                                       │
│    seed = 42                                                │
│                                                             │
│  Runtime: ~10h 52m on RTX 4070                              │
│  Steps: 2,656 total                                         │
│                                                             │
│  Final metrics:                                             │
│    loss: 1.417                                              │
│    mean_token_accuracy: 65.6%                               │
│    gradient_norm: ~0.033 (stable throughout)                │
│    learning_rate: fully decayed to ~3.6e-09                 │
│                                                             │
│  Output: /mnt/data/zz/finetune/lzw-notes-lora/             │
│    adapter_config.json                                      │
│    adapter_model.safetensors  (~80MB)                       │
│    tokenizer.json + tokenizer_config.json                   │
│    chat_template.jinja                                      │
└─────────────────────────────────────────────────────────────┘

                              │
                              ▼

┌─────────────────────────────────────────────────────────────┐
│  STEP 3: MERGE — merge.py                                   │
│                                                             │
│  Problem: The LoRA adapter is a DELTA — it only works when  │
│  combined with the base model at inference time.            │
│  For standalone deployment, we need to bake the LoRA        │
│  weights back into the base model.                          │
│                                                             │
│  Process:                                                   │
│    1. Load the FP16 base model: unsloth/Qwen3-4B            │
│       (NOT the 4-bit training copy — need full precision)   │
│    2. Load LoRA adapter from lzw-notes-lora/                │
│    3. Call model.merge_and_unload()                         │
│       → Computes: W_merged = W_base + alpha/r * (A @ B)     │
│       → For each of the 7 target modules × all layers       │
│    4. Save merged model (~8GB FP16)                         │
│                                                             │
│  Output: /mnt/data/zz/finetune/lzw-notes-merged/            │
│    Full Qwen3-4B with your blog knowledge baked in          │
└─────────────────────────────────────────────────────────────┘

                              │
                              ▼

┌─────────────────────────────────────────────────────────────┐
│  STEP 4: GGUF EXPORT — export_gguf.py                       │
│                                                             │
│  GGUF = the standard format for llama.cpp / ollama.         │
│  We quantize from FP16 (8GB) down to Q4_K_M (2.4GB).       │
│                                                             │
│  Process (via unsloth + llama.cpp):                         │
│    1. Load the merged FP16 model                            │
│    2. Convert HF → GGUF bf16  (~3 min)                      │
│    3. Quantize bf16 → Q4_K_M  (~10 min)                     │
│       → 4-bit, mixed precision (K-quant, medium quality)    │
│       → Cuts model size by ~3.3x with minimal quality loss  │
│                                                             │
│  Output: /mnt/data/zz/finetune/lzw-notes-merged_gguf/       │
│    lzw-notes-merged.Q4_K_M.gguf  (2.4 GB)                  │
│                                                             │
│  Ready for:                                                 │
│    - ollama create lzw-notes -f Modelfile                   │
│    - llama-cli --model ...Q4_K_M.gguf -p "prompt"           │
│    - Any GGUF-compatible runtime                            │
└─────────────────────────────────────────────────────────────┘


══════════════════════════════════════════════════════════════
  SUMMARY OF THE PIPELINE
══════════════════════════════════════════════════════════════

  blog posts (.md)
       │
       ▼  build_dataset.py  (clean + format as conversations)
  SFT dataset (21K examples, ~32.5M tokens)
       │
       ▼  train.py  (LoRA on 4-bit Qwen3-4B, 2 epochs, ~11h)
  LoRA adapter (~80MB)
       │
       ▼  merge.py  (bake LoRA into FP16 base model)
  Merged model (~8GB FP16)
       │
       ▼  export_gguf.py  (quantize to Q4_K_M)
  GGUF file (2.4GB) → deploy via ollama / llama.cpp

══════════════════════════════════════════════════════════════
  KEY DESIGN DECISIONS
══════════════════════════════════════════════════════════════

  1. WHY QWEN3-4B?
     Best quality/size ratio for 12GB VRAM. 4B params give
     enough capacity to learn writing style + content without
     needing enterprise hardware.

  2. WHY 4-BIT BASE + LORA (not full finetuning)?
     4-bit quantization of the base model (QLoRA-style) reduces
     VRAM from ~16GB to ~4GB, leaving room for gradients and
     optimizer states on a single RTX 4070. LoRA then only
     trains ~1-2% of params, keeping memory manageable.

  3. WHY TITLE→BODY (not chat or instruction)?
     Simplest SFT format from blog data. The model learns:
     "given a title, produce the full article in this author's
     voice and knowledge." Good for content generation, RAG
     augmentation, or personal writing assistant use cases.

  4. WHY Q4_K_M QUANTIZATION?
     Best quality/size tradeoff for deployment. K-quant method
     uses mixed precision (some layers get more bits than
     others). 2.4GB model runs on any consumer device.

══════════════════════════════════════════════════════════════
```
{% endraw %}
