---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 超越语言炒作与教条
translated: true
type: note
---

关于 Leslie Lamport 的这段轶事非常有趣。我认为 Lamport 和 王垠 都触及了一些本质的东西，尽管我的表述方式会有所不同。

**他们的正确之处：**

1. **Language hype cycles 是真实存在的**。“新语言 X 将解决一切问题” → 大规模采用 → 幻灭 → 下一个语言，这种模式是切实可观察到的。Scala、Go 以及现在的 Rust 都经历过这种周期。

2. **仅靠语言无法解决根本问题**。更好的 syntax 或 type systems 并不会自动让程序员写出更好的软件。Software engineering 中困难的部分（理解 requirements、管理 complexity、团队协作）是超越语言选择的。

3. **Formal reasoning 至关重要**。Lamport 关于 mathematics 的观点可能指的是 precise specification 和 reasoning about correctness 的价值——这在很多软件开发中确实被低估了。

**我的不同看法：**

1. **语言确实重要，只是作用不是无限的**。与 C/C++ 相比，Rust 的 ownership system 确实让某些类别的 bugs 更难发生。Go 的简洁性确实有助于维护大型 codebases。即使这些优点被过度推销，它们也并非虚幻。

2. **“Mathematics 是最好的编程语言”虽具有启发性但不切实际**。Formal methods 很有价值，但编写 TLA+ specs 并不能取代 implementation。我们既需要严谨的思考，也需要务实的 tools。

3. **这种轻蔑态度似乎有些过度**。将 POPL 描述为“人们如何吹嘘和解决不存在的问题”忽视了真实的 research progress。虽然有些学术研究确实与实践脱节，但并非全部如此。

**我的看法：** 语言是具有实际权衡的 tools，而不是银弹。健康的中间立场是：根据 context 使用合适的语言，投入精力进行适当的 design 和 specification，但不要指望任何语言能解决那些本质上属于人类判断和 complexity management 的问题。
