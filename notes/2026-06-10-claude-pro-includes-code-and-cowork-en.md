---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Pro Includes Code and Cowork
translated: false
type: note
---

I'll search for current information on what the Claude Pro plan includes for Claude Code and Claude Cowork.Question: When I open a Claude Pro plan (Pro, not Plus; account-based, not API), will I be able to use Claude Code with that account? What about Claude Cowork?

Answer:

Yes to both. Your Pro account ($20/mo) authenticates Claude Code and Claude Cowork directly — no API key, no Console billing.

**Claude Code:** With Pro and Max plans, you now have access to both Claude on the web, desktop, and mobile apps and Claude Code in your terminal with one unified subscription. You just download Claude Code and sign in with your Claude credentials — same account, no separate API setup. Anthropic briefly ran an A/B test removing Claude Code from Pro for approximately 2% of new subscribers, but reverted it after community pushback. As of now it's included in Pro.

**Claude Cowork:** Also included. When Anthropic first launched Claude Cowork on January 12, 2026, it was only available to Max subscribers... the demand was so loud that four days later, on January 16, 2026, Anthropic opened Cowork up to all Pro subscribers.

Two important caveats for your setup:

**1. Watch your `ANTHROPIC_API_KEY` env var.** Since you run a lot through OpenRouter/API providers and consume ~1B tokens, you likely have this exported in your shell. If you have an ANTHROPIC_API_KEY environment variable set on your system, Claude Code will use this API key for authentication instead of your Claude subscription, resulting in API usage charges rather than using your subscription's included usage.

To force subscription auth, unset it before launching:

```bash
# one-off
env -u ANTHROPIC_API_KEY claude

# or check what's set
echo $ANTHROPIC_API_KEY

# verify which auth Claude Code is using
claude  # then run /status inside — shows "Pro" vs API billing
```

**2. Shared usage limits.** Both Pro and Max plans offer usage limits that are shared across Claude and Claude Code, meaning all activity in both tools counts against the same usage limits. Pro's window is tight for "short coding sprints in small codebases" — given your workload you'll hit the ceiling fast. When you reach your usage limits... Enable usage credits to continue using Claude with your Pro plan after hitting the included usage limit. That credit overflow bills at standard API rates (distinct from Pro/Max Plan pricing).

**3. Cowork runs only while desktop is open.** Cowork tasks only run while the Claude Desktop app is open on your computer. Close the app and the session ends. Relevant if you'd want to schedule agent runs on your Air vs. the workstation.

Bottom line: Pro covers both as a unified account-based subscription. For your token volume, Pro limits will bite quickly — Max 5x/20x is the realistic tier if Claude Code becomes a daily driver alongside your existing API spend.

References:

- [Use Claude Code with your Pro or Max plan](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan)
- [Claude Code product page](https://claude.com/product/claude-code)
- [What is the Pro plan?](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan)
- [Claude Code on Pro: What's Actually Included Right Now](https://codeongrass.com/blog/claude-code-pro-plan-whats-included/)
