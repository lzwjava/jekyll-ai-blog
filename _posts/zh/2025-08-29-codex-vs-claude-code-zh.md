---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Codex与Claude代码对比
translated: true
type: note
---

以下通过更清晰的非表格形式，对比 **OpenAI Codex** 与 **Anthropic Claude Code** 的各自优势及适用场景：

---

### 最新进展

* **OpenAI Codex**

  * 于 **2025 年 5 月 16 日** 作为研究预览版发布，基于 codex‑1 模型（o3 推理模型的适配版本）。该工具面向 ChatGPT Pro、Team 及 Enterprise 用户开放，能够编写代码、修复错误、运行测试并分析代码库，利用云端执行环境在 **1 到 30 分钟内** 返回结果（[维基百科][1]、[华尔街日报][2]）。
  * 更早于 2025 年 4 月 16 日发布的 **Codex CLI** 为开源工具，可在本地运行（[维基百科][1]）。

* **Claude Code**

  * 作为 Anthropic 产品线的一部分，于 2025 年 2 月 24 日随 **Claude 3.7 Sonnet** 一同发布（[维基百科][3]）。
  * 深度集成至 VS Code、JetBrains、GitHub Actions 等开发环境及企业级 API 中。支持多文件协同、本地代码库上下文感知以及功能丰富的智能 CLI（[维基百科][4]）。
  * 基于 **Claude Sonnet 4** 与 **Opus 4** 等先进模型，在基准测试中表现超越早期版本——尤其是 **Opus 4**，其 SWE-bench 得分达 72.5%（对比 GPT‑4.1 的 54.6%），并能独立运行长达七小时的复杂任务（[IT Pro][5]）。
  * Anthropic 报告称，自 2025 年 5 月 Claude 4 发布以来，Claude Code 带来的收入增长了 **5.5 倍**（[维基百科][3]）。

---

### 开发者与用户反馈

* **博客对比** 指出：

  * **Claude Code 更为成熟、对开发者更友好**，而 Codex 则更像尚需完善的最小可行产品（[Composio][6]）。
  * Codex 可能更适合结构化编码流程，而 Claude Code 则提供更接近对话式、灵活性更强的编程伙伴体验（[Composio][6]）。

* **真实用户经验**（来自 Reddit）：

  > “Codex 有其优势……在通过容器和并行会话构建大型项目时表现惊人”（[Reddit][7]）。
  > “Claude Code 功能更为丰富和完善”——包括结合 GPT‑5 进行调试——而 Codex 则受限于速率限制和稳定性问题（[Reddit][8]）。

* **Geeky Gadgets** 总结：

  * **Codex CLI 针对性能驱动型任务（如数据处理或 SwiftUI 生成）进行了优化**，并提供迭代改进建议。
  * **Claude Code 擅长精确度与用户体验**，具备工具批准、一致设计等特性，但在原始性能上可能略逊一筹（[Geeky Gadgets][9]）。

* **上下文与架构**：

  * Claude Code 直接访问本地项目文件，提供快速、上下文感知的编码支持。
  * Codex 依赖云端加载的代码库，但也能实现类似的上下文访问能力（[维基百科][3]、[Bind AI IDE][10]）。

---

### 简明总结

#### **选择 Claude Code，如果你：**

* 希望获得一个成熟、功能丰富的 CLI 编码助手，深度集成至本地工作流及 IDE 中。
* 重视精确、结构化的输出、出色的内存管理及多文件协调能力。
* 处理复杂或长时间运行的任务——尤其是利用 Claude Opus 4 的高级功能时。
* 偏好一个行为如同对话式专家级伙伴的编码伴侣。

#### **选择 OpenAI Codex，如果你：**

* 需要专注于性能的自动化——例如 SwiftUI 任务或数据工作流中的效率。
* 青睐轻量级、简洁的工具，能无缝融入现有流程而无需过高复杂度。
* 倾向于使用能够推断编码风格、协助代码审查或运行自主云端工作流的模型。

---

### 最终简评

并无绝对的“更好”——取决于你的优化目标：

* **Claude Code** 通常在功能完整性、成熟度、上下文感知及编码能力上领先。
* **OpenAI Codex** 在性能、简洁性及原始自动化能力上表现突出。

---

* [华尔街日报](https://www.wsj.com/articles/openai-launches-new-ai-coding-agent-c8dabc60?utm_source=chatgpt.com)
* [IT Pro](https://www.itpro.com/software/development/anthropic-claude-opus-4-software-development?utm_source=chatgpt.com)

[1]: https://en.wikipedia.org/wiki/OpenAI_Codex?utm_source=chatgpt.com "OpenAI Codex"
[2]: https://www.wsj.com/articles/openai-launches-new-ai-coding-agent-c8dabc60?utm_source=chatgpt.com "OpenAI 发布新型 AI 编程助手"
[3]: https://en.wikipedia.org/wiki/Claude_%28language_model%29?utm_source=chatgpt.com "Claude（语言模型）"
[4]: https://en.wikipedia.org/wiki/Anthropic?utm_source=chatgpt.com "Anthropic"
[5]: https://www.itpro.com/software/development/anthropic-claude-opus-4-software-development?utm_source=chatgpt.com "Anthropic 新 AI 模型或成开发者游戏规则改变者：Claude Opus 4 '在编码领域突破界限'，显著超越 OpenAI GPT-4.1，并能独立编程七小时"
[6]: https://composio.dev/blog/claude-code-vs-openai-codex?utm_source=chatgpt.com "Claude Code 对比 OpenAI Codex"
[7]: https://www.reddit.com/r/ClaudeAI/comments/1l5rxdq/codex_vs_claude_code_real_current_experiences/?utm_source=chatgpt.com "Codex 对比 Claude Code，真实使用体验如何？"
[8]: https://www.reddit.com/r/ClaudeAI/comments/1mtk2d9/a_few_thoughts_on_codex_cli_vs_claude_code/?utm_source=chatgpt.com "关于 Codex CLI 与 Claude Code 的一些思考"
[9]: https://www.geeky-gadgets.com/chatgpt-codex-cli-vs-claude-code-comparison/?utm_source=chatgpt.com "Codex CLI 与 Claude Code 详细对比……"
[10]: https://blog.getbind.co/2025/05/20/openai-codex-compared-with-cursor-and-claude-code/?utm_source=chatgpt.com "OpenAI Codex 与 Cursor、Claude Code 的对比"
