---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 按q或Ctrl+C退出TUI
translated: true
type: note
---

是的——已完成。编辑了 `src/main.rs`：

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

为什么需要这个改动：TUI 运行在 raw mode 下，因此 terminal 不再在 Ctrl+C 时发送 SIGINT——app 必须自己拦截按键。由于 `quit_on_key()` 被 `run_info()`（以及 `run_hello()`）共享，现在两个 TUI 界面都可以通过 **`q`** 或 **`Ctrl+C`** 退出，并且 terminal 会通过 `restore_terminal()` 正确恢复。

`cargo check` 通过（8 个 warnings 是 `word2vec.rs` 中已有的 dead code，与本次改动无关）。
