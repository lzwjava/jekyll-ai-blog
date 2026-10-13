---
audio: false
generated: true
image: false
lang: en
layout: post
title: Personal Rust CLI/TUI Toolbox
translated: false
type: note
---

**`/home/lzw/projects/ll`** is a personal Rust CLI/TUI toolbox — a single binary (`ll`) that dispatches subcommands, plus some side experiments.

## Main binary (Rust, ratatui + crossterm + sysinfo)

`src/main.rs` routes the first argument to subcommands:

| Command | What it does | Module |
| --- | --- | --- |
| `cargo run` (default) | Centered "Hello" in a bordered box TUI (`run_hello`, quit with `q`) | `main.rs` |
| `info` | Live dashboard: CPU brand/cores/usage, memory, disk tables | `main.rs` |
| `gcloud` | Show Google Cloud account & config info | `src/gcloud.rs` |
| `uno` | Arduino UNO serial monitor (uses the `serialport` crate) | `src/uno.rs` |
| `word2vec` | Word2Vec training — Rust port of Mikolov's implementation, multi-threaded with an epoch loop | `src/word2vec.rs` (~39 KB, the biggest file) |

## Side experiments

- `quicksort.py`, `Quicksort.java` — quicksort benchmarks sorting 10,000 numbers, for comparing languages against the Rust version.
- `sketch_jul9a/sketch_jul9a.ino` — Arduino sketch that blinks an LED every 3 seconds (pairs with the `uno` subcommand).

Note: the README is slightly out of date — it only mentions the `info` TUI and the quicksort benchmarks, but the code has since grown `gcloud`, `uno`, and `word2vec` subcommands.
