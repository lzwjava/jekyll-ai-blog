---
audio: false
generated: true
image: false
lang: en
layout: post
title: Warp vs Ghostty Terminal Workflows
translated: false
type: note
---

**Question:** What do you think of using Warp Terminal as a multi-pane zsh manager (vertical layout, AI agent disabled), and when would Ghostty still be preferred?

**Answer:**

Nice setup — using Warp purely as a tab/pane manager with the AI agent off is a pragmatic middle ground. Here's my honest take:

**Where Warp wins for your workflow:**

- **Vertical tab layout** is genuinely better for multi-session work than tmux split panes when you're jumping between, say, a Claude Code session, a model training monitor, and a build log simultaneously. The visual sidebar gives you named sessions at a glance.
- **Block-based output** is underrated for ML work — you can fold/copy a whole training run's output as one unit. Much cleaner than scrolling raw terminal history.
- Disabling the AI agent is the right call if you're already running Claude Code / your own `zz`/`ww` CLI agents. No point having two AI layers competing.

**Where Ghostty still wins:**

- **Environment purity.** Warp ships its own terminal emulator layer with some custom env vars and protocol handling. This can cause subtle issues — things like `$TERM`, `$COLORTERM`, custom escape codes for tools like `fzf`, `bat`, `delta`, or anything that probes terminal capabilities. If you're running CUDA jobs over SSH or doing raw `ioctl` stuff, the extra layer introduces occasional friction.
- **Latency.** Ghostty is GPU-accelerated with near-zero input latency. Warp adds a small but real overhead from its Electron-ish rendering layer (it's actually Rust + Metal on Mac, but still heavier than Ghostty's pure native approach).
- **SSH remoting.** When SSHing into your Ubuntu workstation at `192.168.1.36` or the AMD Dev Cloud, Warp's block model breaks down — blocks only work in local sessions. Ghostty just passes through cleanly.
- **Font rendering edge cases.** Some CJK characters or Nerd Font glyphs can render slightly off in Warp. Not a dealbreaker but worth noting given you're working in mixed-language environments.

**My actual recommendation for your setup:**

Use Warp for **local macOS sessions** where you want named tabs managing multiple local processes — it's genuinely the best native multi-session UI on macOS right now if you don't want to invest in learning tmux deeply. Keep Ghostty (or even iTerm2 with tmux integration) for anything involving:

1. SSH into remote machines (workstation, AMD cloud)
2. Tools that probe `$TERM` carefully
3. Situations where you need raw terminal transparency

Essentially: Warp as the **session manager UI**, Ghostty as the **protocol-clean workhorse** for remote/sensitive environments. That's not a regression — that's just using the right tool per context, which is exactly what you already figured out.

The note you published is a good reference. The vertical layout + disabled agent config is the correct minimal Warp setup for a developer who already has their own AI toolchain.
