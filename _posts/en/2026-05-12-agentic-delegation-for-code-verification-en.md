---
audio: false
generated: true
image: false
lang: en
layout: post
title: Agentic Delegation for Code Verification
translated: false
type: note
---

Question: Is the prompt "try it, run it, kill after 1 min, adjust params if not suitable, then tell me it's OK to run for hours" a great Claude Code prompt pattern? And can you explain why this workflow is so effective?

Answer:

## Yes — That Is an Excellent Claude Code Prompt

Your prompt is a near-perfect example of **agentic delegation**. Here's why it works so well:

---

### Why This Prompt Pattern Is Great

**1. It gives Claude a complete mini-workflow, not just a task**

You're not asking "what are the params?" — you're saying:
> "Do the experiment, judge the result, fix the problems, hand me the final answer."

Claude Code handles the entire feedback loop:
- Run → observe → diagnose → patch → confirm

**2. It uses time-boxing as a sanity check**

"Kill after 1 minute" is genius. It means:
- No wasted GPU hours on a broken config
- Claude sees real stdout/stderr (OOM errors, CUDA errors, loss=NaN, shape mismatches)
- 1 minute is enough to confirm the training loop is healthy

**3. It ends with a clear human handoff point**

> "Tell me it's OK — let me run in another terminal for hours"

This is the perfect division of labor:
- **Claude Code**: trial run, debugging, param validation
- **You**: execute the final blessed command in `tmux`

This matches exactly what the Claude Code team calls verification-first workflow — Claude performs dramatically better when it can verify its own work, like running tests and validating outputs, before handing results back to you.

---

### The General Pattern (Reusable Template)

This prompt works for almost any long-running ML job:

```
"Try running [command], kill it after [short time],
check for errors/warnings/bad params,
adjust anything that looks wrong,
then give me the final production command to run for real."
```

Apply it to:
- `torchrun` distributed training
- `python tokenize.py` on large datasets
- `pytest` on a big test suite before CI
- `ffmpeg` batch jobs
- Any `nohup`-worthy process

---

### What Claude Code Does During That 1 Minute

When Claude Code runs and kills your training job, it's checking:

| Signal | What It Means |
|---|---|
| CUDA OOM immediately | `batch_size` too large → halve it |
| `loss=NaN` at step 1 | LR too high or bad data |
| Slow step time | Need `compile=True` or smaller model |
| Clean step logs | ✅ Config is good |
| Shape mismatch error | Config/model mismatch → fix dims |

---

### Your Prompt Improved (Even Sharper Version)

```
Run a 1-minute smoke test of the training command.
Watch stdout for OOM errors, NaN loss, CUDA errors, or
abnormally slow step times. Kill it after 1 min.
Fix any param issues you find.
At the end, give me one clean final command I can paste
into a tmux session to run overnight.
```

This version makes Claude's checklist explicit, so it knows exactly what "looks OK" means.

---

### Summary

Your instinct is exactly right and aligns with professional ML workflow best practices:

```
Claude Code (1 min smoke test)  →  You (hours-long tmux run)
     diagnosis & fixing               production execution
```

The Claude Code team calls verification the single most impactful practice — giving Claude a way to check its own output before handing back to you. Your "run then kill" pattern is a hand-crafted version of exactly that.

References:

- [Claude Code Best Practices – Official Docs](https://code.claude.com/docs/en/best-practices)
- [Claude Code Power User Tips](https://support.claude.com/en/articles/14554000-claude-code-power-user-tips)
