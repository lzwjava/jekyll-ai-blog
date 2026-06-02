---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PIL与PyAutoGUI截图功能对比
translated: true
type: note
---

**PIL 的 `ImageGrab`** 与 **PyAutoGUI 的截图工具** 都支持屏幕捕捉，但它们在用法、功能和跨平台支持方面存在差异。

---

## 1. PIL (Pillow) – `ImageGrab`

`ImageGrab` 是 **Pillow（现代 PIL 分支）** 的组成部分，可用于捕捉整个屏幕或指定区域。

### 工作原理

* 在 **Windows 和 macOS** 上，通过原生 API（Windows 使用 GDI，macOS 使用 Quartz）捕捉像素。
* 在 **Linux** 上默认不支持（需额外安装 `xwd` 等库）。

### 使用示例

```python
from PIL import ImageGrab

# 捕捉全屏
screenshot = ImageGrab.grab()
screenshot.save("screenshot.png")

# 捕捉指定区域（左, 上, 右, 下）
region = (100, 100, 500, 500)
cropped_screenshot = ImageGrab.grab(bbox=region)
cropped_screenshot.show()
```

### 优势

* 简单易用，属于 Pillow 生态（无需额外依赖）。
* 适合已使用 Pillow 进行图像处理的场景。

### 劣势

* 默认不支持 Linux。
* 灵活性较低（无法识别多显示器）。

---

## 2. PyAutoGUI – `screenshot()`

PyAutoGUI 是更通用的自动化工具（支持鼠标/键盘控制及屏幕捕捉）。

### 工作原理

* 内部封装 **Pillow** 功能。
* 调用各操作系统 API（支持 Windows、macOS、Linux）。
* 可直接返回 Pillow `Image` 对象或保存为文件。

### 使用示例

```python
import pyautogui

# 捕捉全屏
screenshot = pyautogui.screenshot()
screenshot.save("screenshot.png")

# 捕捉指定区域（左, 上, 宽, 高）
region_screenshot = pyautogui.screenshot(region=(100, 100, 400, 400))
region_screenshot.show()
```

### 优势

* 全平台兼容（Windows、macOS、Linux）。
* 易于与自动化脚本集成（配合鼠标/键盘控制）。
* 直接支持指定区域捕捉。

### 劣势

* 因封装层级更多，速度略慢于 `ImageGrab`。
* 需额外安装依赖（`pip install pyautogui`）。

---

## 如何选择？

* **若仅需截图功能且运行环境为 Windows/macOS** → 轻量快速的 `ImageGrab` 更合适。
* **若需自动化功能或 Linux 支持** → `pyautogui` 是更优选择。

---

👉 是否需要我同时提供 **性能基准测试方法**，用 Python 代码对比 `ImageGrab` 与 `pyautogui.screenshot()` 的速度差异？
