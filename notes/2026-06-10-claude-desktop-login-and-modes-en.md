---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Desktop Login and Modes
translated: false
type: note
---

Question: How do I log in to the Claude desktop app on macOS using the email link flow, and is it true that Cowork, Claude Code, and chat are all bundled together in one app?

Answer:

Two separate things here. Let me split them.

**1. Email magic-link login on macOS**

Yes, that flow works. Steps:

1. Open the Claude desktop app → click **Continue with email**.
2. Enter your email → Claude sends a sign-in link.
3. Open your mail client, click the link → it opens your default browser.
4. Browser authenticates, then hands off back to the app via a `claude://` deep link (macOS prompts "Open in Claude?" → allow it).

The browser→app handoff is the deep-link redirect. If it *doesn't* jump back automatically, it's usually because (a) the link opened in a browser where you're not the same logged-in session, or (b) the deep-link handler didn't register. Workaround: copy the link and paste it directly, or just use **Continue with Google** which skips the email round-trip entirely.

**2. "Cowork, Claude, chat all in one app" — partly right**

Let me verify the current state rather than guess, since the desktop app surface has been changing.Confirmed. Both parts of your understanding are right.

**Login flow:** Email magic-link works exactly as you described — enter email in the app, click the link in your mail client, browser authenticates, then deep-links back to the app. Google SSO is the faster path if you want to skip the round-trip.

**One app, multiple modes:** Yes. The Claude Desktop app features three main modes at the top of the interface: Chat (classic conversation, like the web), Cowork (autonomous agent that works on your files), and Claude Code access. You switch via a mode selector/tab at the top.

A few details worth knowing given your setup:

- Cowork runs inside a sandboxed virtual machine on your computer, which keeps it from modifying system files or accessing anything outside its sandbox without your permission. That VM spin-up is why Cowork is heavier than Chat — relevant on your 16GB M2 Air. For real agentic file work you may feel the RAM pressure; the workstation at `<IP_ADDRESS>` (62GB) is the better host if you can run desktop there.
- Claude Code is the CLI coding agent (write code, run tests, submit PRs, manage repos from the terminal); Cowork lives inside the desktop app and was introduced after Anthropic noticed developers using Claude Code for far more than coding. Both now share the same computer-use capability.
- Requires a paid plan — Pro at $20/mo now includes Chat, Cowork, and Claude Code access; Free is excluded.
- The default model is Opus 4.8 on the heavy tier and Sonnet 4.6 on the daily tier.

Since you're terminal-first (Warp) and vibe-coding fast, Claude Code is your natural entry point and Cowork is the GUI-ish file-automation layer you'll reach for less often.

References:

- [Claude Desktop explained: chat, Cowork and Code](https://www.clickforest.com/en/blog/claude-desktop-explained)
- [Claude Code Can Now Run Your Desktop — DevOps.com](https://devops.com/claude-code-can-now-run-your-desktop/)
- [Claude Desktop System Requirements 2026 — Houtini](https://houtini.com/articles/claude-desktop-system-requirements/)
