---
audio: false
generated: true
image: false
lang: en
layout: post
title: Adding MLflow Logger and CLI Support
translated: false
type: note
---

All done. Here's what was added:

**Files changed on lzw@192.168.1.36:**

1. **`/mnt/data/nanochat/nanochat/mlflow_logger.py`** (new) — `MLflowLogger` class with same `.log()` / `.finish()` interface as wandb/DummyWandb. Logs numeric metrics via `mlflow.log_metrics()`, string values as tags, config as params.

2. **`/mnt/data/nanochat/scripts/base_train.py`** — Added `--tracker {wandb,mlflow,none}`, `--mlflow-uri`, `--mlflow-experiment` args. Removed top-level `import wandb` (now lazy in else branch).

3. **`/mnt/data/nanochat/scripts/chat_sft.py`** — Same tracker args, same pattern.

4. **`/mnt/data/nanochat/scripts/chat_rl.py`** — Same tracker args, same pattern.

5. **`/mnt/data/nanochat/pyproject.toml`** — Added `mlflow>=2.20.0` to dependencies.

**Usage:**

```bash
# Default wandb (unchanged behavior)
python -m scripts.base_train --run=my-run

# MLflow with local file store
python -m scripts.base_train --run=my-run --tracker mlflow

# MLflow with remote server
python -m scripts.base_train --run=my-run --tracker mlflow --mlflow-uri http://localhost:5000

# No tracker at all
python -m scripts.base_train --run=my-run --tracker none

# View results
mlflow ui --port 5000
```

**Xiaomi API key** was also fixed on the remote — now matches this machine's key (51 chars, `tp-cfmiit9...`).
