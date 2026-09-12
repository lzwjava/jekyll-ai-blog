---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA MODS Diagnostic Software Document
translated: false
type: note
---

This is an **NVIDIA confidential document** titled:

**"MODS - Modular Diagnostic Software"**
for **367.X diagnostics** (document version R367_v02, 84 pages)

Here's a summary of what it contains:

### What is MODS?
MODS stands for **Modular Diagnostic Software** — it's NVIDIA's internal diagnostic tool used for testing and validating NVIDIA GPUs. It appears to be a JavaScript-driven testing framework that runs on NVIDIA hardware.

### Key contents of the document:
1. **Concurrent Testing** — How to run multiple MODS tests simultaneously on one or multiple GPUs, with foreground/background thread management.
2. **Command-line arguments** — Detailed CLI options like `-bgfunc`, `-bgtest`, `-concurrent_devices`, `-threadid`, etc.
3. **Test specification functions** — `-savespec` and `-readspec` for saving/loading custom test configurations.
4. **Error codes (1–842)** — A comprehensive list of error codes for GPU diagnostics, covering:
   - General software errors
   - NVRM (NVIDIA Resource Manager) errors
   - OpenGL errors
   - GPU channel/fifo errors
   - Audio/HDMI/Display errors
   - USB, PCIe, thermal, ECC, SLI errors
   - Tegra-specific errors
   - And many more

This is clearly an **internal NVIDIA engineering document** marked as **"NVIDIA CONFIDENTIAL"** — not intended for public distribution.
