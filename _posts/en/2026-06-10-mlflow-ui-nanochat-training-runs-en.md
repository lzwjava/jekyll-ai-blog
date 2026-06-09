---
audio: false
generated: true
image: false
lang: en
layout: post
title: MLflow UI Nanochat Training Runs
translated: false
type: note
---

MLflow UI is up and running. Here's the summary:

---

**MLflow UI: <http://localhost:5001>**

The DB contains your nanochat training runs from the MI300X (amd-cloud). Here's what's inside:

**3 Experiments, 5 Runs:**

| Run Name | Status | Key Metrics (latest step) |
|---|---|---|
| smoke-test | FINISHED | loss: 3.2 (step 1) |
| test-mi300x | FINISHED | loss: 10.40, mfu: 2.8%, tok/s: 7,009 (step 0) |
| test-mi300x-bs64 | FINISHED | loss: 10.40, mfu: 3.4%, tok/s: 8,292 (step 0) |
| mi300x-d24-760m | RUNNING | loss: 3.76, mfu: 27.1%, tok/s: 67,119 (step 200) |
| mi300x-d24-760m-fp8 | RUNNING | loss: 10.40, mfu: 6.8%, tok/s: 16,886 (step 0 only) |

**Model config (d24-760m runs):**

- depth=24, head_dim=128, max_seq_len=2048
- total_batch_size=524288, device_batch_size=32
- matrix_lr=0.02, embedding_lr=0.3, weight_decay=0.28
- warmup_steps=40, warmdown_ratio=0.65

**Fix applied:** The DB was created with mlflow 3.13.0 (from source on amd-cloud), but only 3.1.4 is on PyPI. Patched the alembic_version from `da6fb0208061` → `bda7b8c39065` so the local UI can read it.

Note: the `mi300x-d24-760m` run shows great progress — loss dropped from 10.4 → 4.87 → 3.76 over 200 steps with 27% MFU on MI300X. The fp8 run seems stuck at step 0 with much lower throughput (16k tok/s vs 67k) — possibly a cold start or the fp8 matmul overhead at small scale.
