---
audio: false
generated: true
image: false
lang: en
layout: post
title: Focus on CLI Agent Moat
translated: false
type: note
---

Question: What should I focus on over the next few months, given consulting, model training, and CLI agent dev?

Answer: No single lever — but here's a specific prioritization, not a vague "it depends."

**1. Compound the CLI agents into a moat (highest leverage)**

- ww/iclaw/zz are your actual product. Consulting revenue is time-for-money; agents are the thing that scales without you.
- Concrete move: pick ONE of the three, ship a public benchmark against Claude Code / Cursor / Aider on a fixed task set (SWE-bench-lite subset or your own repo tasks). Numbers > claims. Publish the harness on GitHub.
- If you don't have eval infra yet, build it first — 200-300 lines, not a framework:

```python
# eval_harness.py — minimal task runner
import subprocess, json, time

def run_task(agent_cmd, task_dir, timeout=300):
    start = time.time()
    result = subprocess.run(agent_cmd, cwd=task_dir, capture_output=True,
                             timeout=timeout, text=True)
    return {
        "task": task_dir,
        "passed": run_tests(task_dir),  # your test runner
        "duration_s": time.time() - start,
        "tokens": parse_token_usage(result.stdout),
    }

def run_tests(task_dir):
    r = subprocess.run(["pytest", "-x", "-q"], cwd=task_dir, capture_output=True)
    return r.returncode == 0
```

**2. Model training — narrow the scope**

- GPT-2 760M on MI300X was infra proof-of-work. The next unlock isn't bigger pretrain, it's post-training on your own agent traces (SFT + rejection sampling from ww/iclaw logs). That directly feeds #1.
- 2B tokens/mo across top models = you already have a dataset of what fails. Turn agent failure/success traces into a training set. That's higher ROI than another pretrain run right now.

**3. Consulting — use it as distribution, not the business**

- Every consulting client is a design partner for the CLI agents if you frame it that way. Ask each one: "can I open-source the eval results from your codebase (anonymized)?" Turns billable hours into public proof.

**4. What to explicitly NOT do**

- Don't hire yet unless a specific bottleneck (support load, infra ops) is costing you >10hrs/wk that isn't agent/research work.
- Don't chase a bigger pretrain run before your post-training data pipeline from #2 exists — wasted compute.

If you tell me which of ww/iclaw/zz you're pushing, I can help design the eval harness or the SFT data pipeline concretely.
