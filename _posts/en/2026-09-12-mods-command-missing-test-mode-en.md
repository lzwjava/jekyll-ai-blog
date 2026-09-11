---
audio: false
generated: true
image: false
lang: en
layout: post
title: MODS command missing test mode
translated: false
type: note
---

Question: What is wrong with this MODS command?

Answer: The screenshot shows a **command-line argument error**, not a GPU hardware failure.

You ran:

```bash
mods gpuTest.js --skip_rm_state_init --notest
```

The important error is:

```text
Invalid test mode 0: you must use one of: -mfg -slt -oqa
Error 0000000005: Global.DoCommonTestBookkeeping bad command line argument
```

Your `--notest` does **not** select a MODS test suite. MODS requires one of the test modes:

```bash
# Manufacturing / broad stress test
./mods gputest.js -skip_rm_state_init -mfg

# SLT test
./mods gputest.js -skip_rm_state_init -slt

# Outgoing QA, generally lighter/faster
./mods gputest.js -skip_rm_state_init -oqa
```

This matches the MODS documentation: normal GPU testing uses `-mfg` or `-oqa`, while `-slt` is another defined test specification. ([studylib.net][1])

### For your GT730

I'd start with:

```bash
cd /home/GT730

./mods gputest.js -skip_rm_state_init -mfg
```

If your purpose is specifically **GPU repair / VRAM diagnosis**, you can then try standalone MATS:

```bash
./mats -h
```

and, depending on whether this GT730 is a normal display card or a headless/mining-style card, use the appropriate MATS invocation. MODS documentation describes standalone MATS as a framebuffer/memory test and notes that it is particularly useful when MODS itself cannot initialize the GPU. ([studylib.net][1])

So the current screen basically means:

```text
MODS itself is running
        ↓
gputest.js loaded
        ↓
command-line parsed
        ↓
NO TEST SUITE SELECTED
        ↓
exit with error 5
```

**It does NOT mean the GT730 failed.** You haven't actually started a GPU test yet.

[1]: https://studylib.net/doc/28338650/toaz.info-modspdf-pr-d6c4fcd269959d8ff99a0a1323fbc5f6?utm_source=chatgpt.com "NVIDIA MODS Diagnostic Software Manual for 343.X"
