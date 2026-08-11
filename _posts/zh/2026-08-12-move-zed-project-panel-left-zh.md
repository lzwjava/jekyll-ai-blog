---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将Zed项目面板移到左侧
translated: true
type: note
---

已完成。已在 `~/.config/zed/settings.json` 中创建以下配置：

```json
{
  "project_panel": {
    "dock": "left"
  }
}
```

说明：
- 这是 Zed 用于定位文件浏览器（“项目面板”）的设置：`project_panel.dock` 接受 `"left"` 或 `"right"`（已根据你的 Zed 1.14.2 二进制文件中的内置设置模式验证）。
- Zed 会热加载 `settings.json`，因此打开的窗口应能立即重新停靠面板。如果某个工作区之前已将面板拖拽到右侧，请重新启动 Zed（或再次将其拖回左侧），之后面板将始终保持在左侧。
- 额外提示：`~/.config/zed/` 正是 `ww sync zed` 同步的内容，因此该更改将通过 `uv run ww sync zed` 传播到你的其他机器。