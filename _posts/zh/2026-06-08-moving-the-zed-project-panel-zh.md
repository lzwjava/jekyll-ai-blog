---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 移动Zed项目面板
translated: true
type: note
---

以下是Zed代码库中关于将文件资源管理器（项目面板）从右侧移动到左侧的内容：

---

## 代码分析：项目面板停靠位置

### 该机制包含3层：

**1. 设置层** (`crates/settings_content/src/workspace.rs` 第709行)

`ProjectPanelSettingsContent` 结构体包含：
```rust
/// 默认值：右侧（Agentic布局），左侧（Classic布局）
pub dock: Option<DockSide>,
```

`DockSide` 是一个简单的枚举，仅包含 `Left` 和 `Right`（项目面板没有 `Bottom`）。

**2. Panel trait 实现** (`crates/project_panel/src/project_panel.rs` 第7257行)

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

当你改变位置时，它会**持久化写入你的 settings.json 文件**。

**3. 布局预设** (`crates/agent_settings/src/agent_settings.rs` 第40-55行)

两个内置布局决定了默认值：

```rust
const AGENT: Self = Self {
    project_panel_dock: Some(DockSide::Right),  // <-- Agent 布局：右侧
    // ...
};

const EDITOR: Self = Self {
    project_panel_dock: Some(DockSide::Left),   // <-- Editor 布局：左侧
    // ...
};
```

**4. 右键上下文菜单** (`crates/workspace/src/dock.rs` 第1262行)

右键点击状态栏中的面板按钮会构建一个可切换的上下文菜单：
- "Dock Left"（如果当前为左侧则选中）
- "Dock Right"（如果当前为右侧则选中）
- 项目面板不显示 "Dock Bottom"（因为 `position_is_valid` 拒绝了它）

每个菜单项都会调用 `panel.set_position(position, window, cx)` 并写入设置。

**5. 键盘循环** (`crates/workspace/src/dock.rs` 第127行)

```rust
fn move_to_next_position(&self, window: &mut Window, cx: &mut App) {
    // 循环顺序：Left -> Bottom -> Right -> Left（循环）
    // 经 position_is_valid 过滤后，对于项目面板：Left -> Right -> Left
}
```

当面板获得焦点时，由 `MoveFocusedPanelToNextPosition` 动作触发。

---

## 实际操作方式（3种）：

1. **右键单击状态栏中的面板按钮** → 选择 "Dock Left"

2. **编辑 settings.json**（`~/.config/zed/settings.json`）：
   ```json
   {
     "project_panel": {
       "dock": "left"
     }
   }
   ```

3. **切换布局** — 如果你当前使用 "Agentic" 布局（默认将项目面板放在右侧），切换到 "Editor/Classic" 布局，其中默认左侧。

你的项目面板很可能在右侧，因为你正在使用 Agentic 布局，该布局将 AI 代理面板放在左侧，并将项目面板推到右侧。