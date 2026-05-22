---
audio: false
generated: true
image: false
lang: en
layout: post
title: Configure Zed to Open Projects in New Windows
translated: false
type: note
---

**Question:** How to make Zed Editor always open each project in its own window (one project = one window) permanently, without being asked?

**Answer:**

Add this to your `~/.config/zed/settings.json`:

```json
{
  "cli_default_open_behavior": "new_window"
}
```

That's it. This setting controls CLI and double-click behavior. Setting it to `"new_window"` makes Zed always open folders in a new window instead of the current window's threads sidebar.

Open your settings directly from the terminal:

```sh
zed ~/.config/zed/settings.json
```

Or via command palette: `Cmd+Shift+P` → `zed: open settings`.

**Caveats to know:**

`cli_default_open_behavior` only affects CLI (`zed ~/project`) and double-click behavior — it does **not** affect `File > Open` from the menu, which always opens in the current window's threads sidebar.

So for `File > Open`, you'll still need to use `Cmd+Enter` (instead of Enter) in Open Recent to force a new window. There's currently no setting to make `File > Open` always spawn a new window — that's a Zed limitation.

**Quick reference for manual overrides:**

| Want | Do |
|---|---|
| New window always (CLI/drag) | `"cli_default_open_behavior": "new_window"` in settings |
| New window from Open Recent | `Cmd+Enter` or `Cmd+click` |
| New window from CLI one-off | `zed -n ~/myproject` |

References:

- [Windows & Projects — Zed Docs](https://zed.dev/docs/windows-and-projects)