---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 配置 Zed 在新窗口中打开项目
translated: true
type: note
---

**问题：** 如何让 Zed 编辑器始终以独立窗口打开每个项目（一个项目 = 一个窗口），无需询问且永久生效？

**答案：**

将以下内容添加到 `~/.config/zed/settings.json`：

```json
{
  "cli_default_open_behavior": "new_window"
}
```

就是这样。此设置控制 CLI 和双击行为。将其设为 `"new_window"` 后，Zed 将始终在新窗口中打开文件夹，而不是在当前窗口的线程侧边栏中打开。

直接从终端打开设置：

```sh
zed ~/.config/zed/settings.json
```

或通过命令面板：`Cmd+Shift+P` → `zed: open settings`。

**需要注意的事项：**

`cli_default_open_behavior` 仅影响 CLI（`zed ~/project`）和双击行为——它**不**影响菜单中的 `File > Open`，后者始终在当前窗口的线程侧边栏中打开。

因此，对于 `File > Open`，你仍需在“打开最近”中使用 `Cmd+Enter`（而非 Enter）来强制打开新窗口。目前没有设置可以让 `File > Open` 始终生成新窗口——这是 Zed 的限制。

**手动覆盖操作的快速参考：**

| 目标 | 操作 |
| --- | --- |
| 始终新窗口（CLI/拖拽） | 在设置中设置 `"cli_default_open_behavior": "new_window"` |
| 从“打开最近”打开新窗口 | `Cmd+Enter` 或 `Cmd+click` |
| CLI 临时打开新窗口 | `zed -n ~/myproject` |

参考资料：

- [Windows & Projects — Zed Docs](https://zed.dev/docs/windows-and-projects)
