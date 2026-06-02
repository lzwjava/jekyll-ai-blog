---
audio: false
generated: true
lang: zh
layout: post
title: 修复Python distutils模块导入错误
translated: true
type: note
---

该错误是由于您环境中缺少Python标准库中的`distutils`模块所致。这在精简版Python安装中较为常见。以下是解决方法：

### 解决方案

1. **安装Python开发工具**（包含`distutils`）：

   ```bash
   sudo apt update && sudo apt install python3-distutils python3-dev
   ```

2. **重新安装`setuptools`**（确保功能正常）：

   ```bash
   pip install --upgrade --force-reinstall setuptools
   ```

3. **重新尝试安装依赖项**：

   ```bash
   pip install -r requirements.local.txt
   ```

### 原理说明

- `python3-distutils`提供缺失的`distutils`模块
- `python3-dev`包含必要的头文件/构建工具
- 重新安装`setuptools`可解决残留的配置问题

若您正在使用虚拟环境，建议在安装系统包后重建虚拟环境，以确保环境能正确访问所需模块。
