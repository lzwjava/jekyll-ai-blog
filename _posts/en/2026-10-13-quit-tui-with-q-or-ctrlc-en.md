---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quit TUI with q or Ctrl+C
translated: false
type: note
---

Yes — done. Edited `src/main.rs`:

```rust
use crossterm::{
    event::{self, Event, KeyCode, KeyModifiers},
    ...
}

fn quit_on_key() -> io::Result<bool> {
    if let Event::Key(key) = event::read()? {
        // Quit on 'q' or Ctrl+C (raw mode disables the default SIGINT).
        if key.code == KeyCode::Char('q')
            || (key.code == KeyCode::Char('c') && key.modifiers.contains(KeyModifiers::CONTROL))
        {
            return Ok(true);
        }
    }
    Ok(false)
}
```

Why it's needed: the TUI runs in raw mode, so the terminal no longer delivers SIGINT on Ctrl+C — the app has to intercept the key itself. Since `quit_on_key()` is shared by `run_info()` (and `run_hello()`), both TUI screens now exit on either **`q`** or **`Ctrl+C`**, and the terminal is restored properly via `restore_terminal()`.

`cargo check` passes (the 8 warnings are pre-existing dead code in `word2vec.rs`, unrelated to this change).
