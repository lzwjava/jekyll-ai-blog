---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: PyGetWindow 快速入门指南
translated: true
type: note
---

### 安装
PyGetWindow 是一个用于在多种平台（Windows、macOS 和 Linux）上操作和查询窗口的 Python 库。通过 pip 安装：

```bash
pip install pygetwindow
```

### 导入模块
首先在 Python 脚本中导入模块：

```python
import pygetwindow as gw
```

### 获取窗口对象
PyGetWindow 将窗口表示为 `Window` 对象。您可以通过标题、进程或其他属性检索窗口。

- **获取所有窗口对象**：
  使用 `gw.getAllWindows()` 返回所有打开窗口的列表。

- **按标题获取窗口**：
  使用 `gw.getWindowsWithTitle(title)` 或 `gw.getFirstWindowWithTitle(title)` 进行部分或精确匹配。

- **获取活动窗口**：
  使用 `gw.getActiveWindow()` 获取当前聚焦的窗口。

示例：
```python
windows = gw.getAllWindows()
active = gw.getActiveWindow()
notepad = gw.getWindowsWithTitle('Notepad')  # 包含标题中带有 'Notepad' 的窗口列表
```

### 窗口对象的常用方法
获取 `Window` 对象后，您可以访问以下属性和方法：

- **属性**：`title`、`left`、`top`、`width`、`height`、`isMinimized`、`isMaximized`、`isActive`。
- **方法**：
  - `activate()`：将窗口置于前台并激活。
  - `maximize()` / `minimize()` / `restore()` / `close()`：控制窗口状态。
  - `resize() / move()`：调整大小和位置。

示例：
```python
if notepad:
    win = notepad[0]
    print(win.title)  # 输出：例如 'Untitled - Notepad'
    win.activate()
    win.maximize()
    win.move(100, 100)  # 移动到位置 (100, 100)
    win.resize(800, 600)  # 调整大小为 800x600
```

### 多平台处理
- 在 Windows 和 macOS 上，它使用原生 API。
- 在 Linux 上，它依赖 X11 或 Wayland 支持；请确保系统已安装相关依赖（例如 Ubuntu 上的 `x11-utils`）。
- 如果某个方法在您的操作系统中不受支持，可能会引发 `NotImplementedError`。

### 示例
以下是一些实用代码片段：

1. **打印所有窗口标题**：
   ```python
   for win in gw.getAllWindows():
       print(win.title)
   ```

2. **关闭特定窗口**：
   ```python
   firefox_wins = gw.getWindowsWithTitle('Mozilla Firefox')
   if firefox_wins:
       firefox_wins[0].close()
   ```

3. **移动和调整多个窗口大小**：
   ```python
   windows = gw.getAllWindows()
   for i, win in enumerate(windows[:3]):  # 前 3 个窗口
       win.move(50 * i, 50 * i)
       win.resize(400, 400)
   ```

有关高级用法，请参阅[官方文档](https://pygetwindow.readthedocs.io/)。如果遇到平台特定问题，请检查系统权限或依赖项（例如 Linux 上的 `xdotool`）。
