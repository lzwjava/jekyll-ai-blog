---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Zig 为 Ghostty 开发者带来喜悦
translated: true
type: note
---

**问题：为什么 Ghostty 作者喜欢 Zig lang？**

**回答：**

**Ghostty** 的作者 Mitchell Hashimoto（HashiCorp 联合创始人）多次解释说他选择并喜欢 **Zig** 主要是因为它真正**有趣**，即使经过数年的开发，这种个人乐趣依然强烈。

以下是他喜欢 Zig 的主要原因，基于他在演讲、博客文章和访谈中的表述：

- **日常编码的乐趣和喜悦** — 他将 Zig 描述为“an absolute joy to work with”，并说他每天编写 **Zig** 代码都**很有趣**，这种感觉在构建 Ghostty 两年多后也没有减弱。

- **他个人喜欢该语言、社区和构建系统** — 在他的 Zig Showtime 演讲中介绍 Ghostty 时，他说：“Simply put: I like the community, language, and build system.” 他觉得 Zig 的特性和构建系统特别适合像终端模拟器这样的复杂项目。

- **与其他语言的对比** — 虽然承认 Rust 很棒，但他指出 Rust 对他个人来说“not that fun”（相比之下）。Zig 给他带来更高的士气和乐趣，这对于长期的个人/热情项目非常重要。

- **对项目的实际优势** — Zig 实现了干净、高性能的核心（libghostty），可在各平台共享，编译为原生代码，与 C API（Linux 上的 GTK）良好互操作，尽管是较新的语言，但代码库对贡献者仍易于上手。

Ghostty 于 2022 年起步，纯粹作为个人游乐场，用于实验 Zig、学习图形编程并更好地理解终端 — 最初并非打算发布。持续使用 Zig 的乐趣是将其转变为严肃、高质量终端模拟器、达到 1.0 版本并获得人气的关键。

简而言之：最大的原因是主观乐趣 — Zig 让他觉得编码愉悦，这对独立的多年度项目是强大的动力。

**参考资料：**

- [https://mitchellh.com/writing/ghostty-1-0-reflection](https://mitchellh.com/writing/ghostty-1-0-reflection)
- [https://mitchellh.com/writing/ghostty-and-useful-zig-patterns](https://mitchellh.com/writing/ghostty-and-useful-zig-patterns)
- [https://ghostty.org/docs/about](https://ghostty.org/docs/about)
- [https://leapcell.medium.com/some-fun-facts-about-ghostty-0baa34a345ae](https://leapcell.medium.com/some-fun-facts-about-ghostty-0baa34a345ae)