---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 Sliding Window Attention Incompatibility
translated: false
type: note
---

Question: Why is the training run failing with the message about `window_pattern="SSSL"` and RTX 4070 not supporting sliding window attention?

Answer:

The issue arises from a mismatch between the attention pattern used in your script and what your GPU supports. Here's a breakdown:

1. **Attention Patterns:**

   * `L` = full context attention (standard attention over the entire sequence).
   * `S` = sliding window attention (a memory-efficient approximation that only looks at a small “window” of tokens).

2. **Hardware Limitation:**

   * On your **RTX 4070**, the SDPA (Scaled Dot-Product Attention) implementation in the framework **does not support sliding window attention**.
   * That’s why using `window_pattern="SSSL"` (which contains sliding windows `S`) causes the error.

3. **Previous Run Worked:**

   * The previous run used `"L"` (full attention), which your GPU supports, so it worked fine.

4. **Solution:**

   * You need to explicitly set `--window-pattern L` in your script so that the model uses **full context attention**, which is compatible with your RTX 4070.
   * Essentially, the script defaulted to a sliding window configuration, which your GPU cannot handle.

5. **Next Steps:**

   * Kill the current run (it’s only at step 10k and hasn’t done any real training yet).
   * Edit your `run_rtx4070_chinchilla.sh` script to add `--window-pattern L` in the command that launches training.
   * Restart the run.

This is **not a bug** in your code—just a hardware compatibility issue with the attention pattern.

If you want, I can show you the exact snippet to patch in your script so it runs without errors.
