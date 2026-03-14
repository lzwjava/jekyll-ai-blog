---
audio: false
generated: true
image: false
lang: en
layout: post
title: WebFetch Tool Guide for Claude Code
translated: false
type: note
---

Question: What does the `WebFetch` tool do in Claude Code, and how should it be used?

Answer:

## WebFetch Tool in Claude Code

The `WebFetch` tool is a built-in Claude Code tool that allows Claude to **retrieve and analyze web page content** during an agentic session.

---

### What It Does

| Feature | Detail |
|---|---|
| **Input** | A URL + a prompt describing what to extract |
| **Process** | Fetches the URL, converts HTML → Markdown, then runs your prompt against the content using a small/fast model |
| **Output** | The model's response about the page content |
| **Cache** | 15-minute self-cleaning cache to speed up repeated fetches of the same URL |

---

### Key Behaviors

**✅ What it handles well:**
- Public web pages (blogs, docs, news articles, etc.)
- HTTP URLs — automatically upgraded to HTTPS
- Large pages — results may be summarized if content is too big
- Redirects — notifies you of the redirect URL, so you can make a new request manually

**❌ What it cannot do:**
- Access **authenticated or private URLs** (Google Docs, Confluence, Jira, GitHub private repos, etc.) — it will **fail**
- Modify any files (read-only tool)

---

### Priority Rules

```
1. If an MCP-provided web fetch tool is available → use THAT instead
2. For GitHub URLs → prefer the gh CLI via Bash (gh pr view, gh issue view, gh api)
3. For authenticated services → use a specialized MCP tool, not WebFetch
4. For public URLs → WebFetch is fine
```

---

### Practical Example

```
URL:    https://docs.anthropic.com/en/docs/overview
Prompt: "Summarize the main features of Claude's API"
```

Claude fetches the page, parses its HTML into Markdown, and then a fast model extracts whatever the prompt asks for — returning a clean summary to you.

---

### Why the Warning About Auth URLs?

Many developers instinctively paste a Jira ticket, GitHub PR, or Google Doc URL — but WebFetch has **no session/cookie/token**, so it hits a login wall and fails. The tool warns you upfront to **check if the URL requires authentication first**, and if so, find an appropriate MCP connector instead (e.g., a GitHub MCP tool, a Confluence MCP tool, etc.).