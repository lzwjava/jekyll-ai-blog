---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Claude Code Leak Rewrite
translated: false
type: note
---

Question: What is the `ultraworkers/claw-code` GitHub repository, and is it worth using?

Answer:

## Overview of `ultraworkers/claw-code`

This repository has a dramatic backstory that explains everything about what it is and why it went viral.

### The Origin: The Claude Code Leak

On March 31, 2026, Anthropic accidentally shipped a `.map` sourcemap file inside a Claude Code npm update. Within minutes, the 600k lines of code were mirrored, analyzed, ported to Python and other languages, and uploaded across the internet.

The leak exposed approximately 512,000+ lines of TypeScript, 44 hidden feature flags, an always-on background agent called KAIROS, and a stealth mode designed to hide Anthropic employee contributions to open-source projects.

### What `claw-code` Actually Is

`claw-code` is **not a dump of leaked proprietary code**. The maintainers carefully avoided storing the original leaked snapshot, focusing instead on a functional Python-first rewrite and a high-performance Rust port.

The repository was born as a mirror that later became a complete rewrite of the Claude Code app, first in Python and later in Rust, and crossed 100,000 stars on GitHub — making it the fastest-growing repo in GitHub history, surpassing even the previous record holder.

The repo is now a **Rust-dominant project** (92.9% Rust, 7.1% Python) with these main components:
- `crates/api-client` — API client with provider abstraction and streaming
- `crates/runtime` — session state, MCP orchestration, prompt construction
- `crates/tools` — tool manifest definitions and execution framework
- `crates/claw-cli` — interactive REPL and project bootstrap flows

### Is It "Good"? An Honest Assessment

**Pros:**
- **Massive community traction** — 153k stars and 101k forks is unprecedented
- **Clean-room approach** — designed to avoid direct copyright infringement by reimplementing architecture from scratch
- **Rust port** — aims to deliver a faster, memory-safe harness runtime compared to the original TypeScript
- **Educational value** — useful for studying AI agent harness engineering, tool wiring, and orchestration patterns

**Cons / Cautions:**
- The Python workspace is not yet a complete one-to-one replacement for the original system; it still contains fewer executable runtime slices than the archived source.
- **Legal uncertainty** — the legal status of claw-code remains unresolved. No litigation has been filed against the clean-room rewrite as of early April 2026, but Anthropic has not published a formal post-mortem either.
- **Ownership in flux** — the repo itself notes it is *temporarily locked during an ownership transfer*, with active maintenance happening at `ultraworkers/claw-code-parity`.
- **Malware risk in the ecosystem** — a malicious GitHub repository used the Claude Code exposure as a lure, distributing an infostealer (Vidar) and a proxy malware (GhostSocks) disguised as a leaked source archive. Always verify what you're downloading from related repositories.

### Bottom Line

`claw-code` is a **fascinating engineering and community phenomenon**, useful for learning about AI agent harness design. However, it is **not production-ready** as a full Claude Code replacement, its legal status is unresolved, and the ecosystem around it has been polluted with malware lookalikes. If you're a developer curious about agent internals, the Rust port is interesting to explore — but do so cautiously and only from the verified repo.

References:

- [Leaked Claude Code source spawns fastest growing repository in GitHub's history – Cybernews](https://cybernews.com/tech/claude-code-leak-spawns-fastest-github-repo/)
- [Diving into Claude Code's Source Code Leak – Engineers Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code)
- [Where is Claude Code Leaked Source Code? – Medium](https://medium.com/data-science-in-your-pocket/where-is-claude-code-leaked-source-code-9a5b1d00cd2a)
- [Fake Claude Code source downloads delivered malware – The Register](https://www.theregister.com/2026/04/02/trojanized_claude_code_leak_github/)
- [512,000 Lines, One Night: The Legal Crisis of AI Clean Rooms – Bean Kinney](https://www.beankinney.com/512000-lines-one-night-zero-permission-the-claude-code-leak-and-the-legal-crisis-of-ai-clean-rooms/)
- [Critical Vulnerability in Claude Code Emerges Days After Source Leak – SecurityWeek](https://www.securityweek.com/critical-vulnerability-in-claude-code-emerges-days-after-source-leak/)
