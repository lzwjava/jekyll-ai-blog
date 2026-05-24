---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WW Ghostty 窗口管理命令
translated: true
type: note
---

## 综合摘要

### 构建内容

为 `ww ghostty` 新增两个命令：

| 命令 | 描述 |
|---------|-------------|
| `ww ghostty list` | 列出所有已打开的 Ghostty 窗口，包括 ID、标题、位置、尺寸 |
| `ww ghostty focus <N\|title>` | 根据索引或标题子串将 Ghostty 窗口缩放至接近全屏 |
| `ww ghostty focus reset` | 将所有窗口变换恢复至原始尺寸/位置 |

### 创建的文件

- `/Users/lzwjava/projects/ww/ww/ghostty/list_windows.py` — 通过内联 Swift 代码进行 CGWindowList 枚举
- `/Users/lzwjava/projects/ww/ww/ghostty/focus.py` — 使用 CGSSetWindowTransform 缩放并重新定位窗口

### 修改的文件

- `/Users/lzwjava/projects/ww/ww/main.py` — 在 ghostty 部分增加了 `list` 和 `focus` 的分发逻辑及帮助文本

### `list` 工作原理

使用 `CGWindowListCopyWindowInfo`（CoreGraphics，无需权限）枚举屏幕上所有 Ghostty 窗口。Swift 代码通过 `swift -e` 运行，解析制表符分隔的输出并格式化为表格：

```
#      Window ID  Title                                    Position         Size
    1. [6419]  hermes                                   (220,203)        760x533
    2. [3932]  lzw@to: /mnt/data/deepseek-v4-inference  (43,177)         995x699
```

### `focus` 工作原理（最终版本）

使用 SkyLight 私有框架的 `CGSSetWindowTransform`。它对窗口应用二维仿射变换——放大并平移以填充主显示器（保留少量内边距和菜单栏偏移）。不会抢夺键盘焦点；当前终端仍保持输入焦点。

### 尝试过但已放弃的方案

1. **CGEvent 鼠标点击** — 窗口重叠时不可靠（点击到错误窗口）。在 macOS Sequoia+ 上还需要屏幕录制权限。

2. **AXUIElement（辅助功能 API）** — 返回错误 -25211（“不受信任”）。需要终端应用在系统设置 > 隐私与安全性 > 辅助功能中获得辅助功能权限。

3. **AppleScript / System Events** — 没有辅助功能权限时同样出现 -25211 错误。

4. **CGEvent 键盘（Cmd+`）** — 事件发送无错误但未到达 Ghostty（macOS 26.5 上静默丢弃，可能是 Sequoia 安全限制）。

5. **CGSOrderWindow** — 未崩溃但 CGWindowList 的 z 顺序未更新，且无法验证视觉结果。

6. **SLSMoveWindow / SLSGetWindowBounds / CGSMoveWindow** — 在 macOS 26.5 上均导致段错误。SkyLight 内部签名已更改，或需要修改 SIP 才能获得的授权。

7. **SLSSetWindowShape** — 崩溃（期望 CGSRegionRef 而非 CGRect）。

### 在 macOS 26.5 上可用的方案

| API | 状态 | 用途 |
|-----|--------|---------|
| `CGWindowListCopyWindowInfo` | ✅ 可用 | 列出/枚举窗口 |
| `CGSSetWindowTransform` | ✅ 可用 | 视觉上缩放+平移窗口 |
| `CGSOrderWindow` | ✅ 可用（CGWindowList 中视觉 z 顺序未改变） | 将窗口置于最前 |
| `SLSSetWindowLevel` | ✅ 可用 | 改变窗口层级 |
| `NSWorkspace.shared.runningApplications` | ✅ 可用 | 查找/激活应用 |

### 当前方法的局限性

- `CGSSetWindowTransform` 是**视觉变换**——窗口的后端存储大小不变，但渲染时被缩放。文本会显得更大。
- 没有辅助功能权限或可用的 CGS 移动/调整大小 API，无法通过编程方式改变窗口的实际边界。
- `reset` 命令会重置变换，但如果窗口在缩放后被手动调整过大小，则无法恢复。