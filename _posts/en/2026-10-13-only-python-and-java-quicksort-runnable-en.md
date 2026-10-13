---
audio: false
generated: true
image: false
lang: en
layout: post
title: Only Python and Java Quicksort Runnable
translated: false
type: note
---

Right now, only the Python and Java versions are runnable — there's **no quicksort in `src/`**, so nothing to invoke via `cargo run` (the README claims otherwise, but it's stale).

## Working commands today

**Python:**

```bash
cd /home/lzw/projects/ll
python3 quicksort.py
```

Output looks like:

```
Before: [...] 
After:  [...] 
Sorted 10000 numbers in X.XXX ms
```

**Java:**

```bash
javac Quicksort.java
java Quicksort
```

(Only needs `javac`/`java` on PATH; no build tooling.)

**Rust:** not available — there's no `bench`/`quicksort` subcommand wired into `main.rs`.

## Want a Rust subcommand?

I can add one so all three run the same benchmark:

```bash
cargo run --release -- bench   # Rust quicksort on 10,000 ints
```

Implementation would be: a `bench` arm in `main.rs`'s `match`, a `quicksort` module with the same Lomuto partition and 10,000-element input, timed with `std::time::Instant` — making the three-way comparison actually apples-to-apples (and I'd fix the README section to match). Say the word and I'll add it.
