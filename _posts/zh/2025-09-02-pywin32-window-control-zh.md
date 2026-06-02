---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyWin32窗口控制基础
translated: true
type: note
---

以下是关于使用 **PyWin32 窗口**的指南——重点介绍其属性、激活和底层区域处理。

---

## 1. PyWin32 中的窗口是什么？

在 PyWin32 中，“窗口”指的是由 Windows API 管理的任何具有**句柄 (HWND)** 的 GUI 元素。这可以是顶级应用程序窗口、对话框，甚至是表单内的控件。

你通常通过以下方式与窗口交互：

* `win32gui` – 用于窗口句柄、属性和消息的低级函数。
* `win32con` – 用于 Windows 消息和样式的常量。
* `win32api` – 通用的 Windows API 函数。

---

## 2. 常见窗口属性

窗口有许多可以查询或修改的属性：

* **句柄 (HWND)**：窗口的唯一标识符。
* **标题**：标题栏中显示的文本 (`win32gui.GetWindowText(hwnd)`)。
* **类名**：窗口注册的类 (`win32gui.GetClassName(hwnd)`)。
* **样式**：定义窗口的行为/外观 (`GetWindowLong` 配合 `GWL_STYLE`)。
* **位置和大小**：通过 `GetWindowRect(hwnd)` 或 `MoveWindow` 获取矩形坐标。
* **可见性**：窗口是否显示 (`IsWindowVisible`)。
* **启用状态**：是否接受输入 (`IsWindowEnabled`)。
* **父窗口/所有者**：窗口的层次结构 (`GetParent(hwnd)`)。

---

## 3. 窗口激活

要将窗口置于前台或使其激活：

* **SetForegroundWindow(hwnd)** – 使窗口成为活动窗口。
* **SetActiveWindow(hwnd)** – 激活窗口，但不保证置顶。
* **BringWindowToTop(hwnd)** – 将其提升到其他窗口之上。
* **ShowWindow(hwnd, flag)** – 根据 `flag` 显示/隐藏/最小化/最大化窗口（例如 `SW_SHOW`、`SW_MINIMIZE`、`SW_RESTORE`）。

---

## 4. “底层区域”（Z 顺序和位置）

窗口按 Z 顺序分层：

* **置顶** – 始终在其他窗口之上（使用 `SetWindowPos` 配合 `HWND_TOPMOST`）。
* **底层** – 可以使用 `SetWindowPos(hwnd, win32con.HWND_BOTTOM, …)` 将窗口推到所有其他窗口之后。
* **无激活** – 可以在不激活窗口的情况下显示或定位窗口（使用 `SWP_NOACTIVATE` 等标志）。

这对于希望后台工具窗口保持打开但不抢占焦点的情况非常有用。

---

## 5. 常用函数示例

以下是一些关键的 PyWin32 函数及示例：

```python
import win32gui
import win32con

# 通过标题查找窗口
hwnd = win32gui.FindWindow(None, "无标题 - 记事本")

# 获取属性
title = win32gui.GetWindowText(hwnd)
rect = win32gui.GetWindowRect(hwnd)  # (left, top, right, bottom)

# 激活窗口
win32gui.SetForegroundWindow(hwnd)

# 移至底层（在其他窗口之后）
win32gui.SetWindowPos(hwnd, win32con.HWND_BOTTOM, 0, 0, 0, 0,
                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

# 显示/恢复窗口
win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
```

---

## 6. 事件/消息处理

你还可以通过以下方式挂钩窗口事件（激活、调整大小、关闭）：

* 使用 `SetWindowLong` 进行子类化。
* 使用 `SendMessage` / `PostMessage` 模拟操作。
* 处理诸如 `WM_ACTIVATE`、`WM_SIZE` 等消息。

---

✅ 总结：

* **属性**：标题、类名、大小、样式、可见性、启用状态。
* **激活**：使用 `SetForegroundWindow`、`BringWindowToTop`。
* **底层区域**：使用 `SetWindowPos` 和 `HWND_BOTTOM` 管理 Z 顺序。

是否需要我提供一个**实用脚本**，列出所有顶级窗口及其属性（标题、位置、Z 顺序），并允许你交互式地激活或将它们发送到底层？
