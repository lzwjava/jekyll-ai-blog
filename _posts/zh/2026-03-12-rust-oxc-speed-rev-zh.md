---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rust 驱动 OXC 速度革命
translated: true
type: note
---

问题：为什么 oxc.rs（the JavaScript Oxidation Compiler）这么快？

答案：

## OXC 是什么？

OXC (oxc.rs) 是一个由 Rust 完全编写的高性能 JavaScript 和 TypeScript 工具集合——parser、linter、formatter、transformer、minifier 和 resolver。它是 VoidZero 对 JavaScript 统一、高性能工具链愿景的一部分，并为 Rolldown（Vite 未来的 bundler）提供动力。

---

## 为什么它这么快？

### 1. 使用 Rust 编写

OXC 利用 Rust 的内存安全保证和零成本抽象，实现了以前在基于 JavaScript 的工具中不可能实现的高性能水平。与 ESLint（Node.js/JS）或 Babel（JS）不同，Rust 编译为原生机器码，没有垃圾回收器暂停，也没有 JIT 预热开销。

---

### 2. Memory Arena 分配

Memory arena 预先以块或页的形式分配内存，并在 arena 被丢弃时整体释放。AST 在 arena 上分配，因此丢弃 AST 是一个快速操作。

此外，AST 以特定顺序构建，树遍历也遵循相同顺序，从而在访问过程中实现线性内存访问。这种访问模式高效，因为所有附近的内存会以页为单位读入 CPU cache，从而实现更快的访问时间。

切换到使用 memory arena 进行 AST 分配带来了大约 **20% 的性能提升**。

---

### 3. 小型且对 Cache 友好的 AST Enum 大小

在典型的 JavaScript AST 中，像 `Expression`（45 个变体）和 `Statement`（20 个变体）这样的 enum，如果天真实现，每个节点可能超过 200 字节。OXC 仔细地对 enum 变体进行 boxing 以保持其小巧。这减少了在模式匹配过程中必须传递和读取的数据——显著提高了 **CPU cache 效率**。

---

### 4. 共享编译栈（无冗余解析）

共享 parser 架构意味着所有 OXC 工具都操作相同的 Abstract Syntax Tree (AST)，消除了传统上多个工具处理同一代码库时发生的冗余解析。在传统设置中，ESLint、Babel 和 Prettier 各自独立解析文件——OXC 只解析一次。

---

### 5. 优化的 Parser 内部实现

Parser 使用了几种优化技术：AST 节点在 memory arena 上分配以实现快速清理，span offsets 使用 `u32` 而非 `usize` 以提高内存效率，复杂的语法错误委托给单独的 semantic analyzer 以保持解析速度。

---

### 6. 无竞争的并行性

团队移除了阻塞并行解析线程的全局锁机制（如 `string-cache` 库）。移除此全局锁将并行解析性能提高了约 **30%**，通过 Rayon（Rust 的数据并行库）实现了完整的 CPU 核心利用率。

---

### 7. 将速度视为首要需求

Oxc 将速度视为产品需求。更快的工具改善了本地反馈循环并降低了 CI 成本。性能回归被视为 bug。

---

## 基准测试总结

Oxc 的 parser 至少比 SWC 快 3 倍，比 Biome 快 5 倍。OXC transformer 比 SWC 快 4 倍，比 Babel 快 40 倍，并使用 70% 更少的内存。Oxlint 根据 CPU 核心数量比 ESLint 快 50–100 倍。Oxfmt 比 Biome 快 3 倍，比 Prettier 快 35 倍。oxc-resolver 比 webpack 的 enhanced-resolve 快 30 倍。

---

## 总结表格

| 工具 | 与之比较 | 速度提升 |
|---|---|---|
| Parser | SWC | ~3x faster |
| Parser | Biome | ~5x faster |
| Linter | ESLint | 50–100x faster |
| Formatter | Prettier | ~35x faster |
| Transformer | Babel | ~40x faster |
| Resolver | webpack enhanced-resolve | ~30x faster |

参考资料：

- [oxc.rs — What is Oxc?](https://oxc.rs/docs/guide/what-is-oxc.html)
- [oxc.rs — Performance Deep Dive](https://oxc.rs/docs/learn/performance)
- [oxc.rs — All Benchmarks](https://oxc.rs/docs/guide/benchmarks.html)
- [OXC Deep Dive Article](https://alisoueidan.com/blog/oxc-rust-powered-next-gen-javascript-tooling)
- [GitHub — oxc-project/oxc](https://github.com/oxc-project/oxc)