---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复PIL图像后端错误
translated: true
type: note
---

这个错误意味着你的 PIL 安装要么缺少二进制后端（`_imaging`），要么你不小心使用了旧的 "PIL" 包而不是现代的 "Pillow"。以下是修复方法：

1. **确保使用 Python 3**
   如果 `python` 指向的是 Python 2，请切换到 Python 3：

   ```bash
   python3 --version
   python3 scripts/content/avatar.py
   ```

2. **卸载过时的 PIL 包**

   ```bash
   # 如果旧版 PIL 是通过 pip 安装的，此命令会将其移除
   python3 -m pip uninstall -y PIL
   ```

3. **（重新）安装 Pillow**

   ```bash
   python3 -m pip install --upgrade --force-reinstall pillow
   ```

4. **安装必要的系统库**
   在 Ubuntu 系统上，你需要安装图像头文件以便 Pillow 能构建其 `_imaging` 扩展：

   ```bash
   sudo apt update
   sudo apt install -y libjpeg-dev zlib1g-dev
   # 然后重新安装 Pillow 使其针对这些库重新编译
   python3 -m pip install --upgrade --force-reinstall pillow
   ```

5. **使用虚拟环境（可选但推荐）**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install pillow
   python scripts/content/avatar.py
   ```

完成这些步骤后，`from PIL import Image` 应该就能正常工作，不会再出现 `_imaging` 导入错误。
