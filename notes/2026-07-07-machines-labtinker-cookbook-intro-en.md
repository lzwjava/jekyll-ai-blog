---
audio: false
generated: true
image: false
lang: en
layout: post
title: -machines-lab/tinker-cookbook Intro
translated: false
type: note
---

**Question:** Give me an intro to the `thinking-machines-lab/tinker-cookbook` repo.

**Answer:**

## What it is

Tinker is Thinking Machines Lab's (Mira Murati's lab, with John Schulman — the RLHF/PPO guy) post-training-as-a-service play. There are two libraries: `tinker`, a training SDK where you send API requests and they handle the complexities of distributed training, and `tinker-cookbook`, which builds on the Tinker API with realistic fine-tuning examples and common abstractions.

The core design insight is what makes it interesting for you: **it's not a "submit dataset, get model" fine-tuning API like OpenAI's.** It exposes low-level training primitives over the network, so *you* write the training loop locally while they run the forward/backward on their cluster. You keep algorithmic control; they own the distributed-systems pain (FSDP, pipeline parallelism, preemption recovery).

## The primitive layer

The entire API surface is basically four verbs:

```python
import tinker

service_client = tinker.ServiceClient()
training_client = service_client.create_lora_training_client(
    base_model="meta-llama/Llama-3.2-1B", rank=32,
)

training_client.forward_backward(...)   # compute loss + accumulate grads on their cluster
training_client.optim_step(...)         # apply optimizer update
training_client.save_state(...)         # checkpoint
sampling_client = training_client.save_weights_and_get_sampling_client()
sampling_client.sample(...)             # rollouts for RL / evals
```

That decomposition is the whole trick. Because `forward_backward` and `sample` are separate calls you control, you can implement *any* post-training algorithm on top — SFT, DPO, PPO/GRPO, distillation — just by changing what data you feed and how you compute rewards/losses between calls. It's LoRA-based (note `rank=32`), which is what makes multi-tenant serving of thousands of user fine-tunes economical on their end (shared base weights, per-user adapters).

Compare to your nanochat work: nanochat gives you the full stack but you own the GPUs; Tinker gives you the loop-level control of nanochat with someone else's cluster. You can also download the weights of any model as a checkpoint archive, so it's not a lock-in trap — train there, export, serve on your MI300X.

## What's in the cookbook

The recipes directory is effectively a survey of modern post-training, each runnable:

`sl_loop.py` and `rl_loop.py` are minimal examples of using the primitives, while `sl_basic.py` and `rl_basic.py` show minimal SL/RL configuration. Fuller recipes cover Chat SFT (Tulu3-style), Math RL with verifiable rewards, Code RL replicating DeepCoder with sandboxed execution, preference learning (DPO plus a three-stage RLHF pipeline: SFT → reward model → RL), on-policy and off-policy distillation with multi-teacher configs, tool-use RL replicating Search-R1, and multi-agent RL with self-play. There's also rubric-based grading, VLM classification, and SDFT in the recipes README.

For learning, the `tutorials/` directory has 20+ progressive marimo notebooks covering rendering, loss functions, completers, weight management, custom RL environments, DPO, RLHF, and weight export.

Reusable infrastructure worth reading even if you never use the API:

- `renderers` — bidirectional conversion between token sequences and structured chat messages. This is the unglamorous part everyone gets wrong (chat template ↔ token masks ↔ loss weights). Their abstraction is worth stealing for your own training code.
- `hyperparam_utils` — learning rate and hyperparameter scaling for LoRA training — encodes their "LoRA Without Regret" findings (LR scaling with rank).
- An eval framework supporting 12 benchmarks (GSM8K, MATH-500, MMLU-Pro, GPQA, IFEval, AIME 2025/2026, etc.) with scores verified against published results, usable inline during training via `BenchmarkEvaluator`.

One more detail: the repo ships Claude Code skills — `/tinker:research` for planning post-training experiments and `/tinker:debug` for diagnosing training issues, installed via `/plugin marketplace add thinking-machines-lab/tinker-cookbook`. Given your CLI-agent workflow, this is directly usable.

## Getting started

```bash
uv pip install tinker-cookbook
export TINKER_API_KEY=<API_KEY>   # from tinker-console.thinkingmachines.ai after signup
marimo edit tutorials/101_hello_tinker.py
```

## Why this matters for you specifically

Your positioning is literally "Tinker-level skills as moat." The highest-leverage way to use this repo isn't as a customer — it's as a **reference architecture**. Read `rl_loop.py`, the renderers, and the RLHF recipe, then map each abstraction onto what you'd build yourself on the MI300X with your own DeepSeek-style MoE work. The gap between "API wrapper consultant" and "Frontier Labs level" is exactly the code in `tinker_cookbook/recipes/` — the loss masking, the advantage computation, the reward-model pipeline. It's Apache-2.0, 445 commits, actively maintained (v0.4.1, May 2026), pure Python. It's one of the cleanest public expressions of how a frontier lab thinks about post-training loops.

**References:**

- [tinker-cookbook (GitHub)](https://github.com/thinking-machines-lab/tinker-cookbook)
- [Tinker docs](https://tinker-docs.thinkingmachines.ai)
- [Tinker product page](https://thinkingmachines.ai/tinker/)
