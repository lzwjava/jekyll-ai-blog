---
audio: false
generated: true
image: false
lang: en
layout: post
title: MLflow Integration Complete
translated: false
type: note
---

No code changes needed. The integration is already complete in the codebase. Here's why:

**CLI args** (base_train.py lines 43-45): Already defined:

- `--tracker` with choices `wandb|mlflow|none`
- `--mlflow-uri` for remote server
- `--mlflow-experiment` for experiment name

**Init logic** (lines 101-110): Already handles the switch:

```python
if args.tracker == "mlflow":
    wandb_run = MLflowLogger(...)
```

**Training loop**: All logging goes through `wandb_run.log(...)` which works identically for both wandb and the MLflow logger (same interface).

**MLflowLogger class**: Already implements `log()` and `finish()` — numeric metrics get logged, strings become tags, config gets logged as params.

So yes, just adding these three flags to any existing training command is all it takes:

```
--tracker=mlflow --mlflow-experiment=<name> --run=<run-name>
```

Everything else (val_bpb every N steps, train loss every 100 steps, CORE metrics, checkpoints) flows through the same `wandb_run.log()` calls and gets captured by MLflow automatically.
