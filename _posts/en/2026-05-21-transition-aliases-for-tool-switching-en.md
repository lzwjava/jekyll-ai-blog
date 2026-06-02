---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transition Aliases for Tool Switching
translated: false
type: note
---

**Question:** You added `alias code=zed` to your zprofile as a lightweight substitute for VS Code — is that a good move? And generally, when changing habits on a computer, is having a transition period (like aliasing old commands to new tools) a smart strategy?

**Answer:**

Yes, both ideas are solid.

**`alias code=zed` — practical and clean**

Zed is genuinely lighter than VS Code. It's written in Rust, GPU-accelerated via GPUI, and has almost no Electron overhead. For your MacBook Air M2 with 54 GB free and likely memory pressure from LLM workloads, this matters. The alias lets your muscle memory (`code .`) keep working while the underlying tool is now faster.

You can go further in your `.zprofile`:

```zsh
alias code=zed
alias c=zed          # even shorter
alias zz="zed ."     # open cwd instantly
```

Or if you ever want fallback logic:

```zsh
code() {
  if command -v zed &>/dev/null; then
    zed "$@"
  else
    /usr/local/bin/code "$@"  # real VS Code as fallback
  fi
}
```

**Transition period aliasing — yes, this is a real pattern**

It's essentially a shim strategy. You used it to redirect behavior at the command layer while your habits catch up. Same principle as:

- `alias python=python3` during the Python 2→3 migration era
- `alias vim=nvim` when switching editors
- `alias grep='rg'` when moving to ripgrep
- Kernel `compat` layers, macOS Rosetta, `update-alternatives` on Linux

The key insight: **habits live in motor memory, not in your conscious mind**. The alias intercepts at the execution layer so you don't have to fight your fingers while your brain retrains. After a few weeks you can drop the alias and just type `zed` directly — the alias has done its job.

This is also why you keep the same keybindings when switching editors, or why Zed supports VS Code keymaps out of the box. Reducing the delta between old and new habit lowers the activation energy to switch.

Smart move overall.
