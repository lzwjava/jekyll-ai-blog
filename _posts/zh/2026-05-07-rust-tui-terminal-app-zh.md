---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rust TUI 在终端内运行
translated: true
type: note
---

问题：Rust TUI 是否总是弹出一个单独的窗口，而不是直接在终端中显示结果？

答案：不是——大多数 Rust TUI 库**不会**创建单独的桌面窗口。

Rust TUI（终端用户界面）通常**在**现有的终端**内部**运行。

例如，像以下这些库：

* [ratatui](https://ratatui.rs/?utm_source=chatgpt.com)
* [crossterm](https://github.com/crossterm-rs/crossterm?utm_source=chatgpt.com)
* [termion](https://github.com/redox-os/termion?utm_source=chatgpt.com)

通常会：

* 将终端切换到“alternate screen buffer”
* 持续重绘屏幕
* 临时隐藏普通 shell 提示符
* 交互式捕捉键盘事件

所以它*看起来*像是“弹出了”一个全屏应用，但实际上仍然在你的终端内部。

示例：

```bash
cargo run
```

然后你的终端会变成类似：

```text
┌────────────────────────────┐
│   System Monitor           │
│ CPU: 32%                   │
│ Memory: 5.2 GB             │
│                            │
│ Press q to quit            │
└────────────────────────────┘
```

当你退出（`q`）时，normal shell 会恢复。

---

你可能是在对比以下情况：

| 类型        | 行为                          |
| ----------- | --------------------------------- |
| CLI 程序    | 打印结果并退出           |
| TUI 程序    | 交互式接管终端 |
| GUI 程序    | 打开实际的 OS 窗口            |

所以：

```rust
println!("Hello");
```

→ 直接输出

而 TUI：

```rust
terminal.draw(|f| {
   // render UI
});
```

→ 交互式终端屏幕

---

有些 TUI 也可以表现得像普通 CLI。

例如：

```bash
git log
htop
btop
lazygit
```

这些都是基于终端的界面，而非单独的窗口。

---

从技术上讲，大多数 Rust TUI 应用使用：

```text
Alternate Screen Buffer
```

通过 ANSI escape sequences 实现。

这意味着：

* 你之前的终端内容被保留
* 应用获得一个干净的临时屏幕
* 退出后，旧屏幕恢复

这就是为什么感觉像是“弹出模式”。

---

如果你想要：

## 1. 仅直接输出

使用普通 CLI：

```rust
println!("result");
```

或像这样的库：

* [clap](https://github.com/clap-rs/clap?utm_source=chatgpt.com)
* [indicatif](https://github.com/console-rs/indicatif?utm_source=chatgpt.com)

---

## 2. 交互式终端 UI

使用 TUI：

* [ratatui](https://ratatui.rs/?utm_source=chatgpt.com)
* [cursive](https://github.com/gyscos/cursive?utm_source=chatgpt.com)

---

## 3. 实际图形窗口

使用 GUI 框架：

* [egui](https://github.com/emilk/egui?utm_source=chatgpt.com)
* [iced](https://github.com/iced-rs/iced?utm_source=chatgpt.com)
* [tauri](https://tauri.app/?utm_source=chatgpt.com)

这些会创建真实的桌面窗口。

参考资料：

* [https://ratatui.rs/](https://ratatui.rs/)
* [https://github.com/crossterm-rs/crossterm](https://github.com/crossterm-rs/crossterm)
* [https://github.com/gyscos/cursive](https://github.com/gyscos/cursive)
* [https://github.com/emilk/egui](https://github.com/emilk/egui)
* [https://tauri.app/](https://tauri.app/)