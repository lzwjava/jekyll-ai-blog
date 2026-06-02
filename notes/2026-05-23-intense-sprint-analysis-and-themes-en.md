---
audio: false
generated: true
image: false
lang: en
layout: post
title: Intense Sprint Analysis and Themes
translated: false
type: note
---

Here's the analysis of the last 2 weeks (May 9–23, 2026):

============================================================
  OPENCLACKY — LAST 2 WEEKS CHANGE ANALYSIS
============================================================

TOTALS: 113 commits | 433 files changed | +18,636 / -6,886 lines

BREAKDOWN BY TYPE:
  feat     39  (35%)  — New features
  fix      34  (30%)  — Bug fixes
  chore    17  (15%)  — Version bumps, scripts, maintenance
  docs     12  (11%)  — Changelogs, READMEs, guides
  test      3   (3%)  — Test fixes/isolation
  perf/refactor/style/other  8  (7%)

VERSIONS SHIPPED: 1.0.3 → 1.0.4 → 1.0.5 → 1.1.0 → 1.1.1 → 1.1.2 → 1.1.3 → 1.1.4 → 1.1.5 → 1.1.6
(10 releases in 14 days)

============================================================
  MAJOR THEMES
============================================================

1. WEB UI OVERHAUL (lib/clacky/web — 126 file changes, biggest area)
   - Streaming: real-time token streaming, TTFT display, thinking progress
   - Syntax highlighting + per-block copy buttons (#152)
   - Font size setting (S/M/L) with proportional scaling (#147)
   - LaTeX rendering support
   - Cache rate display
   - Code block UI polish, hover effects
   - Mobile responsive fixes (#165)
   - Session list: fold cron sessions into groups (#163)
   - Rename via modal dialog instead of inline (#113)

2. CHANNEL ADAPTERS (Telegram, Discord, DingTalk, Feishu, WeChat)
   - Telegram channel adapter (new)
   - Discord adapter: REST + Gateway + Web UI (#112)
   - DingTalk via Stream Mode WebSocket (#112)
   - Feishu CLI install & auth onboarding (#98)
   - WeChat: SendQueue with batching, throttling, retry (#127)
   - Enable/disable toggle for channels (#108)
   - Channel-manager skill rename for better trigger matching (#120)
   - Local image proxy via /api/local-image (#93)
   - File-action API unification with download support (#153)

3. LLM PROVIDERS & MODEL SUPPORT
   - Added Qwen 3.6 provider
   - Added OpenRouter models + MiMo 2.5
   - Added Kimi Code (Coding Plan) preset (#89)
   - DeepSeek price fix
   - Thinking level feature
   - Free brand / brand config system
   - Provider promo hints (#109)

4. SERVER & CLI (lib/clacky/server — 50 file changes)
   - USR1 hot-reload session info drop fix (#142)
   - Server command: --help/-h/--bind/-b, -p alias (#135)
   - Hot-reload upgrade fix (#143)
   - Local image proxy endpoint
   - Dockerfile + CLACKY_ACCESS_KEY validation (#140)
   - Debian apt mirror support + CN mirror config (#139)

5. BILLING SYSTEM
   - New billing system with USD/CNY currency settings (#166)

6. AGENT & SYSTEM
   - System prompts aligned with Claude Code behavioral rules (#96)
   - Memory persistence
   - Context compression
   - Running config + agent count limits (perf)
   - Subagent session bar fix

7. PLATFORM COMPAT
   - WSL: UTF-8 encoding fixes (#130, #164)
   - Windows: native config detection on WSL (#129)
   - Ruby 4.0 compatibility (CI + terminal markdown rendering)
   - macOS: Xcode command auto-install

============================================================
  HOTTEST FILES (by churn)
============================================================
  lib/clacky/web/     — 126 changes (UI overhaul)
  lib/clacky/server/  — 50 changes (API + infra)
  lib/clacky/agent/   — 17 changes (agent behavior)
  lib/clacky/ui2/     — 16 changes (TUI)
  lib/clacky/cli.rb   — 10 changes (CLI)
  spec/clacky/        — 35 changes (tests)

============================================================
  CONTRIBUTORS
============================================================
  yafei@dao42.com               — primary author (68 changes)
  huzhuangyongbiao@gmail.com    — 13 changes
  leihaibo1992@gmail.com        — 7 changes
  rina@RinadeMacBook-Air.local  — 2 changes

============================================================
  TAKEAWAY
============================================================
This was a very intense sprint — 10 releases in 2 weeks. The main thrust was transforming OpenClacky from a CLI/TUI tool into a full platform with:
  (a) A polished streaming Web UI
  (b) Multi-channel messaging (Telegram/Discord/DingTalk/Feishu/WeChat)
  (c) A billing system
  (d) Expanded LLM provider support

The Web UI alone got 126 file changes — it's clearly the primary investment area. Channel adapters are the second big push, making OpenClacky a multi-platform chat agent, not just a CLI tool.
