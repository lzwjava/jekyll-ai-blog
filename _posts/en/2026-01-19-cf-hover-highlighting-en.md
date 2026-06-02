---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Codeforces Sample Hover Highlighting Behavior
translated: false
type: note
---

Question: For Codeforces, when input is provided, does putting the mouse cursor over one test case highlight it with a yellow background and also highlight the corresponding output section in the output area?

Answer:

Yes, that's **exactly** how it works on Codeforces.

When you look at a problem's sample input/output:

- If you hover the mouse over any line (or group of lines) in the **Input** section,
  that line/block gets a **yellow background highlight**.

- At the same time, the **corresponding part** in the **Output** section also gets highlighted with the same yellow background.

This is a very helpful feature especially when:

- There are many sample test cases
- The input/output is large
- You want to quickly see which output belongs to which input

The highlighting is synchronized between input and output sections. Codeforces groups the corresponding input/output pairs and highlights them together when you hover over either side.

This behavior has existed for many years and is still present in 2026.

References:
