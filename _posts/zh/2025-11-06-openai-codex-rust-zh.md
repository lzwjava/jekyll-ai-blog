---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: OpenAI Codex命令行工具基于Rust开发
translated: true
type: note
---

### OpenAI Codex CLI 与 Rust

GitHub 仓库 [https://github.com/openai/codex](https://github.com/openai/codex) 托管着 OpenAI 的 Codex，这是一个轻量级、实验性的基于 CLI 的编码助手，可在本地终端运行。它通过与 OpenAI 模型（例如通过 Responses API，默认为 o4-mini）集成，帮助完成代码生成、编辑和调试等任务。它支持通过 ChatGPT 账户或 API 密钥进行身份验证，通过 TOML 文件进行配置，并通过模型上下文协议（MCP）进行扩展。可通过 npm、Homebrew 或适用于 macOS 和 Linux 的直接二进制文件进行安装。

#### Codex 如何使用 Rust？

Codex 的 CLI 工具已大部分用 Rust 重写，目前 Rust 代码约占代码库的 96.7%（其余为 Python、TypeScript 等）。Rust 实现（位于 `codex-rs` 子目录中）为核心终端界面提供动力，包括：

- **原生二进制编译**：生成用于跨平台分发的独立可执行文件（macOS Apple Silicon/x86_64、Linux x86_64/arm64），无需外部运行时依赖。
- **安全功能**：使用 Rust 实现 Linux 沙箱，以安全地执行和测试生成的代码。
- **协议处理**：实现可扩展的 MCP 服务器"线协议"及未来的多语言扩展（例如允许 Python 或 Java 插件）。
- **TUI（终端用户界面）组件**：Rust 处理终端中的文本选择、复制/粘贴和交互元素。

此次转型始于部分重写（到 2025 年中约一半代码使用 Rust），现已进展到近乎完全采用，发布版本标记如 `rust-v0.2.0`。您可以通过 `npm i -g @openai/codex@native` 安装原生 Rust 版本。原始的 TypeScript/Node.js 版本仍然可用，但将在实现功能对等后逐步淘汰。

#### Rust 对它有帮助吗？

是的，Rust 显著提升了 Codex 作为 CLI 工具的可用性和可靠性。主要优势包括：

- **性能提升**：无垃圾收集运行时意味着更低的内存使用和更快的启动/执行速度，非常适合 CI/CD 流水线或容器等资源受限环境。
- **简化分发**：单一静态二进制文件消除了"依赖地狱"（例如无需安装 Node.js v22+、npm 或 nvm），使其更易于部署并减少用户摩擦。
- **安全性改进**：Rust 的内存安全性和原生绑定为代码执行提供了强大的沙箱支持，防止在运行不受信任生成代码的工具中出现漏洞。
- **可扩展性和可维护性**：线协议允许与其他语言无缝集成，而 Rust 的生态系统支持快速迭代终端特定功能，如 TUI。

这些特性使得 Codex 对于在终端或 IDE（例如 VS Code 集成）中工作的开发人员来说更加稳健。

#### 他们为什么使用 Rust？

OpenAI 从 TypeScript/Node.js 切换到 Rust，主要是为了解决 JS 生态系统在高性能、安全 CLI 方面的局限性：

- **消除依赖**：Node.js 要求（例如特定版本）阻碍了没有合适设置的用户；Rust 二进制文件是零依赖且可移植的。
- **更好的代码执行安全性**：用于沙箱的原生 Rust 绑定已被使用，因此完全切换对于更安全的本地代码测试是合乎逻辑的。
- **性能优化**：避免 JS 运行时开销（例如 GC 停顿）确保了可预测、高效的资源使用——这对于实时处理 AI 生成代码的工具至关重要。
- **长期可扩展性**：Rust 支持更轻松的扩展协议，并与 OpenAI 实现"原生"体验的目标保持一致，相比双重的 Node/Rust 代码库，减少了维护负担。

迁移大约在 2025 年 6 月宣布，并有一个燃尽列表跟踪诸如 README 更新和 Homebrew 配方更改等任务。它仍然是实验性的，因此预计会有持续的改进。

**参考资料**

- [GitHub 仓库概览](https://github.com/openai/codex)
- [关于 Rust 重写的 Reddit 讨论](https://www.reddit.com/r/rust/comments/1lkdu2m/openai_is_ditching_typescript_to_rebuild_codex/)
- [关于安全与性能切换的 Heise 文章](https://www.heise.de/en/news/Security-and-performance-OpenAI-Codex-CLI-switches-from-TypeScript-to-Rust-10425172.html)
- [SSOJet 博客关于效率提升的文章](https://ssojet.com/blog/openai-codex-transitions-to-rust-enhancing-efficiency-and-power)
