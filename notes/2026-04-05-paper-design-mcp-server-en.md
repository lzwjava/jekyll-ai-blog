---
audio: false
generated: true
image: false
lang: en
layout: post
title: Paper.design MCP Server Overview
translated: false
type: note
---

**Question:** How good is the Paper.design MCP server?

**Answer:**

## Overview of Paper.design MCP

Paper.design is a relatively new, HTML/CSS-native design tool (currently in open alpha) that has built one of the most capable MCP server integrations among design tools available today. Here is a comprehensive breakdown:

---

## What Makes It Stand Out

### 1. Bidirectional Read + Write Access

Most design tool MCP integrations are read-only. Paper.design exposes 24 tools through an authenticated MCP server — and unlike most tool integrations that only let AI agents read your work, Paper supports full bidirectional access. An AI agent running in Claude Code or Cursor can not only inspect your design, it can modify it.

This is a major differentiator. For comparison, Figma's MCP server exposes only three core tools and is primarily read-only.

### 2. Rich Tool Surface (24 Tools)

Paper.design's MCP server exposes 24 tools split into read operations (get_selection, get_jsx, get_screenshot, get_computed_styles) and write operations (create_artboard, write_html, set_text_content, update_styles, rename_layer, duplicate_node, delete_node).

### 3. Native HTML/CSS Foundation = LLM-Friendly

Because Paper is based on web technology and LLMs are really good at understanding the DOM, the results can be impressive. There is no translation step — the canvas is already HTML/CSS, so agents operate in their native language.

### 4. Powerful Cross-Tool Workflows

Because the Paper MCP supports both reading and writing to your files, you can use the MCP server to pull context from other sources into your design files. This unlocks a bunch of workflows that were previously tedious to carry out, like syncing tokens from your design system or using real content for your designs.

It also integrates with other MCP servers. For example, you can connect the Figma MCP and the Paper MCP simultaneously to migrate design tokens, or connect Notion MCP to populate real content into design frames.

### 5. Wide IDE Compatibility

Setup in Claude Code is a single terminal command. Cursor users get a one-click deeplink. VS Code Copilot, Codex, and OpenCode also work out of the box.

---

## Strengths vs. Figma MCP

| Feature | Paper.design MCP | Figma MCP |
| --- | --- | --- |
| Tools exposed | 24 | 3 |
| Read + Write | ✅ Both | ❌ Read-only |
| Canvas format | HTML/CSS (LLM-native) | Proprietary SVG |
| Setup complexity | Low (1 command) | Higher (Code Connect needed) |
| Free tier MCP calls | 100/week | Requires paid plan |
| Pro tier MCP calls | 1M/week | Available on Professional plan |

---

## Limitations & Caveats

- **Still in open alpha** — expect rough edges and bugs. The tool is in open alpha and recently launched cool additions like a desktop app and a powerful MCP server.
- **Developer-oriented UX.** Paper's canvas really comes alive if you are comfortable in a code editor. Its MCP integration, Tailwind export, and DOM-native architecture are for people using CSS. Non-technical designers may find the setup friction too high.
- **Free tier is limited.** Paper's free tier is functional for exploring the canvas, but the 100 MCP calls per week limit means AI-assisted workflows hit a ceiling quickly.
- **WSL issues.** When using Windows Subsystem for Linux (WSL) you may not be able to access the local MCP server at <http://127.0.0.1:29979/mcp>.

---

## Verdict

Paper.design's MCP is **one of the best-designed design-tool MCP integrations currently available**, particularly for developer-designers or solo builders using AI coding agents like Claude Code or Cursor. It excels due to its bidirectional access, large tool surface, and the natural fit between its HTML/CSS canvas and how LLMs process code. The main trade-off is that it is still early-stage software, and the workflow requires technical comfort with terminals and IDEs.

**Best for:** Designer-developers, solo builders, AI-first workflows, Tailwind/React teams.

**Not ideal for:** Pure designers unfamiliar with code editors, or large teams needing enterprise maturity.

---

**References:**

- [Paper.design MCP Documentation](https://paper.design/docs/mcp)
- [Figma MCP vs Paper.design Comparison — SFAI Labs](https://sfailabs.com/guides/figma-mcp-vs-paper)
- [Paper.design Review — Banani Blog](https://www.banani.co/blog/paper-design-mcp-review)
- [Paper.design: GPU Shaders, MCP and Vibe Coding — Abduzeedo](https://abduzeedo.com/paperdesign-gpu-shaders-mcp-and-vibe-coding-designers)
- [A Guide to Paper and Claude Code for Designers](https://adplist.substack.com/p/a-guide-to-paper-and-claude-code)
- [Paper.design Pricing](https://paper.design/pricing)
