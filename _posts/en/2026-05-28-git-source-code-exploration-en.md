---
audio: false
generated: true
image: false
lang: en
layout: post
title: Git Source Code Exploration
translated: false
type: note
---

This is the **Git source code** — the actual distributed version control system written by Linus Torvalds. You're in `/Users/lzwjava/projects/git` which contains the full C source tree of git itself.

Key files you'll find:

- **Core**: `builtin/` (commands), `object-store/`, `refs/`, `diff.c`, `merge.c`
- **xdiff/**: diff/merge algorithms (patience, histogram)
- **Transport**: `remote-curl.c`, `send-pack.c`, `fetch-pack.c` (protocol handling)
- **Pack files**: `pack-objects.c`, `index-pack.c`
- **Refs**: `refs/` directory for ref storage backends

The project is ~600K lines of C, built with Makefile, and uses autoconf for configuration.

What are you exploring here — studying git internals, contributing a patch, or something else?
