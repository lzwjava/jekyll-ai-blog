---
audio: false
generated: true
image: false
lang: en
layout: post
title: A Two-Phase Machine Learning Workflow
translated: false
type: note
---

Question: When training nanoGPT, is the recommended workflow to first do a smoke run with Claude Code, and then run the full training command manually in a separate terminal since training takes a long time?

Answer:

Yes — this is exactly the right workflow, and it's a well-established best practice in ML training. Here's why it makes sense and how it works:

---

## Why This Two-Phase Workflow Is Correct

### Phase 1: Smoke Run via Claude Code (Short Sanity Check)

A **smoke run** is a minimal, fast test to confirm your setup doesn't break before committing to a long training job. With Claude Code, you ask it to set up, configure, and kick off a very short run (a few iterations), so it can:

- Verify the environment (dependencies like `torch`, `tiktoken`, `numpy` are installed)
- Confirm data prep scripts work (`prepare.py` ran and produced `train.bin` / `val.bin`)
- Check config overrides are valid (no typos in model size, batch size, etc.)
- Ensure GPU/MPS/CPU is detected correctly
- Catch OOM (Out of Memory) errors early with tiny `batch_size` or `block_size`

A typical smoke run for nanoGPT might look like:

```bash
# Smoke run: just 10 iterations to confirm setup works
python train.py config/train_shakespeare_char.py \
  --max_iters=10 \
  --eval_interval=5 \
  --device=cuda
```

Claude Code runs this interactively, reads the output, and can debug any errors inline — this is **exactly what Claude Code is good at** (short, iterative, agentic work).

---

### Phase 2: Full Training in a Separate Terminal (Long-Running Job)

Once the smoke run passes, you **do not** want Claude Code to run the real training, because:

- Full nanoGPT GPT-2 (124M) training can take **hours to days** (e.g., 4 days on a single A100, or ~3 min on 8×H100s for the speedrun)
- Even the Shakespeare char model can take **5 minutes on GPU or 8+ hours on CPU**
- Claude Code sessions are not meant for long-blocking processes — they can time out or lose context
- You want the training process running **independently**, not tied to an AI session

So you open a **separate terminal** and run it yourself:

```bash
# For Shakespeare (small, CPU-friendly, ~5 min on GPU):
python train.py config/train_shakespeare_char.py

# For GPT-2 full reproduction (requires 8× A100):
torchrun --standalone --nproc_per_node=8 train.py config/train_gpt2.py
```

Use `tmux` or `screen` to keep training alive even if you disconnect:

```bash
tmux new -s nanogpt_train
python train.py config/train_shakespeare_char.py
# Ctrl+B, D to detach; tmux attach -t nanogpt_train to reconnect
```

---

## Summary of the Full Workflow

| Step | Who Does It | Why |
|---|---|---|
| Setup env, prep data | Claude Code | Agentic, handles errors |
| Smoke run (10–50 iters) | Claude Code | Fast validation, catch bugs |
| Full training run | You, in separate terminal | Long-running, needs persistence |
| Monitor logs / debug errors | Claude Code (if needed) | Can read log files and advise |
| Sample/generate text | Either | Short task again |

---

## Pro Tip: Checkpoint Recovery

nanoGPT automatically saves checkpoints during training (`ckpt.pt` in `out_dir`). If training crashes, you can resume:

```bash
python train.py config/train_shakespeare_char.py --init_from=resume
```

This makes the manual terminal approach even safer — you're not starting over if something goes wrong.

---

**In short: Yes, smoke run with Claude Code ✅, full training yourself in a separate terminal ✅ — this is the correct and professional pattern.**

References:

- [nanoGPT GitHub (Andrej Karpathy)](https://github.com/karpathy/nanoGPT)
- [Training nanoGPT on Modal - AI Engineering Academy](https://aiengineering.academy/LLM/ServerLessFinetuning/TrainNanoGPTModalTutorial/)
- [Smoke Testing Best Practices](https://thetestershub.com/smoke-testing/)
- [Exploring NanoGPT - DoltHub Blog](https://www.dolthub.com/blog/2023-02-20-exploring-nanogpt/)