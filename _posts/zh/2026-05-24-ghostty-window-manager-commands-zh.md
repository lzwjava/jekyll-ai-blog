---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ghostty 窗口管理器命令
translated: true
type: note
---

完成。添加了两个新命令：

```
ww ghostty list         # 列出所有打开的 Ghostty 窗口，包含 ID、标题、位置、大小
ww ghostty focus <N>    # 根据索引（如 7）或标题子串（如 "deepseek"）聚焦窗口
ww ghostty focus        # 无参数 = 列出窗口并显示用法提示
```

创建的文件：
- /Users/lzwjava/projects/ww/ww/ghostty/list_windows.py — 通过 Swift 枚举 CGWindowList
- /Users/lzwjava/projects/ww/ww/ghostty/focus.py — 通过 CGEvent 鼠标点击将窗口提升到前台

修改的文件：
- /Users/lzwjava/projects/ww/ww/main.py — 分发逻辑 + 帮助文本

工作原理：
- `list` 使用 `CGWindowListCopyWindowInfo`（无需无障碍权限）枚举所有 Ghostty 窗口
- `focus` 激活 Ghostty 应用，然后在目标窗口边界中心发送 CGEvent 鼠标点击以将其提升到前台。支持基于 1 的索引和标题子串匹配。
