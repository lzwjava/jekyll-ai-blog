---
audio: false
generated: true
image: false
lang: en
layout: post
title: Missing Build System Broke Entry Point
translated: false
type: note
---

## Summary

### What happened

You renamed the project from `timesheet` to `tt` (both the directory and `pyproject.toml` `name` field). After that, `uv run tt` failed with:

```
error: Failed to spawn: `tt`
  Caused by: No such file or directory (os error 2)
```

### Root cause

The `pyproject.toml` was missing a `[build-system]` declaration. When `uv sync` runs without one, it emits this warning (which was easy to miss):

```
warning: Skipping installation of entry points (`project.scripts`) for package `tt`
because this project is not packaged; to install entry points, set `tool.uv.package = true`
or define a `build-system`
```

Without a build system, `uv` installs the dependencies but **never registers the CLI entry point** (`tt = "tt.cli:main"`). So the `tt` command simply doesn't exist in the venv's `bin/`, and the shell can't find it.

### What was changed

**`pyproject.toml`** — two edits:

1. Added a build system (hatchling):
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

2. Replaced the old setuptools package discovery with hatch's equivalent:
```toml
# Before (setuptools — inert without setuptools as build-backend)
[tool.setuptools.packages.find]
include = ["tt*"]
exclude = ["data*", "input*"]

# After (hatchling)
[tool.hatch.build.targets.wheel]
packages = ["tt"]
```

Then `uv sync` rebuilt the package and registered the entry point.

### Why it probably worked before

The old project at `/Users/lzwjava/projects/timesheet` likely had a cached venv from a time when `uv sync` or `uv pip install -e .` was run with the package in installable mode, or `tool.uv.package = true` was set. When you renamed/moved the project, `uv sync` re-resolved from scratch and hit the missing build-system gap.

### Options if you ever need them

Instead of adding `[build-system]`, you could also have added this to `pyproject.toml`:

```toml
[tool.uv]
package = true
```

This tells `uv` to treat the project as a package and install entry points even without a formal build backend. But using `hatchling` is the more standard approach.
