---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pyright Benefits Outweigh Overhead
translated: false
type: note
---

**Question:** Is Pyright (Microsoft's static type checker) worth the effort? It downloads stubs/sources to check types, has a cache, and takes a few minutes on first init — is that overhead justified?

**Answer:**

Short answer: **Yes, for serious Python codebases, especially AI/ML work — but with caveats.**

---

## What Pyright Actually Does on Init

When Pyright starts cold:

1. **Indexes your environment** — it walks `site-packages` and resolves all installed packages
2. **Loads type stubs** — from `typeshed` (bundled) + any `py.typed` packages + auto-downloaded stubs via `pylance` (VS Code only)
3. **Builds a symbol table** — cross-file dependency graph, all imports resolved
4. **Caches to `.pyright/` or the LSP cache dir** — subsequent runs are fast (seconds, not minutes)

The "downloads source" behavior is mostly a Pylance (VS Code) thing — it fetches stub packages from `pypi` for packages that don't ship their own types. Pyright CLI itself doesn't download — it uses whatever's in your env.

---

## Is the Overhead Worth It?

**For your workflow specifically:**

| Factor | Verdict |
| --- | --- |
| You write Python CLI agents, LLM tooling | ✅ High value — catches wrong arg types in API calls |
| You use LLM SDKs (Anthropic, OpenAI) | ✅ Both ship `py.typed` — Pyright gives you full completions + type errors |
| You vibe-code fast and iterate in REPL | ⚠️ Can slow you down if you over-enforce |
| You train models (numpy, torch) | ⚠️ Torch stubs are incomplete; expect false positives |

---

## The Real Trade-off

**Where Pyright shines:**

```python
# Catches this at edit time, not runtime:
from anthropic import Anthropic
client = Anthropic()
msg = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": "hi"}],
    max_tokens="1000"  # ← Pyright: Argument of type "str" not assignable to "int"
)
```

**Where it wastes time:**

```python
import torch
x: torch.Tensor = torch.zeros(3, 4)
y = x @ x.T  # Pyright sometimes can't infer this cleanly
```

PyTorch stubs (`torch/_C/_VariableFunctions.pyi`) are auto-generated and full of `Any` — Pyright can't help much there.

---

## Practical Setup (minimal friction)

```toml
# pyrightconfig.json
{
  "pythonVersion": "3.11",
  "typeCheckingMode": "basic",   # not "strict" — too noisy for fast iteration
  "reportMissingImports": "warning",
  "reportUnknownVariableType": "none",  # kills torch noise
  "exclude": ["**/__pycache__"]
}
```

Use `basic` mode, not `strict`. Strict mode on an ML codebase will drown you in `Unknown` type errors from numpy/torch.

---

## Alternatives Worth Knowing

| Tool | Speed | Accuracy | Best For |
| --- | --- | --- | --- |
| **Pyright** | Fast (after cache) | Best | Large codebases, SDK usage |
| **mypy** | Slow | Good | Legacy, CI gates |
| **ruff** (type hints) | Instant | Surface only | Linting, not deep type checking |
| **basedpyright** | Same as Pyright | Stricter | If you want more pedantic checks |

`basedpyright` is a community fork of Pyright that's worth knowing — stricter defaults, better error messages.

---

## Verdict for You

Given you're building agent systems and LLM tooling where API contracts matter — **yes, worth it**. The init cost is a one-time tax. After that, it runs in milliseconds as an LSP or in `--watch` mode.

The one place I'd skip it: pure torch training loops. Too many `Any` types from incomplete stubs = noise without signal. For everything else (CLI tools, agent orchestration, API wrappers) it catches real bugs before runtime.
