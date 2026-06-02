---
audio: false
generated: true
image: false
lang: en
layout: post
title: Top Rust Open-Source Tools
translated: false
type: note
---

**Question:** What are some good Rust open-source tools/software worth knowing, similar to Zed and Warp?

**Answer:**

Here's a curated list organized by category — all production-quality, actively maintained Rust projects:

---

## Terminals & Shells

| Project | What it is |
|---------|-----------|
| [Warp](https://github.com/warpdotdev/Warp) | AI-native terminal (you mentioned it) |
| [Alacritty](https://github.com/alacritty/alacritty) | GPU-accelerated terminal, minimal, blazing fast |
| [WezTerm](https://github.com/wez/wezterm) | GPU-accelerated terminal + multiplexer, Lua-configurable |
| [Zellij](https://github.com/zellij-org/zellij) | Terminal multiplexer (tmux alternative), plugin system |

---

## Editors & IDEs

| Project | What it is |
|---------|-----------|
| [Zed](https://github.com/zed-industries/zed) | Fast collaborative editor (you mentioned it) |
| [Helix](https://github.com/helix-editor/helix) | Modal editor, tree-sitter + LSP built-in, no plugins needed |

---

## CLI Replacements (the "modern Unix tools" tier)

| Project | Replaces | Notes |
|---------|----------|-------|
| [ripgrep (rg)](https://github.com/BurntSushi/ripgrep) | `grep` | Fastest grep, respects `.gitignore` |
| [fd](https://github.com/sharkdp/fd) | `find` | Simpler syntax, fast |
| [bat](https://github.com/sharkdp/bat) | `cat` | Syntax highlighting, git integration |
| [eza](https://github.com/eza-community/eza) | `ls` | Colors, icons, tree view |
| [zoxide](https://github.com/ajeetdsouza/zoxide) | `cd` | Smarter directory jumping |
| [dust](https://github.com/bootandy/dust) | `du` | Visual disk usage |
| [procs](https://github.com/dalance/procs) | `ps` | Better process viewer |
| [bottom (btm)](https://github.com/ClementTsang/bottom) | `htop` | Full TUI system monitor |
| [sd](https://github.com/chmln/sd) | `sed` | Sane substitution syntax |
| [hyperfine](https://github.com/sharkdp/hyperfine) | manual timing | Benchmarking CLI tool |

---

## Build, Package & Dev Tooling

| Project | What it is |
|---------|-----------|
| [just](https://github.com/casey/just) | `make` alternative, saner syntax — great for project scripts |
| [cargo-watch](https://github.com/watchexec/watchexec) | Re-runs cargo on file changes |
| [mise](https://github.com/jdx/mise) | `asdf`/`nvm`/`pyenv` all-in-one version manager |
| [pixi](https://github.com/prefix-dev/pixi) | Conda-compatible package manager, fast |
| [uv](https://github.com/astral-sh/uv) | Python package manager — `pip` + `venv` replacement, 100x faster |
| [ruff](https://github.com/astral-sh/ruff) | Python linter + formatter, replaces flake8/black/isort |

---

## Networking & HTTP

| Project | What it is |
|---------|-----------|
| [xh](https://github.com/ducaale/xh) | `httpie` clone but fast — best curl alternative for humans |
| [dog](https://github.com/ogham/dog) | DNS lookup tool, `dig` replacement |
| [bandwhich](https://github.com/imsnif/bandwhich) | Terminal bandwidth monitor by process |
| [miniserve](https://github.com/svenstaro/miniserve) | Instant HTTP file server, one binary |

---

## Data & Search

| Project | What it is |
|---------|-----------|
| [Meilisearch](https://github.com/meilisearch/meilisearch) | Full-text search engine, Elasticsearch alternative |
| [Tantivy](https://github.com/quickwit-oss/tantivy) | Lucene-equivalent search library in Rust |
| [Quickwit](https://github.com/quickwit-oss/quickwit) | Distributed search engine for logs/traces |
| [Lancedb](https://github.com/lancedb/lancedb) | Embedded vector DB (relevant for your AI work) |

---

## AI / LLM Adjacent

| Project | What it is |
|---------|-----------|
| [Candle](https://github.com/huggingface/candle) | HuggingFace's ML framework in Rust — run LLMs without Python |
| [llm](https://github.com/rustformers/llm) | Run GGML models locally from CLI |
| [Ratchet](https://github.com/FL33TW00D/ratchet) | WebGPU ML inference in Rust |

---

## My Top Picks for You Specifically

Given your AI engineering trajectory and CLI-first workflow:

1. **`uv` + `ruff`** — you're probably already on these, but if not, immediate wins for Python workflow
2. **`mise`** — single tool to replace pyenv/nvm/rbenv
3. **`just`** — replace your Makefiles, works great for agent/CLI project scripts
4. **Candle** — worth studying the source; HF's bet on Rust for inference, directly relevant to your model training work
5. **Tantivy / Quickwit** — if you ever build RAG pipelines with custom retrieval
6. **Helix** — if you want a modal editor that's LSP-native from day one without vimrc archaeology
