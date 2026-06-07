---
audio: false
generated: true
image: false
lang: en
layout: post
title: WandB API Key Length Fix
translated: false
type: note
---

**Question:** In the nanochat training script, how does the `tracker=wandb` parameter work, and why is WandB complaining that the API key format is not 48 characters?

**Answer:**

The `tracker=wandb` argument tells the training script to log metrics, gradients, and samples to Weights & Biases. WandB's complaint about key length suggests you're either using an **old API key format** or an **outdated WandB version**.

## How it works

The script likely initializes WandB early in `scripts/base_train.py`:

```python
if config.tracker == "wandb":
    import wandb
    wandb.init(project="nanochat", config=config)
```

WandB reads your API key from (in order of precedence):
1. `WANDB_API_KEY` environment variable
2. `~/.netrc` file (from `wandb login`)
3. `.wandb` local directory

## The 48-char issue

**WandB changed API key format around mid-2024:**
- **Old format:** 40-character hex string
- **New format:** 48-character alphanumeric string (looks like `wab_<...>`)

If WandB is complaining about 48 chars, it expects the **new format**, meaning your old key is invalid.

## Fix it (3 steps)

**Step 1: Regenerate your key**
```bash
# Log out of old session
wandb logout

# Login again (opens browser, generates new key)
wandb login
```

Paste your new key from https://wandb.ai/authorize (should be 48 chars, starting with `wab_`).

**Step 2: Verify it's saved**
```bash
cat ~/.netrc | grep wandb
# Should show something like: password wab_xxxxxxxxxxxxxxxxxxxxx
```

**Step 3: Or set via env variable**
```bash
export WANDB_API_KEY="wab_xxxxxxxxxxxxxxxxxxxxx"

# Then run training
cd /mnt/data/nanochat && PYTORCH_ALLOC_CONF=expandable_segments:True .venv/bin/python -m scripts.base_train \
  --run=rtx4070-d12-200k \
  --tracker=wandb \
  ...
```

## Alternative: Skip WandB if you just want training

If WandB is slowing you down or adding friction, use `--tracker=none` or comment it out:

```bash
# ... --tracker=none ...
```

Then monitor loss locally via tensorboard, raw logs, or parse the training output.

**Pro tip:** For long runs like 200k iterations, WandB is worth it (checkpoints your run, lets you track across machine restarts). But make sure your key is current — regenerate once and you're good.
