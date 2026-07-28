---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Zed JSON键位映射修复
translated: true
type: note
---

问题就在这里——`// comments`在JSON中无效。现在该文件是有效的JSON，应该可以正常工作了。

以下是清理后的版本：

**`~/.config/zed/keymap.json`**

```json
[
  {
    "context": "Editor && vim_mode == false",
    "bindings": {
      "ctrl-x ctrl-left": "editor::GoBack",
      "ctrl-x ctrl-right": "editor::GoForward",
      "ctrl-x left": "editor::GoBack",
      "ctrl-x right": "editor::GoForward",
      "alt-left": "editor::GoBack",
      "alt-right": "editor::GoForward"
    }
  }
]
```

Zed会立即识别该文件（无需重启）。在**Alt+点击**跳转到定义后：

| 按键 | 操作 |
|---|---|
| `Ctrl+x ←` | Go Back（返回之前的位置） |
| `Ctrl+x →` | Go Forward（前进到之后的位置） |
| `Alt+←` | Go Back（备选返回方式） |
| `Alt+→` | Go Forward（备选前进方式） |

如果仍然看到错误，请尝试打开Zed的命令面板（`Cmd+Shift+P`），然后运行**“zed: open default keymap”**来检查确切的命令名称——它们区分大小写。