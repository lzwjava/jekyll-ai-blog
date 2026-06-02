---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 聚焦macOS窗口的Swift脚本
translated: true
type: note
---

以下是逐步的工作原理：

**1. 列出所有 Ghostty 窗口**

我编写了一个 Swift 脚本，使用 macOS 的 CoreGraphics 中的 `CGWindowListCopyWindowInfo` API。这也是 Activity Monitor 用来列出窗口的同一 API。它返回每个屏幕窗口的元数据——所有者名称、窗口标题、位置、大小以及唯一的 `CGWindowID`。

```
swift -e '
import Cocoa
import CoreGraphics
// CGWindowListCopyWindowInfo 枚举所有屏幕窗口
// 按所有者名称 == "ghostty" 过滤
// 提取：窗口 ID、标题、位置、大小
'
```

无需特殊权限——这是一个只读的公共 API。

**2. 按 ID 聚焦特定窗口**

这是比较难的部分。编译后的脚本位于 `/tmp/focus_window`。它执行以下操作：

```
步骤 1：通过 CGWindowListCopyWindowInfo 按窗口 ID 过滤，查找目标窗口的边界（x, y, width, height）
步骤 2：通过 NSRunningApplication.activate() 激活 Ghostty 应用
        （将应用带到前台，但只有最后聚焦的窗口）
步骤 3：计算目标窗口的中心点
步骤 4：坐标转换——CGWindowList 返回“左上角原点”坐标，
        但 CGEvent 使用 Quartz 坐标（左下角原点）。
        因此：quartzY = screenHeight - clickY
步骤 5：通过 CGEvent 发布合成鼠标事件：
        - mouseMoved 到中心点
        - leftMouseDown
        - leftMouseUp
        这样“点击”目标窗口，告诉 macOS 聚焦它。
```

**限制：**

- `CGEvent.post(tap: .cghidEventTap)` 在 HID 级别注入事件。它可以工作，但属于合成点击——它会与屏幕位置上的任何内容交互。如果弹窗或覆盖层挡在中间，它会被点击到。
- 如果你授予运行此进程（Terminal 或 Hermes）**辅助功能**权限，我可以使用通过 System Events 的 AppleScript（`tell process "ghostty" to set frontmost to true, perform action "AXRaise" of window N`），这样更精确——无需合成点击，只需一个辅助功能命令来提升特定窗口。
- Swift 脚本需要编译一次（`swiftc`），我已在 `/tmp` 中完成。它是临时性的——重启后仍然存在。

**磁盘上的文件：**

| 文件 | 用途 |
|------|---------|
| `/tmp/focus_window.swift` | 源代码——列出窗口边界、激活应用、点击中心 |
| `/tmp/focus_window` | 编译后的二进制文件（macOS arm64） |
| `/tmp/raise_window.swift` | 更简单的变体——仅激活应用，无点击 |

如果你希望它更健壮，我可以：
1. 安装 `cliclick`（`brew install cliclick`）——一个用于合成鼠标/键盘事件的小型 CLI，比编译 Swift 更简单
2. 授予辅助功能访问权限，以便我可以使用 AppleScript 实现无需点击的干净窗口提升
