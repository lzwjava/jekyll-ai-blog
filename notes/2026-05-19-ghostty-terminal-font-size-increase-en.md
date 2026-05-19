---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ghostty Terminal Font Size Increase
translated: false
type: note
---

**Question:** Since I work mostly in the terminal (like using Hermes agent, etc.) and I have myopia, can I simply scale up the font size in Ghostty terminal to see more clearly?

**Answer:**

Yes, absolutely! Scaling up the font size in Ghostty is one of the simplest and most effective ways to help your eyes — especially since, as described in your vision tips blog, you're already managing myopia with undercorrection glasses and working in the terminal most of the time. Larger text means less strain, no prescription needed.

---

## How to Increase Font Size in Ghostty

### Method 1: Keyboard Shortcut (Instant, Runtime)

On **macOS**:
- **Increase font size:** `Cmd` + `+`
- **Decrease font size:** `Cmd` + `-`
- **Reset font size:** `Cmd` + `0`

The out-of-the-box shortcut to increase/decrease font sizes in Ghostty on macOS is `Cmd + +` and `Cmd + -` respectively.

On **Linux**, you can use keybindings like `super+equal` or `super+plus` to increase font size and `super+minus` to decrease it.

---

### Method 2: Config File (Permanent)

Edit the Ghostty config file (open it with `Command + ,` in the app) and set `font-size` to your desired value, for example `font-size=14`.

For better visibility, you might want to go higher — e.g., `font-size=18` or `font-size=20`:

```ini
font-size = 18
font-thicken = true
```

`font-thicken` thickens your terminal font, which can make it easier to read.

After editing, right-click on the terminal window and go to Config → Reload Configuration to apply the change without restarting.

---

### Method 3: Custom Keybindings (for All Tabs/Splits)

You can add explicit keybindings in your config to make font size changes apply across all tabs:

```ini
keybind = all:super+zero=reset_font_size
keybind = all:super+equal=increase_font_size:1
keybind = all:super+plus=increase_font_size:1
keybind = all:super+minus=decrease_font_size:1
```


---

### Method 4: Via CLI

You can also pass font size as a command line option: `--font-size=12` or `--font-family="Fira Code"`.

---

## Why This Works Well for Your Case

Since you spend most of your time in the terminal (Hermes agent, Claude Code, etc.), increasing Ghostty's font size is ideal:

- **No glasses change needed** — just bigger text on screen
- It complements the "just barely clear" undercorrection principle from your blog — you use reduced-prescription glasses, and larger text compensates for the slight blur
- Works perfectly for terminal-heavy workflows (coding, agents, CLI tools)
- You can even set a specific font size via action: `set_font_size:14.5` will set the font size to 14.5 points.

A good starting point is `font-size = 18` or `font-size = 20` and adjust to taste.

---

**References:**

- [Ghostty Config Reference - ghostty.org](https://ghostty.org/docs/config/reference)
- [Ghostty Keybind Action Reference - ghostty.org](https://ghostty.org/docs/config/keybind/reference)
- [My lil' Ghostty terminal config - birchtree.me](https://birchtree.me/blog/my-lil-ghosty-terminal-config-2/)
- [Increasing font size on all tabs - GitHub Discussion](https://github.com/ghostty-org/ghostty/discussions/8149)