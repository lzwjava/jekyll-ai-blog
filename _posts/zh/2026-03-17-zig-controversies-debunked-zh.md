---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Zig 争议：超越炒作
translated: true
type: note
---

**问题：** 关于 Zig 编程语言的不受欢迎观点有哪些？

**回答：**

以下是一些关于 Zig 的不受欢迎/有争议/“热议观点”，这些观点在 Reddit (r/Zig)、Hacker News、X/Twitter 和各种博客/视频社区中流传（截至 2026 年初）。这些观点往往与主流叙事相反，即 Zig 只是“更好的 C”，或在大多数方面明显优于 Rust/C++。

- **Zig 被高估 / 天真 / 部分领域像石器时代**  
  缺乏 traits/interfaces、不自然的泛型（通过 comptime）、缺失更高级抽象，使得它感觉未成熟或“像 Go 但更糟”，仅适合小型系统项目。有些人说语言设计者“其实不知道如何设计现代语言”。

- **标准库不应该存在（或应大幅缩减）**  
  一小部分人认为 Zig 的 stdlib 制造了维护负担和版本冲突——语言作为“更好的 C 编译器 + 构建系统”会更纯粹，一切都放在用户空间包中。

- **Zig 的极端显式性是缺陷而非优点**  
  没有 operator overloading、没有隐藏控制流、强制冗长（例如到处用 `[]const u8` 而非合适的 `string` 类型）、没有真正封装，使得代码更嘈杂、更难读——尤其项目变大时。

- **构建系统仍然糟糕 / 对于简单项目过于复杂**  
  尽管有改进，许多新人（以及一些资深用户）仍觉得添加依赖困惑、不直观，比 Cargo/npm 差——即使经过多年迭代。

- **Zig 实际上并不比 unsafe Rust（甚至实际中的 unsafe C）更安全**  
  “unsafe Zig 比 unsafe Rust 更安全”的说法被视为营销/谬论。在真实代码中，你仍会遇到 use-after-free、double-free 等，就像 C 一样，语言将大部分安全责任推给程序员。

- **没有合适的 Unicode/字符串处理是个严重设计错误**  
  强迫每个人自己实现 UTF-8 逻辑或引入沉重库，破坏了“更好的 C”目标，几乎适用于任何涉及文本的真实世界应用。

- **Comptime 很酷但被严重高估 / 容易踩坑**  
  它制造了难以阅读的“魔法”、编译时爆炸，以及难以推理的代码——有些人认为实际中比 Rust macros 或 C++ templates 更糟。

- **Zig 永远不会广泛采用 / 已经失败于获得牵引力**  
  尽管炒作，它被视为太小众、pre-1.0 时太不成熟、破坏性变更太多、生态太小。有些人预测长期比 Rust 更不受欢迎。

- **Zig 模仿了糟糕的 Posix 设计选择**  
  API（尤其是文件/套接字 I/O）继承了 partial-write/partial-read 行为，却不强制调用者正确处理 → 导致代码静默损坏比 C 替代品更频繁。

- **“未使用变量是编译错误”的规则是意识形态胡说**  
  将未使用变量/返回值视为致命错误（而非警告）感觉像是多余的独裁式语言管制。

这些观点许多来自认真尝试 Zig 的人（有时几个月），然后回到 Rust、C、Go 或 C++——或长期 C 开发者，他们觉得 Zig“修复了本无需修复的东西”。

**参考：**

- [What is your 'unpopular opinion' about Zig? (Reddit)](https://www.reddit.com/r/Zig/comments/1nun2at/what_is_your_unpopular_opinion_about_zig)
- [Zig; what I think after months of using it (Hacker News discussion)](https://news.ycombinator.com/item?id=42942618)
- [Why is Zig so cool? (Hacker News — contains several critical takes)](https://news.ycombinator.com/item?id=45852328)
- Various X posts criticizing Zig's design choices, syntax, and ecosystem maturity (2025–2026)