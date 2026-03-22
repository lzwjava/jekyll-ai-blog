---
audio: false
generated: true
image: false
lang: en
layout: post
title: Comparing OpenCode Export and Claude Copy
translated: false
type: note
---

**Question:** Is the analysis comparing OpenCode's `/export` (session transcript) feature versus Claude Code's `/copy` button accurate — specifically that OpenCode exports the full agentic "journey" while Claude Code only copies the last response?

**Answer:**

Your analysis is **mostly correct**, but a few details need refinement based on the actual documented behavior of both tools.

---

## OpenCode's `/export` Command

OpenCode's TUI provides an `/export` command that exports the current conversation to Markdown and opens it in your default editor (using the `$EDITOR` environment variable).

The export dialog (`DialogExportOptions`) allows the user to set the output filename (defaulting to `session-<id-prefix>.md`), toggle inclusion of thinking blocks, tool details, and assistant metadata, and choose to open the transcript in `$EDITOR` without writing to disk.

So it is indeed a **full-session, structured export** — not just the last turn. The granular toggles (thinking blocks, tool details, metadata) confirm it captures the entire agentic process, not just final responses.

---

## Claude Code's `/copy` Command

Claude Code's behavior is more nuanced than simply "copy the last response":

Claude Code's `/copy` command copies Claude's most recent response to your clipboard. If the response has code blocks, you get an interactive picker to grab individual blocks instead of the full response. You can also pass a number to go further back — `/copy 2` grabs the second-to-last response.

However, Claude Code **does** have a full export option too:

The `/export` command in Claude Code writes the full conversation as plain text directly to disk — no prompt, no dialog. The export is plain text only, no JSON, no structured format. It is a transcript.

The key gap is that Claude Code has no prominent built-in export button in its UI; conversations are stored in `~/.claude/projects/` as JSONL files. This has led developers to build third-party tools to fill the gap.

---

## The Real Distinction

Your core point holds up well:

| Feature | OpenCode `/export` | Claude Code `/copy` |
|---|---|---|
| **Scope** | Full session, all turns | Last response (or N responses) |
| **Format** | Structured Markdown with toggles | Plain text or clipboard |
| **Tool details** | Toggleable (thinking blocks, tool calls) | Not included by default |
| **Thinking traces** | Toggleable | Hidden by default; thinking traces are not included when manually copying terminal sessions |
| **Design philosophy** | First-class TUI export dialog | Per-response clipboard helper |

Transcripts from Claude Code sessions capture extremely important context — what was asked for, what Claude suggested, decisions made, and Claude's own justification for the decisions it made while implementing a feature. The community clearly values this, which is exactly why tools like `claude-code-transcripts` (by Simon Willison) were created to compensate for Claude Code's lack of a polished built-in export flow.

---

## One Correction to Your Framing

OpenCode is **not** built on Zig or "OpenTUI/Zig" as described. OpenCode's interactive TUI is built with Bubble Tea (a Go framework) for a smooth terminal experience, and it supports multiple AI providers including Anthropic Claude, OpenAI, Google Gemini, AWS Bedrock, Groq, Azure OpenAI, and OpenRouter.

So: **your functional comparison is accurate**, but the architectural description (Zig/OpenTUI) is incorrect — OpenCode is a Go + Bubble Tea project.

**References:**

- [OpenCode TUI Documentation](https://opencode.ai/docs/tui/)
- [OpenCode TUI Commands — DeepWiki](https://deepwiki.com/anomalyco/opencode/9.2-tui-commands)
- [OpenCode GitHub (opencode-ai/opencode)](https://github.com/opencode-ai/opencode)
- [Claude Code Export Guide — kentgigger.com](https://kentgigger.com/posts/claude-code-export-save-conversation)
- [Simon Willison: A new way to extract detailed transcripts from Claude Code](https://simonwillison.net/2025/dec/25/claude-code-transcripts/)
- [ZeroSumQuant/claude-conversation-extractor](https://github.com/ZeroSumQuant/claude-conversation-extractor)