---
audio: false
generated: true
image: false
lang: en
layout: post
title: Voice Coding With Push to Talk
translated: false
type: note
---

**Question:** How does Peter Steinberger use voice to control his AI coding assistant, for example with Claude Code or Codex, since they don't support voice input natively?

**Answer:**

Peter Steinberger, the creator of OpenClaw (formerly Clawdbot/Moltbot), extensively used **voice input** for interacting with his AI coding agents and assistants, even though tools like Claude Code (Claude-based coding interfaces) and OpenAI's Codex (or later GPT Codex variants) do not natively support direct voice input.

He described his workflow in interviews (notably on the Lex Fridman Podcast #491 and others):

- He ran multiple terminal instances (often in a grid layout, 3×3 or similar) with AI coding agents like Codex CLI as his primary driver.
- For **short terminal commands** (e.g., navigating folders), he typed normally as it was faster.
- For **interacting with the AI agent** (giving instructions, having conversations about code, describing features, reviewing PRs, or directing the agent), he used **voice** extensively.
- He pressed a **walkie-talkie / push-to-talk (PTT) button** (or similar hotkey) to start recording, then spoke naturally in phrases or full sentences — essentially holding a back-and-forth conversation with the agent.
- The voice was converted to text (via speech-to-text) and fed into the agent's prompt/input stream.

This voice-driven conversational style was so intensive that he once **lost his voice** from overuse.

He preferred this over typing long prompts because:

- It felt more natural and faster for complex or iterative instructions.
- It aligned with his "just talk to it" philosophy for agentic engineering.
- He sometimes used **slash commands** for repetitive tasks (e.g., PR reviews), but mostly relied on free-form spoken conversation.

Although native voice is missing in Claude Code / Codex, he bridged the gap with:

- System-level or third-party **speech-to-text** tools (he has referenced tools like Wispr Flow in related contexts for dictation).
- Custom hotkeys / PTT setups in his terminal/multiplexer environment (tmux or similar) to quickly dictate into the active agent session.

In later setups (e.g., with OpenClaw itself), voice features expanded — including Voice Wake, Talk Mode, and integrations with ElevenLabs for speech — but for pure coding with Claude Code / Codex, the core method was **PTT + speech-to-text → text prompt to the agent**.

This allowed him to "vibe code" at high speed, ship massive amounts of code (thousands of commits), and treat the AI like a real-time collaborator he could talk to.

**References:**

- [Lex Fridman Podcast #491 Transcript with Peter Steinberger](https://lexfridman.com/peter-steinberger-transcript)
- [YouTube: OpenClaw – Peter Steinberger | Lex Fridman Podcast #491](https://www.youtube.com/watch?v=YFjfBk8HI5o)
- [Peter Steinberger's blog posts on agentic engineering and Codex usage](https://steipete.me/posts/just-talk-to-it)
