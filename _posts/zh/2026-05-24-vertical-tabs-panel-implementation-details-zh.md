---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 垂直标签面板实现细节
translated: true
type: note
---

下面是Warp垂直布局的工作原理，基于 `/Users/lzwjava/projects/warp` 的源代码：

**垂直标签面板 - 架构**

垂直标签功能用侧边栏面板取代了传统的水平标签栏。它同时受功能标志和用户设置控制：

```rust
// tab.rs 第61行
pub fn uses_vertical_tabs(ctx: &AppContext) -> bool {
    FeatureFlag::VerticalTabs.is_enabled() && *TabSettings::as_ref(ctx).use_vertical_tabs
}
```

**设置 (tab_settings.rs)**

TOML 配置路径为 `appearance.vertical_tabs.*`：

| 设置 | 默认值 | 选项 |
| ------ | -------- | ------ |
| `enabled` | false | bool |
| `view_mode` | Compact | Compact, Expanded |
| `display_granularity` | Panes | Panes, Tabs |
| `tab_item_mode` | FocusedSession | FocusedSession, Summary |
| `primary_info` | Command | Command, WorkingDirectory, Branch |
| `compact_subtitle` | Branch | Branch, WorkingDirectory, Command |
| `show_pr_link` | true | bool |
| `show_diff_stats` | true | bool |
| `show_details_on_hover` | true | bool |

**渲染方式 (vertical_tabs.rs)**

面板作为一个可调整宽度的侧边栏进行渲染（第1485-1541行）：

1. 一个 `ClippedScrollable` 列包含标签组
2. 其上方是一个带有搜索输入的 `render_control_bar`
3. 整个组件包裹在带拖动条的 `Resizable` 中（根据配置在左侧或右侧）
4. 宽度限制：最小200px，默认248px，最大为窗口宽度的50%

面板位置（左侧或右侧）由 `HeaderToolbarChipSelection` 配置决定——具体取决于 `TabsPanel` 出现在左侧还是右侧的条目列表中（第20259行）。

**显示模式**

有三种解析模式：

- **Panes** — 将每个面板显示为单独行（granularity = Panes）
- **FocusedSession** — 显示带有焦点会话信息的标签（granularity = Tabs）
- **Summary** — 每个标签显示精简摘要（granularity = Tabs）

每个标签行显示：

- 带状态指示器的图标（24px）
- 主要信息（根据设置显示命令/工作目录/分支）
- 副标题（根据 compact_subtitle 设置显示分支/工作目录/命令）
- 可选徽章：PR 链接、差异统计
- 悬停时的详细侧边栏浮层（如果 `show_details_on_hover` 为 true）——使用 SafeTriangle 算法防止鼠标在行和侧边栏之间移动时闪烁

**与工作区的集成 (view.rs)**

垂直标签面板与工作区布局中的其他面板并列。通过 `workspace:toggle_vertical_tabs_panel` 快捷键切换。启用后，它将取代水平标签栏。面板状态包括滚动位置、搜索查询、悬停细节状态和可调整尺寸。

**关于您描述的设置** — Warp 作为 zsh 的 shell 管理器，启用垂直标签且禁用 AI：这是一个完全有效的配置。垂直侧边栏让您可以持续概览所有终端会话，同时不占用水平空间。使用 `display_granularity: Panes` 时，每个分屏面板都有自己的行。使用 `FocusedSession` 时，每个标签显示一行。AI 代理功能可以在 Warp 设置中独立禁用，不会影响垂直标签功能。
