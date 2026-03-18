---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parallel Claude Code With Modular CLIs
translated: false
type: note
---

Yes, exactly right! When your CLI tool has well-separated subcommands/modules, you can run parallel Claude Code instances safely. Here's why it works:Your intuition is exactly right. Here's the breakdown:

**Safe to parallelize** — each subdirectory (`github/`, `llm/`, `network/`, `search/`, `image/`) is a self-contained subcommand. Each Claude instance only touches files inside its own directory, so there's zero chance of merge conflicts.

**Watch the shared files** — `main.py`, `__init__.py`, and shared modules like `utils/` or `env.py` are the conflict zone. Two rules:

1. If a Claude instance only *reads* a shared file (importing `env.py` for config, reading from `utils/`), it's safe — reads never conflict.
2. If two instances both *write* to `main.py` (e.g. adding a new CLI entry point), you'll get conflicts. Coordinate those changes manually, or stagger them — finish one instance's work and merge before the next touches shared files.

**Practical workflow:**
- Spin up one Claude Code per subcommand, each pointed at its own subdirectory
- Give each instance context limited to that folder: `claude --context github/`
- Handle `main.py` / routing changes yourself as the integrator, or do them in a separate sequential step after the subcommand work is done

The cleaner your separation of concerns (no cross-imports between `github/` and `llm/`, etc.), the more parallelism you can safely run. Click any node in the diagram to dive deeper.