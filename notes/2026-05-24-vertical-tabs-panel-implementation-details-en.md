---
audio: false
generated: true
image: false
lang: en
layout: post
title: Vertical Tabs Panel Implementation Details
translated: false
type: note
---

Here's how Warp's vertical layout works, based on the source code at `/Users/lzwjava/projects/warp`:

**Vertical Tabs Panel - Architecture**

The vertical tabs feature replaces the traditional horizontal tab bar with a sidebar panel. It's gated behind both a feature flag and a user setting:

```rust
// tab.rs line 61
pub fn uses_vertical_tabs(ctx: &AppContext) -> bool {
    FeatureFlag::VerticalTabs.is_enabled() && *TabSettings::as_ref(ctx).use_vertical_tabs
}
```

**Settings (tab_settings.rs)**

The TOML config path is `appearance.vertical_tabs.*`:

| Setting | Default | Options |
|---------|---------|---------|
| `enabled` | false | bool |
| `view_mode` | Compact | Compact, Expanded |
| `display_granularity` | Panes | Panes, Tabs |
| `tab_item_mode` | FocusedSession | FocusedSession, Summary |
| `primary_info` | Command | Command, WorkingDirectory, Branch |
| `compact_subtitle` | Branch | Branch, WorkingDirectory, Command |
| `show_pr_link` | true | bool |
| `show_diff_stats` | true | bool |
| `show_details_on_hover` | true | bool |

**How It Renders (vertical_tabs.rs)**

The panel is rendered as a resizable sidebar (line 1485-1541):

1. A `ClippedScrollable` column contains the tab groups
2. Above it sits a `render_control_bar` with search input
3. The whole thing is wrapped in a `Resizable` with a drag bar (left or right side depending on config)
4. Width constraints: min 200px, default 248px, max 50% of window width

The panel position (left vs right) is determined by the `HeaderToolbarChipSelection` config - specifically whether `TabsPanel` appears in the left or right items list (line 20259).

**Display Modes**

There are three resolved modes:

- **Panes** — shows individual panes as rows (granularity = Panes)
- **FocusedSession** — shows tabs with focused session info (granularity = Tabs)
- **Summary** — shows condensed summary per tab (granularity = Tabs)

Each tab row shows:

- An icon with status indicator (24px)
- Primary info (command/dir/branch based on setting)
- Subtitle (branch/dir/command based on compact_subtitle setting)
- Optional badges: PR links, diff stats
- A detail sidecar overlay on hover (if `show_details_on_hover` is true) — uses a SafeTriangle algorithm to prevent flickering when moving mouse between row and sidecar

**Integration with Workspace (view.rs)**

The vertical tabs panel sits alongside other panels in the workspace layout. It's toggled via `workspace:toggle_vertical_tabs_panel` keybinding. When enabled, it replaces the horizontal tab bar. The panel state includes scroll position, search query, detail hover state, and resizable dimensions.

**About your described setup** — Warp as a shell manager for zsh with vertical tabs and AI disabled: this is a perfectly valid config. The vertical sidebar gives you a persistent overview of all terminal sessions without eating horizontal space. With `display_granularity: Panes`, each split pane gets its own row. With `FocusedSession`, you see one row per tab. The AI agent feature can be independently disabled in Warp's settings without affecting the vertical tabs functionality.
