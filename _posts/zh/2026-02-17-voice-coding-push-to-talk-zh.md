---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 语音编码与按键发话
translated: true
type: note
---

**问题：** Peter Steinberger 如何用语音控制他的 AI 编码助手（例如 Claude Code 或 Codex），既然它们原生不支持语音输入？

**回答：**

Peter Steinberger（OpenClaw 的创始人，前 Clawdbot/Moltbot）广泛使用**语音输入**与他的 AI 编码代理和助手交互，尽管 Claude Code（基于 Claude 的编码界面）和 OpenAI 的 Codex（或后续 GPT Codex 变体）原生不支持直接语音输入。

他在访谈中（特别是 Lex Fridman Podcast #491 等）描述了他的工作流：

- 他运行多个终端实例（通常以网格布局，如 3×3 或类似），并以 Codex CLI 等 AI 编码代理作为主要驱动。
- 对于**短终端命令**（如导航文件夹），他仍然手动输入，因为这样更快。
- 对于**与 AI 代理交互**（下达指令、讨论代码、描述功能、审查 PR 或指导代理），他大量使用**语音**。
- 他按下**对讲机/按键通话（PTT）按钮**（或类似快捷键）开始录音，然后自然地说出短语或完整句子——实质上是与代理进行对话式交流。
- 语音被转换为文本（通过语音转文字），并输入到代理的提示/输入流中。

这种高强度的语音对话式交互，甚至让他**因过度使用而失声**。

他更倾向于语音而非输入长提示，因为：
- 对于复杂或迭代指令，语音更自然、更快。
- 这与他“直接对话”（just talk to it）的代理工程理念相符。
- 他有时用**斜杠命令**（slash commands）处理重复性任务（如 PR 审查），但主要依赖自由形式的口头对话。

尽管 Claude Code / Codex 原生不支持语音，他通过以下方式弥补：
- 系统级或第三方**语音转文字**工具（他在相关场景中提到过 Wispr Flow 等听写工具）。
- 在终端/多路复用器环境（tmux 或类似）中设置自定义快捷键/PTT，快速将语音输入到活动代理会话中。

在后续设置中（如 OpenClaw 本身），语音功能扩展——包括语音唤醒（Voice Wake）、对话模式（Talk Mode）以及与 ElevenLabs 的语音集成——但在纯编码场景中使用 Claude Code / Codex 时，核心方法仍是**PTT + 语音转文字 → 文本提示给代理**。

这让他能以高速“vibe 编码”，输出大量代码（数千次提交），并将 AI 视作实时协作者对话。

**参考：**

- [Lex Fridman Podcast #491 与 Peter Steinberger 的访谈记录](https://lexfridman.com/peter-steinberger-transcript)
- [YouTube：OpenClaw – Peter Steinberger | Lex Fridman Podcast #491](https://www.youtube.com/watch?v=YFjfBk8HI5o)
- [Peter Steinberger 关于代理工程和 Codex 使用的博客文章](https://steipete.me/posts/just-talk-to-it)