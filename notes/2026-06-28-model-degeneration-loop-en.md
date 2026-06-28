---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Degeneration Loop
translated: false
type: note
---

There you go — 1000 new tokens. It just keeps getting worse:

- Lines 1-48: prompt replayed verbatim (good)
- Lines 49-65: garbled Java-looking code with random class/method names
- Lines 66+: collapses into repetitive `S.S.S.S.S` patterns, random punctuation, `this.S.S.BufferType = array.S.S.S.S = null`, etc.

By ~200 tokens in it's essentially in a degeneration loop — the model has no idea what comes next so it just cycles through high-probability garbage tokens. The `S.S.S.S.S` repetition suggests the token distribution has collapsed into a narrow mode.

This is the classic failure mode of small language models — they memorize training examples but can't compose novel sequences.
