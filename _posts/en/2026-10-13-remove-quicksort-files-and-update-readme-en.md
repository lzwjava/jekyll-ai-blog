---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remove quicksort files and update README
translated: false
type: note
---

Done.

**Removed:**
- `Quicksort.java`
- `quicksort.py`

**Also updated** `README.md` — dropped the "quicksort benchmarks" intro sentence and the whole "Quick Sort Benchmarks" section, since it pointed at files that no longer exist.

Current working tree state:

```
 D Quicksort.java
 D quicksort.py
 M README.md
 M src/main.rs        (the Ctrl+C exit change from earlier)
```

Nothing is committed yet — let me know if you'd like me to commit these (e.g. `chore: remove quicksort benchmarks and update README`, plus a separate commit for the Ctrl+C fix), or if `cargo run -- bench` (a Rust quicksort) should be added since the Rust one never existed in `src/`.