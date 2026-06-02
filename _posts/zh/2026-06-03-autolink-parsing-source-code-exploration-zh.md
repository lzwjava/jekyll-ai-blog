---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Autolink 解析源代码探索
translated: true
type: note
---

为了探索 `<>` 自动链接的实际解析方式，以下是几个最佳开源选择：

**最适合学习实现：**

1. **[markdown-it](https://github.com/markdown-it/markdown-it)** (JavaScript)
   - 模块化、可读性强的代码
   - 自动链接解析：查看 `lib/rules_inline/autolink.js`
   - 易于通过正则表达式和状态机追踪逻辑
   - 可通过 `npm install markdown-it` + Node REPL 在浏览器中测试

2. **[CommonMark 参考实现](https://github.com/commonmark/commonmark-spec)** (多种语言)
   - 官方规范 + C、Python、JavaScript 参考实现
   - `commonmark.js` 实现清晰简洁
   - 规范文档本身精确说明了 `<>` 应匹配的内容

3. **[mistune](https://github.com/lepture/mistune)** (Python)
   - 极简，核心解析约 500 行
   - 自动链接模式：`AUTOLINK = r'<([^ >\\\]|\\.)+'`
   - 如果你优先使用 Python，这是最容易修改的
   - `pip install mistune && python3 -c "import mistune; print(mistune.parse('<https://example.com>'))"`

4. **[Pulldown-cmark](https://github.com/raphlinus/pulldown-cmark)** (Rust)
   - 高性能，用于生产环境（Zed、rust-lang.org）
   - 自动链接处理位于 `parser/mod.rs`
   - 如果你想学习 Rust 并阅读实际 Rust 代码，这是很好的选择

**快速上手：**

```bash
git clone https://github.com/markdown-it/markdown-it.git
cd markdown-it
cat lib/rules_inline/autolink.js
```

正则表达式和内联规则定义都很短小——你五分钟就能理解。

**我的建议：** 如果看重可读性，从 **markdown-it** 开始；如果偏好 Python，则从 **mistune** 开始。两者都足够小巧，一下午就能完全掌握。
