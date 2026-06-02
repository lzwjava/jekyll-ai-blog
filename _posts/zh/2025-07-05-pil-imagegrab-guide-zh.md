---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: PIL ImageGrab 截图指南
translated: true
type: note
---

### 前置准备
要使用 PIL (Pillow) 库中的 `ImageGrab` 模块，请确保已安装 Pillow。在 Windows 系统上可通过 pip 安装：
```
pip install Pillow
```
Windows 系统通常无需额外配置，因为 `ImageGrab` 直接调用原生 Windows API。

### 基础用法
`ImageGrab.grab()` 可捕获整个屏幕（所有显示器）并返回 PIL Image 对象。以下是一个保存屏幕截图为 PNG 文件的简单示例：

```python
from PIL import ImageGrab

# 捕获整个屏幕
screenshot = ImageGrab.grab()

# 将图像保存至文件
screenshot.save("screenshot.png")
```

执行后将在当前工作目录生成名为 `screenshot.png` 的文件。

### 扩展功能
- **捕获指定区域**：通过像素坐标元组（左, 上, 右, 下）定义捕获区域
  ```python
  # 捕获从坐标(100,100)开始的300x300像素区域
  region = (100, 100, 400, 400)  # 请根据实际需求调整坐标
  screenshot = ImageGrab.grab(bbox=region)
  screenshot.save("region_screenshot.png")
  ```
- **包含鼠标光标**（取决于系统支持，请查阅对应 Pillow 版本文档）：
  ```python
  # 注意：部分系统可能需要设置 include_layered_windows=True
  screenshot = ImageGrab.grab(include_layered_windows=True)
  ```
- **预览图像**：使用 `screenshot.show()` 在默认图片查看器中打开（适用于测试）

### 注意事项
- 坐标系统以主显示器左上角为原点 (0, 0)，单位为像素
- 多显示器环境下，`grab()` 会将所有屏幕内容合并为单一图像
- 若遇权限问题（如新版 Windows 系统的截屏限制），请确保脚本具有屏幕捕获权限，或尝试以管理员权限运行
- 完整文档参阅：[Pillow ImageGrab 文档](https://pillow.readthedocs.io/en/stable/reference/ImageGrab.html)。如遇 Windows 特定问题，可查阅 GitHub 议题记录获取解决方案
