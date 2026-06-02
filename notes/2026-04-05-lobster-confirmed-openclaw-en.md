---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lobster Confirmed as OpenClaw
translated: false
type: note
---

Question: After reading this Nextcloud Talk Bot troubleshooting blog post, can you confirm — does "龙虾" (lobster) refer to OpenClaw (an AI agent), not Claude Code?

Answer:

Yes, you are **correct** — and it's a clever nickname!

## "龙虾" = OpenClaw (AI Agent), NOT Claude Code

The logic is straightforward:

- **OpenClaw** → "Claw" → lobster claw → **龙虾 (lobster)** 🦞
- There's even a literal 🦞 emoji at the bottom of your blog note: *"the last error should be resolved by the `localhost:8080` fix. 🦞"* — that's OpenClaw signing off.

---

## Summary of Your Troubleshooting Workflow

Reading your blog post and your message, here's the workflow you described:

### 1. Download Source Code Locally Instead of Web Search
Rather than asking the AI agent to search the web, you had OpenClaw **download the actual source code** of both:
- **OpenClaw** itself
- **Nextcloud Talk**

This gave the model precise, grounded context — much more accurate than web search snippets.

### 2. Source Code Patch via OpenClaw
OpenClaw identified and applied a real **source code patch**, specifically changing the payload type enum in `dist/channel-W1Ul32NW.js`:
- **Before:** `z.enum(["Create", "Update", "Delete"])`
- **After:** `z.enum(["Create", "Update", "Delete", "Activity"])`

This was a non-trivial fix that required reading actual source code, not documentation.

### 3. Cross-Validation Between OpenClaw and Claude Web Chat
You used a smart **two-model cross-checking strategy**:
- Have OpenClaw summarize the current state / findings
- Paste that summary into **Claude.ai web chat** for independent verification
- Compare the two perspectives to catch blind spots or errors

### 4. Frequent Log Review
You kept instructing OpenClaw to **re-check logs** repeatedly, which is how layered bugs get uncovered — each fix revealed the next hidden error (401 → 400 → 404, as shown in the blog).

---

## Why It Still Took 2–3 Hours Each Time

As your blog explains perfectly:

- **Two problems masked each other** — fixing signature rejection (401) revealed payload format error (400), which then revealed the `localhost` trap (404)
- **No single log showed everything** — Nextcloud logs and OpenClaw logs each showed different partial pictures
- **Multiple config files** across Nextcloud Docker, OpenClaw JSON, and the bot database registration

Even with a powerful AI agent, **layered infrastructure bugs** across Docker networking, URL config, and source code behavior require systematic patience — not just one-shot fixes.

---

## Key Insight from Your Approach

> Giving the model **precise local source code** as input, rather than relying on web search, dramatically improves its accuracy on complex debugging tasks.

This is a genuinely good technique for AI-assisted debugging in the current era — the model's reasoning is only as good as the context you give it.

References:

- [2026-04-05-nextcloud-talk-bot-troubleshooting-en.md](https://github.com/lzwjava/blog-source/blob/main/notes/2026-04-05-nextcloud-talk-bot-troubleshooting-en.md)
