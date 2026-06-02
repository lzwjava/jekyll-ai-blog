---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Paper.design MCP服务器概览
translated: true
type: note
---

**问：** Paper.design MCP 服务器到底有多强大？

**答：**

## Paper.design MCP 概览

Paper.design 是一款相对较新、原生基于 HTML/CSS 的设计工具（目前处于开放测试阶段），目前已构建了当今可用设计工具中功能最为强大的 MCP 服务器集成之一。以下是详细分析：

---

## 脱颖而出的关键特性

### 1. 双向读写访问

大多数设计工具的 MCP 集成仅支持只读模式。Paper.design 通过经过身份验证的 MCP 服务器暴露了 24 个工具——与大多数工具集成仅允许 AI 代理查看工作不同，Paper 支持完全的双向访问。运行在 Claude Code 或 Cursor 中的 AI 代理不仅可以检查你的设计，还可以修改它。

这是一个主要区别。作为对比，Figma 的 MCP 服务器仅暴露三个核心工具，且主要为只读。

### 2. 丰富的工具集（24 个工具）

Paper.design 的 MCP 服务器暴露的 24 个工具分为读取操作（get_selection, get_jsx, get_screenshot, get_computed_styles）和写入操作（create_artboard, write_html, set_text_content, update_styles, rename_layer, duplicate_node, delete_node）。

### 3. 原生 HTML/CSS 基础 = 大语言模型友好

由于 Paper 基于 Web 技术，而大语言模型非常擅长理解 DOM，因此效果令人印象深刻。无需翻译步骤——画布已经是 HTML/CSS，因此代理能够以其原生语言进行操作。

### 4. 强大的跨工具工作流

由于 Paper MCP 支持对设计文件的读写，你可以使用 MCP 服务器将其他来源的上下文引入设计文件。这解锁了许多以前执行起来繁琐的工作流，例如同步设计系统中的令牌，或在设计中使用真实内容。

它还支持与其他 MCP 服务器集成。例如，你可以同时连接 Figma MCP 和 Paper MCP 来迁移设计令牌，或者连接 Notion MCP 以将真实内容填充到设计框架中。

### 5. 广泛的 IDE 兼容性

在 Claude Code 中设置只需一条终端命令。Cursor 用户可以通过一键深度链接访问。VS Code Copilot、Codex 和 OpenCode 也可以直接使用。

---

## 与 Figma MCP 的优劣对比

| 特性 | Paper.design MCP | Figma MCP |
|---|---|---|
| 暴露的工具数量 | 24 | 3 |
| 读写支持 | ✅ 双向 | ❌ 只读 |
| 画布格式 | HTML/CSS（LLM原生） | 专有 SVG |
| 设置复杂度 | 低（1 条命令） | 较高（需 Code Connect） |
| 免费版 MCP 调用限额 | 100次/周 | 需要付费计划 |
| 专业版 MCP 调用限额 | 100万次/周 | 需专业版计划 |

---

## 局限性及注意事项

- **仍处于开放测试阶段**——可能会遇到小问题和Bug。该工具目前为开放测试版，最近推出了桌面应用和强大的 MCP 服务器等酷炫功能。
- **面向开发者的用户体验。** 如果你精通代码编辑器，Paper的画布才能真正发挥威力。它的MCP集成、Tailwind导出以及DOM原生架构都是为使用CSS的人设计的。非技术背景的设计师可能会觉得设置门槛过高。
- **免费版有限制。** Paper的免费版可用于探索画布功能，但每周100次MCP调用的限制意味着AI辅助的工作流很快会遇到瓶颈。
- **WSL问题。** 使用 Windows 子系统 Linux（WSL）时，你可能无法通过 <http://127.0.0.1:29979/mcp> 访问本地 MCP 服务器。

---

## 最终评价

Paper.design 的 MCP **是当前可用的设计工具MCP集成中设计最佳的产品之一**，尤其适合开发者-设计师或使用 Claude Code 或 Cursor 等 AI 编码代理的独立开发者。其优势在于双向访问、丰富的工具接口，以及其 HTML/CSS 画布与大语言模型处理代码的方式间的高度契合。主要权衡点在于该软件仍处于早期阶段，工作流需要熟悉终端和 IDE 的技术舒适度。

**最适合：** 设计师-开发者、独立开发者、AI优先的工作流、Tailwind/React 团队。

**不理想场景：** 完全不熟悉代码编辑器的纯粹设计师，或需要企业级成熟度的大型团队。

---

**参考资料：**

- [Paper.design MCP 文档](https://paper.design/docs/mcp)
- [Figma MCP 与 Paper.design 对比 — SFAI Labs](https://sfailabs.com/guides/figma-mcp-vs-paper)
- [Paper.design 评测 — Banani Blog](https://www.banani.co/blog/paper-design-mcp-review)
- [Paper.design: GPU 着色器、MCP 与氛围编码 — Abduzeedo](https://abduzeedo.com/paperdesign-gpu-shaders-mcp-and-vibe-coding-designers)
- [给设计师的 Paper 与 Claude Code 使用指南](https://adplist.substack.com/p/a-guide-to-paper-and-claude-code)
- [Paper.design 定价](https://paper.design/pricing)
