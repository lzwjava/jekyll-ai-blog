---
audio: false
generated: true
image: false
lang: en
layout: post
title: Smoke Test Running, Then Full Run
translated: false
type: note
---

Smoke test is **already running** in a tmux session named `grpo` (I killed a duplicate process from the earlier aborted call). Commands for you:

```bash
# 1. watch the smoke test (already running in tmux session 'grpo')
tail -f /mnt/data/zz/grpo-rl/smoke.log

# or attach to the live session  (detach with: Ctrl-b then d)
tmux attach -t grpo
```

First run downloads `Qwen/Qwen2.5-1.5B` (~3.1 GB) into `~/.cache/huggingface`, then runs 2 optimizer steps.

Once the smoke test prints `Done - LoRA adapter saved`, start the real run:

```bash
tmux new-session -d -s grpo-full -c /mnt/data/zz/grpo-rl \
  './run.sh --num-epochs 2 2>&1 | tee full.log'

tail -f /mnt/data/zz/grpo-rl/full.log     # monitor
tmux attach -t grpo-full                  # or attach
```

Useful overrides (all flags are in `train_grpo.py --help`):

```bash
./run.sh --model Qwen/Qwen2.5-3B --grad-accum 8     # scale up, still fits 12 GB
./run.sh --dataset gsm8k                            # real word problems (cached locally)
./run.sh --beta 0.005 --temperature 1.2             # if reward plateaus
./run.sh --resume                                   # continue from last checkpoint
```

Watch VRAM in a third pane with `watch -n1 nvidia-smi` — if you OOM, lower `--max-completion-length` to 256 or `--num-generations` to 2.

Files created in `/mnt/data/zz/grpo-rl/`:

| file | purpose |
|---|---|
| `train_grpo.py` | GRPO trainer, argparse CLI, fixed for TRL 1.13 |
| `run.sh` | real training config (`smoke` mode included) |
| `setup_env.sh` | venv creation + deps (already executed) |
| `requirements.txt` | pinned versions |

Three fixes vs. the original snippet, in case you care while it runs:
1. `max_prompt_length` no longer exists in TRL 1.13, and `torch_dtype`/`eval_strategy` were renamed — the script uses the current API.
2. Rewards are now **two functions** (`reward_format`, `reward_correctness`) so TRL logs them separately — you can see whether gains come from formatting or actual correctness.
3. `prepare_model_for_kbit_training` + `gradient_checkpointing_kwargs={"use_reentrant": False}` were missing; without them QLoRA + checkpointing is unstable. Attention defaults to `sdpa` (flash-attn not installed, and it's unnecessary at 1.5B).