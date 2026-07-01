---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mid-Process Failure Cascade
translated: false
type: note
---

Several things went wrong mid-process:

1. sglang 0.4.x hard-pins torch==2.7.1
   Our original plan was torch 2.5.1+cu124 + triton 3.1.0. But sglang 0.4.10's `[srt]` extra has `torch==2.7.1` as an exact pin. The compiled kernels (sgl-kernel 0.2.8, flashinfer 0.2.9rc2) are built against 2.7.1. So torch 2.5.1 was impossible with sglang 0.4.x.

2. cu124 wheels stopped at torch 2.6.0
   PyTorch stopped publishing cu124 wheels after 2.6.0. torch 2.7.1 only has cu126/cu128/cu130. Had to pivot from the original "cu124" plan to cu126.

3. sglang dependency resolver fighting our torch pin
   When we ran `pip install sglang[all]`, pip's resolver saw `torch==2.7.1` in sglang's deps and tried to install it, which would have overwritten our carefully pinned cu124 torch. Had to use `--no-deps` first, then install deps separately.

4. pip timed out downloading torch (2x)
   The torch+cu124 and torch+cu126 wheels are ~800MB. SSH connections timed out at 300s. Had to switch to `nohup` background installs.

5. HuggingFace unreachable from workstation
   The proxy (127.0.0.1:7890) is configured in `.bashrc` via `start_proxy` but doesn't activate in non-interactive SSH. Had to export HTTP_PROXY/HTTPS_PROXY explicitly, then wrote a launch script.

6. ninja not in PATH
   sglang spawns `ninja` as a subprocess for JIT compilation. The pip ninja package installs to the venv bin, but sglang's subprocess couldn't find it. Had to add venv bin to PATH.

7. OOM from zombie process
   First successful launch crashed on port bind (30000 already in use). Second launch OOM'd because the first sglang process was still holding 8.65 GB of GPU memory. Had to `pkill -9` everything and wait for GPU to free.

The biggest conceptual hurdle: the original plan (torch 2.5.1+cu124+triton 3.1.0) was incompatible with sglang 0.4.x's exact torch pin. Had to find that torch 2.7.1+cu126 + triton 3.3.1 was the actual working combination — newer triton (3.3.1) than planned but still old enough to avoid the 3.5/3.6 segfault.
