---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Pyperclip：Python剪贴板管理指南
translated: true
type: note
---

### 什么是 Pyperclip？
Pyperclip 是一个轻量级的 Python 库，用于访问和操作系统剪贴板（复制粘贴功能）。它支持跨平台（Windows、macOS、Linux），并支持将文本复制到剪贴板以及从剪贴板粘贴文本。注意：它仅处理文本；对于文件或图像，请使用其他库。

### 安装
通过 pip 安装 Pyperclip：
```
pip install pyperclip
```

在 Linux 上，可能需要额外的依赖项才能访问剪贴板（例如 `xclip` 或 `xsel`）。使用包管理器安装它们（例如，在 Ubuntu 上使用 `sudo apt-get install xclip`）。

### 基本用法
1. **导入库**：
   ```python
   import pyperclip
   ```

2. **将文本复制到剪贴板**：
   ```python
   pyperclip.copy("Hello, world!")
   ```
   这会将字符串 "Hello, world!" 放入剪贴板。

3. **从剪贴板粘贴文本**：
   ```python
   text = pyperclip.paste()
   print(text)  # 输出当前剪贴板内容
   ```
   这会检索并打印剪贴板中的文本。

### 示例：将用户输入复制到剪贴板
```python
import pyperclip

user_input = input("输入要复制的文本：")
pyperclip.copy(user_input)
print("文本已复制到剪贴板！")
```

### 示例：粘贴并修改
```python
import pyperclip

pyperclip.copy("原始文本")
modified = pyperclip.paste().upper()  # 粘贴后修改（例如转换为大写）
pyperclip.copy(modified)
print("修改后的文本已复制。")
```

### 额外提示
- **错误处理**：在某些系统上（例如无头服务器或某些 Linux 发行版），剪贴板访问可能会失败。使用 try-except 包装：
  ```python
  try:
      pyperclip.copy("文本")
  except pyperclip.PyperclipException as e:
      print(f"剪贴板错误：{e}")
  ```
- **检查可用性**：在脚本运行后立即使用 `pyperclip.paste()`，因为剪贴板内容在多次运行之间会保留。
- **限制**：不适用于二进制数据；仅支持文本。高级用法请参阅[官方文档](https://github.com/asweigart/pyperclip)。

以上是基本内容——可以先尝试复制和粘贴一个简单的字符串进行测试。如果遇到平台特定问题，请查看该库的 GitHub 仓库。
