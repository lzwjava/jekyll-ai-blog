---
audio: false
generated: true
image: false
lang: en
layout: post
title: On-Policy REINFORCE Fine-Tuning on GSM8K
translated: false
type: note
---

This script fine-tunes a pretrained (SFT) chat model on GSM8K math word problems using on-policy policy-gradient RL. As the docstring notes, it's labeled "GRPO" but is really a simplified REINFORCE:

- **No KL regularization** to a reference model (trust region removed)
- **No PPO ratio + clipping** (unnecessary because it's on-policy — each rollout is used exactly once)
- **DAPO-style token-level normalization**: advantage = `reward − mean(reward)` over the samples of one question (no division by std)
- Gradients are scaled by **number of valid tokens** (masked token-level normalization), not by sequence length

## Pipeline overview

### 1. Setup
- CLI args for logging (wandb/mlflow), runtime, model loading, batch sizes, generation params, and per-parameter-group learning rates (embeddings get Adam at 0.2, unembedding Adam at 0.004, matrices get Muon at 0.02 — the NanoChat per-group scheme).
- Loads the SFT model via `load_model("sft", ...)` and wraps it in an `Engine` for batched sampling.

### 2. Rollout generator (`get_batch`)
The core data loop. For each step:
1. Each DDP rank cycles over its own subset of training examples (`rank_indices`), so ranks never duplicate data.
2. Renders the conversation for completion (user + assistant prefix, assistant start token kept, trailing assistant text deleted).
3. Generates `num_samples` completions per question in mini-batches of `device_batch_size` to avoid OOM, with a deterministic per-step seed.
4. **Reward** = `task.reward(conversation, generated_text)` — a GSM8K verifier (checks the model's final answer against the gold answer, e.g. by comparing the last number).
5. Pads all samples to equal length with the `<|assistant_end|>` token (masked in the loss), builds `(inputs, targets)` shifted by one token, sets `targets = -1` (ignore index) wherever the mask is 0 — i.e. **prompt tokens and forced tool-use tokens are excluded from the loss**.
6. **Advantage** = `reward − mean(rewards)` across the `num_samples` samples of that question. Samples that beat the question's average get positive advantage (pushed up), below-average samples get pushed down.

### 3. Evaluation (`run_gsm8k_eval`)
A pass@k evaluator: for each eval question, samples `k = 1..device_batch_size` completions, checks correctness with `task.evaluate`, and accumulates how many questions have at least one correct answer in the top-k. Ranks cooperate over examples; the training loop does the `all_reduce` across ranks and logs `pass@k` to the tracker.

### 4. Training loop
Per step, for each example assigned to this rank:

1. **Policy-gradient objective**: compute per-token log-probs `logp = -model(...)` (negate NLL), then
   `pg_obj = Σ (logp · advantage)` over all tokens, normalized by:
   `num_valid_tokens × num_passes × examples_per_rank` — this is the masked token-level normalization (DAPO-style), which makes the effective learning rate per token uniform regardless of sequence length.
2. `loss = -pg_obj; loss.backward()` accumulates gradients across all examples and passes (no optimizer step in between — gradients from the whole step's rollouts are summed).
3. **LR schedule**: linear decay from `init_lr_frac × base_lr` down to 0 over `num_steps`.
4. `optimizer.step()` then `zero_grad`.
5. Logs mean reward / mean generated sequence length (averaged across ranks), and the master process saves checkpoints every `save_every` steps.

## Why it works / key design choices

| Choice | Rationale |
|---|---|
| On-policy, single use of each rollout | No importance-sampling ratio needed, no clip — simplest stable PG update |
| Advantage = r − μ (no σ) | DAPO: normalizing by std can amplify noise when sample variance is small |
| Token-level normalization | Long sequences don't dominate the gradient; each valid token contributes equally |
| Reward from a verifier, not a learned reward model | GSM8K answers are checkable, so reward is exact and cheap |
| Ignore-index masking | Model is never trained on the prompt or forced tokens, only its own generated reasoning |
| Gradients accumulate over a full step | Effective batch = `examples_per_step × num_samples` sequences before each optimizer step |

## Quick reference
- Run single GPU: `python -m scripts.chat_rl`
- Run 8 GPUs: `torchrun --standalone --nproc_per_node=8 -m scripts.chat_rl -- --run=default`
- Key knobs: `--num-samples` (samples per question, sets the advantage group size), `--examples-per-step` (total questions per step), `--temperature`/`--top-k` (exploration), `--max-new-tokens` (rollout length cap).

One notable simplification to be aware of: it saves checkpoints with `model.state_dict()` but **not the optimizer state**, so resuming mid-training restarts the LR schedule from scratch.