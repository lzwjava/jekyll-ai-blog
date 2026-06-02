---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ghostty 命令与 AXDocument 访问
translated: true
type: note
---

## 摘要

### 构建内容

为 `ww` 命令行工具新增了 `ww ghostty list` 和 `ww ghostty focus` 命令。

### `ww ghostty list`

列出所有 Ghostty 窗口，包括 ID、标题、位置和尺寸。现在还会通过 **AXDocument** 无障碍属性显示 **hermes 项目名称** —— 每个 Ghostty 窗口将其工作目录暴露在 `kAXDocumentAttribute` 中，我们通过 AXUIElement 读取该属性（需要无障碍权限）。

当前输出：

```
 #      Window ID  Title                                    Position         Size
    2. [1605]  hermes [openwrt]                         (28,224)         760x533
    3. [3172]  hermes [ww]                              (503,90)         760x533
    5. [3790]  hermes [jekyll-ai-blog]                  (682,119)        760x533
    6. [6313]  hermes [hermes-agent]                    (260,132)        995x699
    ...
```

### `ww ghostty focus <N|title>`

使用 `CGSSetWindowTransform`（SkyLight 私有 API）将 Ghostty 窗口缩放至近乎全屏。同时支持 `ww ghostty focus reset` 以恢复所有窗口。

### 关键发现：`AXDocument`

突破在于发现 Ghostty 将其每个终端标签页的工作目录作为 `kAXDocumentAttribute` 暴露在其 AXUIElement 窗口上。这使得我们无需通过进程树匹配，即可将“hermes”窗口与其项目目录对应起来。

### 需要清理的小问题

1. **窗口 1**（`[1544]`，尺寸 84x77）是一个小弹窗/通知——应过滤掉
2. **窗口 17-18**（位置 526,139）未显示项目——它们似乎处于屏幕外或最小化状态，因此 AXUIElement 未返回其 `AXDocument`
3. **窗口 7** 显示 `hermes  [ww]`，多了一个空格（原始标题为 `hermes` 带有尾随空格）

### 文件变更

- `/Users/lzwjava/projects/ww/ww/ghostty/list_windows.py` —— CGWindowList + AXUIElement AXDocument
- `/Users/lzwjava/projects/ww/ww/ghostty/focus.py` —— CGSSetWindowTransform 缩放
- `/Users/lzwjava/projects/ww/ww/main.py` —— 分派 + 帮助文本

### 尝试过但已放弃的方法

| 方法 | 失败原因 |
|------|----------|
| CGEvent 鼠标点击 | 窗口重叠时不可靠 |
| CGEvent 键盘（Cmd+`） | macOS 26.5 上静默丢弃 |
| CGSOrderWindow | CGWindowList 的 Z 顺序不更新 |
| SLSMoveWindow / SLSGetWindowBounds | macOS 26.5 上出现段错误 |
| 进程树 TTY 匹配 | 无法将 TTY 映射到窗口 ID |
| 空闲时间 / atime 检测 | 粒度太粗，聚焦时不会改变 |
| S+ 前台标记 | 按终端而非全局焦点 |

需要我清理这些小问题并提交吗？
