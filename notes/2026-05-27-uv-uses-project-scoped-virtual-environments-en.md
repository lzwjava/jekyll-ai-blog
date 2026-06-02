---
audio: false
generated: true
image: false
lang: en
layout: post
title: uv Uses Project-Scoped Virtual Environments
translated: false
type: note
---

Yes — uv is **project-scoped**, not global. Here's how it works:

```
~/projects/ww/          → has its own .venv/
~/projects/uv/          → has its own .venv/
```

When you run `uv sync` or `uv pip install -e .` inside a project, uv creates/uses a `.venv/` **in that project directory**. Everything goes there. Nothing touches your global Python.

**Your situation with ww:**

```bash
cd ~/projects/ww
pip install -e .        # installed into some venv (or globally — which one?)
```

The question is: which Python/environment did that `pip install -e .` target?

- If you ran it without activating a venv → it went into system Python (bad, global pollution)
- If you had a venv active → it went there

**What uv changes:**

```bash
cd ~/projects/uv
uv sync                 # creates .venv/ here, installs deps from uv.lock into it
```

This `.venv/` is completely isolated. Different projects can have different versions of the same library. No conflicts.

**The mental model:**

| Tool | Scope | Where deps live |
|------|-------|-----------------|
| `pip install` (no venv) | Global | system site-packages |
| `pip install` (in venv) | Project | `.venv/` |
| `uv sync` | Project (always) | `.venv/` (auto-created) |
| `uv pip install -e .` | Project | `.venv/` |

uv is stricter — it **always** uses a virtualenv. If none exists, it creates one. No accidental global installs.

**For your ww project**, you can migrate:

```bash
cd ~/projects/ww
uv sync    # reads pyproject.toml, creates .venv, installs everything
```

Then you don't need the old `pip install -e .` anymore. The `.venv/` is gitignored by default (uv adds it to `.gitignore` automatically).
