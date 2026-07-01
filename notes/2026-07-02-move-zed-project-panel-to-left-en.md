---
audio: false
generated: true
image: false
lang: en
layout: post
title: Move Zed project panel to left
translated: false
type: note
---

Question: How do I move the file (project) panel in Zed editor from the right side to the left side?

Answer:

Fastest way — no config editing:

- Command palette (`Cmd+Shift+P`) → run `project panel: toggle focus`, then drag the panel tab to the left dock. Or just drag the project panel's tab strip to the left edge of the window; Zed docks it there automatically and rewrites your `settings.json` for you.

Direct way — edit settings.json:

```bash
# Cmd+, opens settings, or edit the file directly:
vim ~/.config/zed/settings.json
```

Add/edit this key:

```json
{
  "project_panel": {
    "dock": "left"
  }
}
```

Save, and Zed hot-reloads settings immediately — no restart needed.

Notes specific to your setup:

- Default is `"left"` in stock Zed — the default project panel config sets "dock": "left", so if yours is on the right, something (a theme/config you copied, or a manual drag) explicitly set it to `"right"`.
- While you're in there, worth deciding on the rest of your panel layout in one pass, since Zed lets you dock the notification panel, chat panel, outline panel, and project panel independently to left or right, and separately the git panel dock defaults to "left" too, with dock as a settable option alongside button, default_width, status_style, and sort_by_path.
- If you use the Git panel, note it has its own dock key, so by default the Git Panel docks on the left, and you change it via Panels > Git Panel > Git Panel Dock — separate from `project_panel`.

Quick reference config block if you want project panel + git panel both pinned left:

```json
{
  "project_panel": { "dock": "left" },
  "git_panel": { "dock": "left" },
  "outline_panel": { "dock": "right" }
}
```

References:

- [Configuring Zed](https://zedhub.dev/configuring-zed)
- [Zed Git integration docs](https://zed.dev/docs/git)
- [How I configured the Zed editor for daily-driving](https://dev.to/hitblast/how-i-configured-the-zed-editor-for-daily-driving-4k2k)