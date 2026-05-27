---
audio: false
generated: true
image: false
lang: en
layout: post
title: "uv: Python's Fast Package Manager"
translated: false
type: note
---

Here's the breakdown:

---

This is **uv** — Astral's ultra-fast Python package manager written in Rust. Version 0.11.16. It's one of the most important Rust projects in the Python ecosystem right now.

## What it is

A single binary that replaces pip, pip-tools, pipx, poetry, pyenv, twine, and virtualenv. 10-100x faster than pip. Same team that built Ruff (the Python linter) and ty (the type checker).

## Architecture — 72 crates in a Cargo workspace

The codebase is a monorepo with ~72 crates under `crates/`. Here's the key breakdown by layer:

### CLI & Command Dispatch
- `uv-cli` — Clap-derived CLI definitions (the `Commands` enum with all subcommands)
- `uv` (the main crate) — `lib.rs` has a massive `match *cli.command { ... }` dispatch at line 542, routing to command handlers in `commands/`

### Commands (what uv can do)
From the `commands/` directory:
- **pip/** — compile, install, sync, uninstall, freeze, list, show, tree (pip-compatible interface)
- **project/** — init, add, remove, lock, sync, run, tree, export, version, audit
- **tool/** — run, install, uninstall, list, upgrade
- **python/** — install, uninstall, list, find, pin
- **workspace/** — list, dir, metadata
- **publish** — publish packages to PyPI
- **venv** — virtual environment creation
- **self_update** — self-update mechanism

### The Resolver (the hard part)
- `uv-resolver` — The core dependency resolver, ~4268 lines in `resolver/mod.rs` alone
- Uses **PubGrub** (specifically `astral-pubgrub`, their fork) — a SAT-solving-based version resolution algorithm
- Has sophisticated fork support (forking on markers like `sys_platform == 'win32'` vs Python version constraints)
- Key structs: `Resolver<Provider, InstalledPackages>`, `ResolverState`, `InMemoryIndex`, `CandidateSelector`
- Handles: version maps, yanks, pre-releases, constraints, overrides, flat indexes

### Distribution & Packages
- `uv-distribution` — fetching/caching distribution metadata
- `uv-distribution-types` — type definitions for `Dist`, `BuiltDist`, `SourceDist`, `InstalledDist`
- `uv-distribution-filename` — wheel/sdist filename parsing
- `uv-install-wheel` — wheel installation (unpacking into site-packages)
- `uv-installer` — orchestrates installation with progress reporting

### PEP Standards
- `uv-pep440` — PEP 440 version parsing (with `rkyv` zero-copy deserialization for speed)
- `uv-pep508` — PEP 508 dependency specifiers (`requests>=2.0; python_version>="3.8"`)
- `uv-pypi-types` — PyPI API types

### Infrastructure
- `uv-cache` / `uv-cache-info` / `uv-cache-key` — global content-addressed cache (deduplication)
- `uv-client` — HTTP client for PyPI index (reqwest-based, with retry middleware)
- `uv-python` — Python version discovery/management (pyenv replacement)
- `uv-virtualenv` — virtualenv creation
- `uv-git` / `uv-git-types` — git dependency support
- `uv-build-backend` / `uv-build-frontend` — PEP 517 build system
- `uv-configuration` / `uv-settings` — layered config (CLI > env > pyproject.toml > uv.toml > user > system)
- `uv-workspace` — Cargo-style workspace discovery

### Performance
- `uv-performance-memory-allocator` — custom allocator for speed
- `uv-small-str` — small string optimization
- `uv-once-map` — concurrent init-once map
- Uses `rkyv` for zero-copy deserialization of version data
- Uses `dashmap` for concurrent hash maps
- Uses `tokio` throughout for async I/O
- Uses `rayon` for CPU parallelism

### Notable Design Choices
1. **PubGrub solver** — not a traditional backtracking resolver. It's a conflict-driven algorithm (similar to SAT solvers) that's been proven correct in Coq. Astral maintains their own fork (`astral-pubgrub`).
2. **Forking resolution** — the resolver can "fork" when it encounters environment markers, resolving different versions for different platforms/Python versions in a single pass.
3. **Universal lockfile** — `uv.lock` is platform-independent, capturing all possible forks in one file.
4. **Content-addressed cache** — wheels and metadata are cached by content hash, so the same package version only downloads once across all projects.
5. **Batch prefetching** — `batch_prefetch.rs` proactively fetches metadata for likely-needed packages in parallel during resolution.

This is a seriously engineered Rust project — the kind of codebase where every crate has a clear single responsibility, and the performance wins come from careful architecture (zero-copy deserialization, async I/O, parallel resolution) rather than micro-optimizations.