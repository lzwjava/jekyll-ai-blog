---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 使用Python发送Windows Toast通知
translated: true
type: note
---

### 什么是 win10toast？
win10toast 是一个轻量级 Python 库，可让你通过 Python 脚本在 Windows 10 上发送 toast 通知（弹出式提醒）。它适用于桌面应用程序或脚本中的用户通知，类似于原生的 Windows toast。

### 前置条件
- 已安装 Python 3.x
- Windows 10（依赖 Windows 特定的 API）
- 除 Python 外无需其他依赖项

### 安装
通过 pip（Python 包安装工具）安装该库：

```
pip install win10toast
```

如果使用虚拟环境，请先激活它。

### 基本用法
1. 导入模块：
   ```python
   from win10toast import ToastNotifier
   ```

2. 创建一个 `ToastNotifier` 实例，并调用其 `show_toast` 方法来显示通知：
   ```python
   toaster = ToastNotifier()
   toaster.show_toast("标题", "消息", icon_path=None, duration=5)
   ```
   - **标题**：通知标题的字符串
   - **消息**：通知正文的字符串
   - **icon_path**：可选参数，指向通知图标文件的路径（例如 `"path/to/icon.ico"`）。省略则不显示图标
   - **duration**：toast 显示的时长（默认 5 秒；Windows 可能会覆盖此设置）

通知将显示在操作中心并作为弹窗出现。

### 高级用法
- **自定义图标**：使用图像文件（推荐 128x128 像素以获得最佳质量）
- **处理点击事件**：传递回调函数（支持有限；主要用于基本的点击行为）
- **多个通知**：实例化一次 `ToastNotifier` 并重复使用以发送多个 toast
- **错误处理**：使用 try-except 包装以处理潜在的 Windows API 问题，例如通知被禁用

带图标和错误处理的示例：
```python
from win10toast import ToastNotifier
import os

try:
    toaster = ToastNotifier()
    icon = "C:\\path\\to\\icon.ico"  # 替换为实际路径
    toaster.show_toast("提醒！", "你的脚本已执行完成。", icon_path=icon, duration=10)
except Exception as e:
    print(f"通知发送失败：{e}")
```

### 限制与提示
- 通知需要启用 Windows 10 的操作中心（设置 > 系统 > 通知和操作）
- 如需更复杂的功能（例如操作或图像），请考虑使用替代方案，如 plyer 或 winrt（现代 Windows SDK 的一部分）
- 如果通知未显示，请检查 Windows 的专注助手设置，或尝试以管理员身份运行脚本

完整文档请查看 [win10toast GitHub 仓库](https://github.com/Charnelx/win10toast)。如果遇到问题，请提供错误详情以获得针对性帮助。
