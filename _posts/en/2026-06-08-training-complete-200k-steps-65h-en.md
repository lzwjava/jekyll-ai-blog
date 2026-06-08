---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Training Complete: 200k Steps, 65h"
translated: false
type: note
---

🎉🎉🎉 TRAINING COMPLETE! 🎉🎉🎉

Final stats:

- Step: **200,000 / 200,000** — done!
- Total time: **3,921.91 minutes** (~65.4 hours, ~2.7 days)
- Minimum validation bpb: **0.780026**
- CORE metric: **0.1987**
- Peak memory: **9,435 MiB**

Eval results (interesting):

- hellaswag (10-shot): **41.6%**
- winograd (0-shot): **59.0%**
- winogrande (0-shot): **54.2%**
- boolq (10-shot): **54.8%**
- lambada_openai (0-shot): **34.4%**
- bigbench_cs_algorithms (10-shot): **45.8%**

The sample generations show the model can produce coherent text ("The capital of France is Paris...") but struggles with math reasoning ("5*x + 3 = 13" loops). Checkpoint saved to `/home/lzw/.cache/nanochat/base_checkpoints/d12/model_200000.pt`.

The model is ready for downstream fine-tuning or deployment.
