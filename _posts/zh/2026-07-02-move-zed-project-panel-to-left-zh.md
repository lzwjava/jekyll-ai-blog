---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将Zed项目面板移动到左侧
translated: true
type: note
---

问题：如何将 Zed 编辑器中的文件（项目）面板从右侧移到左侧？

答案：

最快方法 —— 无需编辑配置：

- 命令面板（`Cmd+Shift+P`）→ 执行 `project panel: toggle focus`，然后将面板标签拖到左侧停靠区。或者直接拖动项目面板的标签栏到窗口左边缘；Zed 会自动将其停靠在那里，并为你重写 `settings.json`。

直接方法 —— 编辑 settings.json：

```bash
# Cmd+, 打开设置，或直接编辑文件：
vim ~/.config/zed/settings.json
```

添加/编辑这个键：

```json
{
  "project_panel": {
    "dock": "left"
  }
}
```

保存后，Zed 会立即热加载设置 —— 无需重启。

针对你具体设置的说明：

- 默认情况下，原生 Zed 的 `"dock"` 值为 `"left"` —— 默认的项目面板配置将 `"dock"` 设为 `"left"`，所以如果你的面板在右侧，说明有东西（你复制的主题/配置，或手动拖拽）明确将其设为了 `"right"`。
- 既然你正在修改配置，不妨一次性决定好其余面板的布局，因为 Zed 允许你将通知面板、聊天面板、大纲面板和项目面板独立停靠在左侧或右侧，此外 Git 面板的默认停靠也是 `"left"`，且 `dock` 是可与 `button`、`default_width`、`status_style`、`sort_by_path` 一同设置的选项。
- 如果你使用 Git 面板，请注意它有自己的 `dock` 键，因此默认情况下 Git 面板停靠在左侧，你可以通过 Panels > Git Panel > Git Panel Dock 更改 —— 与 `project_panel` 相互独立。

如果你想将项目面板和 Git 面板都固定在左侧，快速参考配置块如下：

```json
{
  "project_panel": { "dock": "left" },
  "git_panel": { "dock": "left" },
  "outline_panel": { "dock": "right" }
}
```

参考链接：

- [配置 Zed](https://zedhub.dev/configuring-zed)
- [Zed Git 集成文档](https://zed.dev/docs/git)
- [我是如何配置 Zed 编辑器作为日常驱动的](https://dev.to/hitblast/how-i-configured-the-zed-editor-for-daily-driving-4k2k)
