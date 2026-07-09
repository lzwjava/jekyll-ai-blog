---
audio: false
generated: true
image: false
lang: en
layout: post
title: Keeping Idle GPU Busy
translated: false
type: note
---

RTX 4070, 12GB — sitting at **0% util**, P8 idle state, 13W of 215W. llama-server is using ~5.9GB but doing nothing (idle). ~4.8GB free.

Here are the useful ways to keep it busy, ranked by what aligns with your stack:

---

### 1. Batch inference / evaluation (most practical)

If llama-server is just sitting there, point work at it. Run eval harness on your models, or batch-process datasets through the server.

```bash
# Point llama-server at eval tasks
# Or run batch inference on a dataset
curl http://localhost:8080/v1/chat/completions \
  -d '{"model":"gemma-4","messages":[{"role":"user","content":"hello"}],"max_tokens":100}' > /dev/null
```

You could set up a cron job that runs eval harness nightly:

```bash
# ~/.hermes/cron/ or system cron
hermes cron create --name "nightly-eval" --schedule "0 2 * * *" \
  --prompt "Run lm-eval-harness on /mnt/data/models/gemma-4-... and report results"
```

### 2. Background LLM serving (it already is, but tune it)

llama-server at P8 with 0% util means it's loaded but nothing's querying it. If you want it to be *usefully* busy — serve your CLI agents (`ww`, `zz`) through it instead of OpenRouter. That saves tokens and keeps the GPU warm.

### 3. LoRA fine-tuning (unsupervised)

Train a LoRA adapter on a dataset you care about while you sleep:

```bash
# unsloth + TRL — fits in 12GB easily
python3.11 -m unsloth.train \
  --model /mnt/data/models/gemma-4-E4B-it-Q3_K_M.gguf \
  --dataset your-dataset \
  --output_dir /mnt/data/lora-runs/cool-experiment
```

4.8GB free is tight for full GPT-2 124M+ training, but LoRA/Q-LoRA on smaller models fits easily.

### 4. Fold@home / BOINC (altruistic compute)

If you want zero-effort background busy:

```bash
# Folding@home — contributes to protein folding research
apt install -y foldingathome
FAHClient --user=lzw --team=0 --gpu=true
```

Sips ~50W, runs at low priority, doesn't interfere with interactive work.

### 5. Dataset generation / synthetic data

Generate synthetic training data using the idle GPU:

```bash
# Feed a large prompt list through llama-server batch API
# Generate QA pairs, preference data, code examples
python3.11 << 'EOF'
# Read prompts from file, send batch to local llama-server
# Store results as JSONL
EOF
```

---

What kind of "busy" are you after?

- **Useful busy** — batch inference, eval, dataset gen, LoRA training
- **Background busy** — Folding@home/BOINC, continuous eval benchmarks
- **Benchmark busy** — burn it with stress tests to verify stability

Pick a mode and I can wire it up with the right commands + cron integration.
