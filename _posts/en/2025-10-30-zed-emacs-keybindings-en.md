---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Configuring Zed with Emacs Keybindings
translated: false
type: note
---

### Configuring Zed Editor with Emacs Keybindings

It looks like you might mean **Zed** (the high-performance code editor), as "Zig editor" doesn't refer to a standard tool—Zig is a programming language without a built-in editor. If that's not what you intended, feel free to clarify! Assuming Zed, it has built-in support for Emacs keybindings (labeled "Emacs (Beta)"). This covers many basics out of the box, like movement (`Ctrl-b/f/n/p`) and editing (`Ctrl-d` for delete char, `Ctrl-k` for cut to end of line). You can enable it easily, then customize further if needed.

#### Step 1: Enable the Built-in Emacs Keymap

Zed's Emacs mode is predefined and doesn't require manual binding setup for basics. Here's how to switch to it:

1. Open Zed's settings:
   - macOS: `Cmd-,`
   - Windows/Linux: `Ctrl-,`

2. In the settings UI, search for "base keymap" and set it to **Emacs**.

   *Or, edit directly in `settings.json`* (open via `Cmd-Alt-,` on macOS or `Ctrl-Alt-,` on Windows/Linux):

   ```json
   {
     "base_keymap": "Emacs"
   }
   ```

   Save and reload Zed (`Cmd-R` or `Ctrl-R`). That's it—the beta Emacs keymap activates immediately.

   Alternatively, use the command palette (`Cmd-Shift-P` or `Ctrl-Shift-P`), type "toggle base keymap," and select Emacs.

This gives you core Emacs muscle memory without extra work. For a full list of built-in bindings, check Zed's default keymap files in the source (e.g., via GitHub), but basics include:

- **Movement**: `Ctrl-b` (left char), `Ctrl-f` (right char), `Ctrl-p` (up line), `Ctrl-n` (down line), `Alt-b/f` (previous/next word).
- **Editing**: `Ctrl-d` (delete char), `Ctrl-k` (cut to end of line), `Ctrl-y` (yank/paste), `Ctrl-@` (set mark for region), `Ctrl-w` (cut region).
- **Other**: `Ctrl-x Ctrl-s` (save), `Ctrl-g` (cancel), `Ctrl-/` (undo).

#### Step 2: Add or Customize Basic Bindings (If Needed)

For tweaks or more Emacs-like behavior (e.g., better home/end or paragraph nav), edit `keymap.json`:

- Open it via command palette: Type "open keymap file."
- Path: `~/.config/zed/keymap.json` (macOS/Linux) or `~\AppData\Roaming\Zed\keymap.json` (Windows).

Add bindings as a JSON array under contexts like "Editor." Here's a **minimal example** for basic movement and editing (paste into the array; it's based on community configs for compatibility):

```json
[
  {
    "context": "Editor",
    "bindings": {
      // Basic movement
      "ctrl-a": "editor::MoveToBeginningOfLine",
      "ctrl-e": "editor::MoveToEndOfLine",
      "ctrl-b": "editor::MoveLeft",
      "ctrl-f": "editor::MoveRight",
      "ctrl-p": "editor::MoveLineUp",
      "ctrl-n": "editor::MoveLineDown",
      "alt-b": "editor::MoveToPreviousWordStart",
      "alt-f": "editor::MoveToNextWordEnd",

      // Basic editing
      "ctrl-d": "editor::DeleteRight",
      "ctrl-k": "editor::CutToEndOfLine",
      "ctrl-y": "editor::Paste",
      "ctrl-w": "editor::Cut",
      "ctrl-@": ["editor::SetSelectionAnchor", { "selection_id": 0 }],  // Set mark
      "ctrl-x ctrl-x": "editor::FlipSelectionAnchor",  // Exchange point/mark

      // Navigation extras
      "ctrl-home": "editor::MoveToBeginning",
      "ctrl-end": "editor::MoveToEnd",
      "ctrl-g": "editor::Cancel"
    }
  }
]
```

- Save and reload Zed. These override or add to the base Emacs map.
- Test in an editor buffer. For selections, use `Ctrl-Space` (or `Ctrl-@`) to set the mark, then move to select a region.
- Pro tip: Combine with `vim_mode: false` in settings.json to avoid conflicts.

#### Tips

- **Beta status**: Emacs mode is improving (track progress [here](https://github.com/zed-industries/zed/issues/4856)). Report issues on Zed's GitHub.
- **Full custom setups**: For advanced (e.g., pane switching with `Ctrl-x o`), see community examples in the discussion below.
- If you want Vim/Helix modes alongside, set `vim_mode: true` or `helix_mode: true` in settings—they layer on top.

This should get you 80% of basic Emacs feel. Start with the built-in, then iterate!

[Key Bindings Docs](https://zed.dev/docs/key-bindings)
[Configuring Zed](https://zed.dev/docs/configuring-zed)
[Emacs Keymap Discussion](https://github.com/zed-industries/zed/discussions/6572)
[Emacs Compatibility Issue](https://github.com/zed-industries/zed/issues/4856)
