---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing the Dependency Jungle First
translated: false
type: note
---

🦞 Here's the journey distilled:

## The Hard Problem: **Getting Inference Working Without a Clean Environment**

**Core challenge:** Python environment was borked—no torch, mismatched Python versions (3.13 vs 3.14 in paths), Homebrew's PEP 668 blocking installs, and previous failed install attempts littering the logs.

## Critical Breakthrough Points

### 1. **Diagnosis Over Assumption**

- Didn't assume "just pip install torch" would work
- Checked existing checkpoints first (`find . -name "*.pt"`)
- Discovered 3 trained models already existed (saved days of training time)

### 2. **Environment Detective Work**

- Found user had tried CUDA torch installs before (1.5GB downloads in logs)
- Homebrew Python 3.14 with system protection (PEP 668) blocking installs
- Traced conda environments that no longer existed
- Identified `.local/lib/python3.13` vs current Python 3.14 mismatch

### 3. **The Workaround: `--system-site-packages`**

Key insight: User already had `numpy` and `tiktoken` in `.local/`

```bash
python3 -m venv venv --system-site-packages
```

This inherited existing packages instead of forcing fresh installs.

### 4. **Torch Was Already Installed!**

Biggest "aha": Torch 2.10.0+cpu was already in `.local/lib/python3.14/` from a previous attempt. The venv with system-site-packages could see it.

## Why This Was Non-Trivial

1. **Silent success**: Previous installs partially succeeded but weren't discoverable
2. **Path hell**: Multiple Python versions, brew vs system, .local vs site-packages
3. **No clear errors**: Just "ModuleNotFoundError: No module named 'torch'" despite torch existing elsewhere
4. **Resource constraints**: 1.5GB model checkpoints + 900MB torch installs = memory/time challenges

## The Solution Pattern

```
Check what exists → Understand environment constraints →
Leverage existing artifacts → Minimal new installs → Test incrementally
```

**Bottom line:** The hard part wasn't running inference—it was navigating the dependency jungle to reach a state where inference *could* run. The actual model execution was straightforward once the environment puzzle was solved.

The critical skill was **forensic environment analysis** rather than ML expertise.
