---
audio: false
generated: true
image: false
lang: en
layout: post
title: Alternatives to Weights & Biases for nanoGPT
translated: false
type: note
---

Question: What are good alternatives to Weights & Biases for experiment tracking, and can they be used with nanoGPT training?

---

## Answer

Yes, several solid alternatives exist depending on your priorities. For nanoGPT training specifically, your best bets are **MLflow** (most flexible) or **Aim** (lighter, better UI), with a hybrid option using both.

### Quick Comparison

MLflow leads in flexibility and self-hosted deployments with strong model registry capabilities and minimal vendor lock-in, while Aim provides lightweight tracking with superior UI/UX for run comparison and visualization. Primary competitors include Neptune.ai, Comet ML, ClearML, and Aim, offering similar experiment tracking functionalities.

---

### **Option 1: MLflow (Recommended for Control)**

Open-source, self-hosted, zero cloud dependency. MLflow Tracking logs data to a local `mlruns` directory by default, with ability to configure remote databases and cloud storage.

**Install:**
```bash
pip install mlflow
```

**Integration with nanoGPT** — modify training loop:

```python
import mlflow
import torch
from model import GPT  # from nanoGPT

mlflow.set_experiment("nanoGPT-baseline")

with mlflow.start_run(run_name="run-1"):
    # Log hyperparameters
    mlflow.log_param("n_layer", 6)
    mlflow.log_param("n_head", 6)
    mlflow.log_param("n_embd", 384)
    mlflow.log_param("learning_rate", 3e-4)
    mlflow.log_param("batch_size", 64)

    model = GPT(config)
    optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)

    for step in range(max_iters):
        logits, loss = model(X, Y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if step % 100 == 0:
            mlflow.log_metric("train_loss", loss.item(), step=step)

    # Save checkpoint
    torch.save(model.state_dict(), "model.pt")
    mlflow.log_artifact("model.pt")
```

View experiments:
```bash
mlflow ui
# Open http://localhost:5000
```

---

### **Option 2: Aim (Recommended for Lightweight Speed)**

Focused on training tracking, with superior UI scalability — can handle thousands of metrics smoothly, outperforming MLflow UI when exploring hundreds of runs. Install:
```bash
pip install aim
```

**nanoGPT integration:**

```python
from aim import Run

run = Run()
run["hparams"] = {
    "n_layer": 6,
    "n_head": 6,
    "n_embd": 384,
    "learning_rate": 3e-4,
}

for step in range(max_iters):
    logits, loss = model(X, Y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if step % 100 == 0:
        run.track(loss.item(), name="train_loss", step=step)
```

View dashboard:
```bash
aim up
# Open http://localhost:43800
```

---

### **Option 3: MLflow + Aim Hybrid (Best UI + Full Control)**

Log with MLflow, visualize with Aim's superior UI. Install aimlflow:
```bash
pip install aimlflow
```

Train with MLflow as shown above, then convert:
```bash
aimlflow sync -m /path/to/mlruns
aim up
```

This gives you MLflow's full artifact/model registry plus Aim's beautiful comparison interface — zero code changes.

---

### **Option 4: Minimal DIY (If You Want Full Autonomy)**

Just log locally to JSON:

```python
import json
from pathlib import Path

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

metrics = {"train_loss": [], "step": []}

for step in range(max_iters):
    loss = ...
    metrics["train_loss"].append(loss.item())
    metrics["step"].append(step)

with open(log_dir / "metrics.json", "w") as f:
    json.dump(metrics, f)
```

Then analyze in Jupyter or plot with matplotlib. Ultra-simple, zero dependencies.

---

### **My Take for Your Workflow**

Given you're on M2 + RTX 4070 workstation with 62GB RAM:

1. **Start with MLflow** — local-first, works everywhere, logging is 5 lines, UI is browser-based
2. **If you find MLflow UI slow** (unlikely for nanoGPT scale), add aimlflow layer for Aim's UI
3. **Skip cloud entirely** — you don't need W&B's collab features for solo training

The `mlruns/` folder stays local, versioned, reproducible. No cloud sync delays, no rate limits, no costs.

---

References:

- https://mlflow.org/docs/latest/ml/tracking/
- https://github.com/aimhubio/aim
- https://aimstack.io/blog/tutorials/exploring-mlflow-experiments-with-a-powerful-ui
- https://medium.com/@bingqian/building-and-tracking-nanogpt-training-in-databricks-with-mlflow-2ce499183881
