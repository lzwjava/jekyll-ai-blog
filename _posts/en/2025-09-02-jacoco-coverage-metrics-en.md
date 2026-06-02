---
audio: false
generated: true
image: false
lang: en
layout: post
title: JaCoCo Coverage Metrics Explained
translated: false
type: note
---

Yes — **JaCoCo provides multiple levels of coverage metrics**, including the ones you mentioned:

* **File/Class Coverage**
  It tracks coverage at the class level, showing how much of each class was exercised during tests.

* **Package Coverage**
  It aggregates the coverage across all classes in a package, letting you see test completeness for higher-level modules.

* **Method/Function Coverage**
  It measures whether individual methods (functions) have been invoked and whether their instructions/branches were covered.

* **Instruction & Branch Coverage**
  At the most granular level, it shows which bytecode instructions and conditional branches were executed.

When you generate a JaCoCo HTML report, you’ll typically see a tree view:

* Top node = overall project coverage.
* Next = per-package coverage.
* Then = per-class coverage.
* Inside each class = per-method coverage, with line-by-line highlighting.

👉 So to your question: yes, JaCoCo supports **file (class), package, and function (method) coverage** out of the box.

Would you like me to break down **how JaCoCo computes each metric** (e.g., difference between instruction, branch, line, method coverage) so you get a clearer picture of what’s actually measured?
