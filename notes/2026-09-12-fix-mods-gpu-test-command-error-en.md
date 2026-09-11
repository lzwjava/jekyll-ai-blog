---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix MODS GPU Test Command Error
translated: false
type: note
---

**Question:** What does this MODS GPU test error mean, and how do I fix it?

**Answer:**

The screen shows a MODS (NVIDIA's GPU diagnostic tool) run with an invalid command line, resulting in **Error Code 0x000000005 (bad command line argument)**.

**What went wrong:**

The command used was:

```
./mods gputest.js -skip_rm_state_init -notest -notest
```

Two issues are visible:

1. **`-notest` was passed twice** — MODS warned: *"Multiple occurrences of '-notest' without PARAM_MULTI_OK, will process last occurrence only"*
2. **Invalid test mode 0** — the error says you must use one of: `-mfg`, `-slt`, or `-oqa` to specify a valid test mode. Running without one of these mode flags causes the failure.

**How to fix it:**

Use a valid test mode flag. For example:

```bash
# Manufacturing mode
./mods gputest.js -skip_rm_state_init -mfg

# SLT (System Level Test) mode
./mods gputest.js -skip_rm_state_init -slt

# OQA mode
./mods gputest.js -skip_rm_state_init -oqa
```

- Remove the duplicate `-notest` flags.
- Choose **one** of `-mfg`, `-slt`, or `-oqa` based on the test context (manufacturing line, system test, or quality assurance).

The red "FAIL" graphic confirms the test did not run successfully due to the bad arguments — it's not a hardware failure.

**References:**

- [NVIDIA MODS Documentation](https://developer.nvidia.com/mods)
