---
audio: false
generated: true
image: false
lang: en
layout: post
title: Git Project Structure and Architecture
translated: false
type: note
---

Here's a comprehensive summary of the Git project:

---

## Git — Distributed Version Control System

**Version**: 2.54.0.265.g56a4f3c3 (latest development)
**Language**: C (with some Perl, Tcl/Tk, and shell)
**License**: GPLv2

---

### Source Stats

- **629 C source files**, 342 headers
- **~385,000 lines** of C code
- **130 builtin commands** (add, commit, push, pull, merge, rebase, etc.)
- **1,094 test scripts** in `t/`
- **252 documentation files** (AsciiDoc)

---

### Directory Structure & Subsystems

| Directory | Purpose |
|-----------|---------|
| `builtin/` | 130 command implementations (add.c, commit.c, merge.c, rebase.c...) |
| `refs/` | Reference storage backends: files, packed, reftable |
| `reftable/` | New binary ref storage format (faster, more compact than packed-refs) |
| `odb/` | Object database layer (loose objects, pack files, streaming) |
| `xdiff/` | Diff/merge algorithms: patience diff, histogram diff, 3-way merge |
| `negotiator/` | Fetch negotiation strategies: default, skipping, noop |
| `sha256/`, `sha1/`, `sha1dc/` | Hash implementations (SHA-1 with collision detection, SHA-256) |
| `block-sha1/` | Optimized block SHA-1 |
| `trace2/` | Structured tracing/telemetry (JSON, perf, normal targets) |
| `compat/` | Platform compatibility shims |
| `contrib/` | Community tools: subtree, diff-highlight, credential helpers, libgit-rs |
| `t/` | Test suite (shell-based, runs with `make test`) |
| `Documentation/` | AsciiDoc man pages and guides |
| `perl/`, `git-gui/`, `gitk-git/` | Perl bindings, GUI tools |

---

### Key Source Files (top-level)

| File | What it does |
|------|--------------|
| `commit.c` | Commit object creation and parsing |
| `merge.c`, `merge-ort.c` | Merge engine (ORT = Ostensibly Recursive's Twin, the modern 3-way merge) |
| `diff.c`, `diffcore-*.c` | Diff pipeline: break, rename detection, pickaxe, ordering |
| `sequencer.c` | Rebase/cherry-pick state machine |
| `rerere.c` | Reuse recorded resolution (remembers merge conflict resolutions) |
| `pack-objects.c`, `packfile.c` | Pack file creation, reading, bitmaps |
| `commit-graph.c`, `midx.c` | Performance accelerators: commit graph, multi-pack index |
| `transport.c`, `connect.c` | Git protocol v2 transport layer |
| `fetch-pack.c`, `send-pack.c` | Client-side fetch/push |
| `remote-curl.c` | HTTP(S) smart transport |
| `config.c` | Config file parsing (gitconfig) |
| `hash-ll.c` | Hash abstraction (SHA-1 ↔ SHA-256) |
| `worktree.c` | Linked worktree management |
| `credential.c` | Credential helper framework |

---

### Architecture Highlights

1. **Object Model**: Everything is an object (blob, tree, commit, tag) addressed by SHA-1 or SHA-256 hash. Objects are stored loose or in pack files.

2. **Diff Pipeline**: Modular pipeline with stages: `diffcore-break` → `diffcore-rename` → `diffcore-pickaxe` → `diffcore-order`. xdiff library does the actual line-level diffing.

3. **Merge Engine (ORT)**: Replaced the old recursive merge in 2021. Handles renames, directory detection, and conflict resolution in a single pass.

4. **Refs Backends**: Pluggable — `files-backend.c` (traditional), `packed-backend.c`, and the new `reftable-backend.c` (Google-contributed binary format).

5. **Negotiation**: During fetch, the client and server negotiate which objects are needed. Three strategies: default (consecutive), skipping (skip ancestors), noop.

6. **Protocol v2**: `serve.c` implements the modern wire protocol with capabilities, ref filtering, and ls-refs.

7. **Build System**: GNU Make with autoconf optional. Supports `make prefix=/usr/local`, `NO_*` flags to disable features, and `DEVELOPER=1` for strict warnings.

---

### Testing

```
make test              # run full suite (~1094 scripts)
make test T=t1234.sh   # run single test
GIT_TEST_OPTS=-v make test  # verbose
```

---

### Contrib/Notable

- `contrib/subtree/` — git subtree merge strategy
- `contrib/diff-highlight/` — word-level diff highlighting
- `contrib/credential/` — credential helpers (store, cache, netrc)
- `contrib/libgit-rs/`, `contrib/libgit-sys/` — Rust bindings (new)

---

This is one of the most battle-tested C codebases in existence — ~20 years of development, used by virtually every software team on the planet.