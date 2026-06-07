---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Unreadable Yellow Text
translated: false
type: note
---

**Question:** When using Hermes in Warp terminal with light mode enabled, the yellow text output is hard to read. How do I fix this?

**Answer:**

Three approaches, in order of preference:

### 1. **Disable Hermes color output** (quickest)

Hermes likely respects the `NO_COLOR` environment variable or has a flag to disable ANSI colors:

```bash
NO_COLOR=1 hermes run

# Or check hermes help for color flags
hermes run --help | grep -i color
```

If it has a config file (typically `~/.config/hermes/config.json` or `~/.hermesrc`), add:

```json
{
  "colors": false,
  "no_color": true
}
```

### 2. **Override Warp's light mode color scheme**

Warp → Settings → Theme → switch to a dark theme specifically for terminal work, or create a custom theme where yellow has higher contrast (lighter/more saturated yellow).

Alternatively, check if Hermes respects `TERM_PROGRAM_VERSION` or environment color overrides:

```bash
# Force 256-color mode or truecolor
export TERM=xterm-256color
hermes run
```

### 3. **Modify Hermes source if open-source**

If Hermes is in your shell dotfiles or a local script, grep for the yellow color code (likely `\033[33m` or `\033[93m`) and replace it:

```bash
# Find the color definition
grep -r "33m\|93m" ~/.config/hermes/

# Replace with a darker/more visible color (e.g., dark gray, cyan)
sed -i 's/\\033\\[33m/\\033[36m/g' <file>  # yellow → cyan
```

**Which machine?** This is a MacBook Air M2 daily driver issue. Quick fix: toggle `NO_COLOR=1` in your shell alias for Hermes, or switch Warp to dark mode for terminal work.

**Quick test:**

```bash
NO_COLOR=1 hermes run
# If that works, add to ~/.zshrc or ~/.bashrc:
alias hermes='NO_COLOR=1 hermes'
```

What does `hermes --help` show for color/output options?
