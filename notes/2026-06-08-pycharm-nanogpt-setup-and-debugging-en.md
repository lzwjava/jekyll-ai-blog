---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyCharm NanoGPT Setup and Debugging
translated: false
type: note
---

Here's how to set it up in PyCharm:

1. Open the project: File → Open → ~/projects/nanoGPT

2. Set Python interpreter: PyCharm → Settings → Project → Python Interpreter → Add → Existing → `/opt/homebrew/bin/python3.14`

3. Create a Run Configuration for sample.py:
   - Run → Edit Configurations → + → Python
   - Name: `sample-gpt2`
   - Script path: `sample.py`
   - Parameters:
     ```
     --init_from=gpt2 --device=mps --dtype=float32 --num_samples=1 --max_new_tokens=150 --start="Hello world"
     ```
   - Working directory: `/Users/lzwjava/projects/nanoGPT`

4. Create another for the Shakespeare model:
   - Name: `sample-shakespeare`
   - Script path: `sample.py`
   - Parameters:
     ```
     --out_dir=out-shakespeare-char --device=mps --dtype=float32 --num_samples=1 --max_new_tokens=200 --start="ROMEO:"
     ```

5. Set breakpoints — good places to start:
   - `model.py` line ~175: inside `forward()` of `CausalSelfAttention` — watch q,k,v shapes
   - `model.py` line ~210: inside `forward()` of `MLP` — watch the 4x expansion
   - `sample.py` line 87: the `model.generate()` call — step into to see autoregressive loop
   - `model.py` line ~245: `GPT.generate()` — watch how tokens are appended one by one

6. Debug: click the bug icon (Shift+F9) instead of Run. Use:
   - F7: Step Into (dive into functions)
   - F8: Step Over
   - F9: Resume (run to next breakpoint)
   - Alt+Click on variable: evaluate expression

For `train.py`, create a config like:
   - Script path: `train.py`
   - Parameters: `config/train_shakespeare_char.py --device=mps`
   - This trains the char-level model — set a breakpoint in the training loop at `train.py` line ~175 (`for X, Y in loader:`) to watch loss decrease step by step.

That's it. PyCharm's debugger with MPS tensors works fine — you can inspect shapes, values, gradients in the Variables panel.
