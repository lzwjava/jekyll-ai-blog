---
audio: false
generated: true
image: false
lang: en
layout: post
title: Moving the Zed Project Panel
translated: false
type: note
---

Here's what the Zed codebase tells us about moving the file explorer (Project Panel) from right to left:

---

## Code Analysis: Project Panel Dock Position

### The mechanism has 3 layers

**1. Settings layer** (`crates/settings_content/src/workspace.rs` line 709)

The `ProjectPanelSettingsContent` struct has:

```rust
/// Default: right (Agentic layout), left (Classic layout)
pub dock: Option<DockSide>,
```

`DockSide` is a simple enum with only `Left` and `Right` (no `Bottom` for project panel).

**2. Panel trait impl** (`crates/project_panel/src/project_panel.rs` line 7257)

```rust
impl Panel for ProjectPanel {
    fn position(&self, _: &Window, cx: &App) -> DockPosition {
        match ProjectPanelSettings::get_global(cx).dock {
            DockSide::Left => DockPosition::Left,
            DockSide::Right => DockPosition::Right,
        }
    }

    fn position_is_valid(&self, position: DockPosition) -> bool {
        matches!(position, DockPosition::Left | DockPosition::Right)
    }

    fn set_position(&mut self, position: DockPosition, _: &mut Window, cx: &mut Context<Self>) {
        settings::update_settings_file(self.fs.clone(), cx, move |settings, _| {
            let dock = match position {
                DockPosition::Left | DockPosition::Bottom => DockSide::Left,
                DockPosition::Right => DockSide::Right,
            };
            settings.project_panel.get_or_insert_default().dock = Some(dock);
        });
    }
}
```

When you change position, it **writes to your settings.json file** persistently.

**3. Layout presets** (`crates/agent_settings/src/agent_settings.rs` lines 40-55)

Two built-in layouts determine defaults:

```rust
const AGENT: Self = Self {
    project_panel_dock: Some(DockSide::Right),  // <-- Agent layout: RIGHT
    // ...
};

const EDITOR: Self = Self {
    project_panel_dock: Some(DockSide::Left),   // <-- Editor layout: LEFT
    // ...
};
```

**4. Right-click context menu** (`crates/workspace/src/dock.rs` line 1262)

Right-clicking a panel button in the status bar builds a context menu with toggleable entries:

- "Dock Left" (checked if current)
- "Dock Right" (checked if current)
- "Dock Bottom" is NOT shown for project panel (position_is_valid rejects it)

Each entry calls `panel.set_position(position, window, cx)` which writes to settings.

**5. Keyboard cycling** (`crates/workspace/src/dock.rs` line 127)

```rust
fn move_to_next_position(&self, window: &mut Window, cx: &mut App) {
    // cycles: Left -> Bottom -> Right -> Left (wraps)
    // filtered by position_is_valid, so for project panel: Left -> Right -> Left
}
```

Triggered by the `MoveFocusedPanelToNextPosition` action when a panel is focused.

---

## How to actually do it (3 ways)

1. **Right-click the panel button** in the status bar → select "Dock Left"

2. **Edit settings.json** (`~/.config/zed/settings.json`):

   ```json
   {
     "project_panel": {
       "dock": "left"
     }
   }
   ```

3. **Switch layout** — if you're on the "Agentic" layout (which defaults project panel to right), switch to "Editor/Classic" layout where left is the default.

Your project panel is likely on the right because you're using the Agentic layout, which puts the AI agent panel on the left and pushes the project panel to the right.
