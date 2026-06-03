---
audio: false
generated: true
image: false
lang: en
layout: post
title: Uv sync workflow
translated: false
type: note
---

Question: What does `uv sync` do?

Answer:

`uv sync` keeps your virtual environment aligned with your project's dependencies by reading your pyproject.toml or uv.lock and making three decisions: installs missing packages, upgrades/downgrades existing packages to match specified versions.

It's the **sync phase** of uv's two-phase dependency workflow:

1. **Lock** (`uv lock`): Resolves `pyproject.toml` → generates deterministic `uv.lock` with pinned versions
2. **Sync** (`uv sync`): Installs/updates packages from `uv.lock` into `.venv`

The key insight: syncing is the process of installing required packages from the lockfile into the project's development environment, and both locking and syncing are automatically handled by uv—for example, when you execute `uv run`, the project is locked and synced before the command is invoked.

**Practical usage:**

```bash
# Explicit sync (manual environment setup)
$ uv sync
$ source .venv/bin/activate
$ python script.py

# Implicit sync (recommended - faster feedback loop)
$ uv run python script.py  # auto-syncs before running

# With options
$ uv sync --frozen --dev  # fail if lock is stale; include dev deps
$ uv sync --no-dev        # exclude development dependencies
$ uv sync --refresh       # revalidate all deps (bust cache)
```

**Why this matters for your workflow:**

Because uv is extremely fast (especially with a hot cache), `uv sync` is basically instant, which means you can sync your environment every time you run a Python command. This eliminates manual venv management friction.

In practice: replace `python` with `uv run` everywhere. You never activate `.venv` manually, never worry about stale packages, never think about environment sync again—uv handles it transparently.

**Key flags for CI/prod:**

- `--frozen`: Fail if `uv.lock` doesn't match `pyproject.toml` (reproducible builds)
- `--no-sync`: Skip sync (useful if you just want to lock without installing)
- `--compile-bytecode`: Pre-compile `.py` to `.pyc` (saves import time on cold starts)

References:

- [uv Locking and Syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv Working on Projects](https://docs.astral.sh/uv/guides/projects/)
