---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Python ZipFile 包使用指南
translated: true
type: note
---

### ZipFile 包概述

Python 的 `zipfile` 模块允许你在无需外部工具的情况下读写 ZIP 归档文件。它是标准库的一部分，因此无需安装（从 Python 2.3+ 开始）。你可以通过编程方式使用它来压缩、解压缩或操作 ZIP 文件。它支持多种压缩方法，如 DEFLATE。

通过以下方式导入：`import zipfile`

### 读取 ZIP 文件

要提取或检查现有的 ZIP 文件：

1. **打开 ZIP 文件进行读取**：

   ```python
   with zipfile.ZipFile('example.zip', 'r') as zip_ref:
       # 'r' 表示读取模式
   ```

2. **列出内容**：

   ```python
   with zipfile.ZipFile('example.zip', 'r') as zip_ref:
       file_list = zip_ref.namelist()  # 返回文件名列表
       print(file_list)
   ```

3. **提取文件**：
   - 提取全部：`zip_ref.extractall('destination_folder')`
   - 提取单个：`zip_ref.extract('file_inside.zip', 'path')`

4. **在不提取的情况下读取文件内容**：

   ```python
   with zipfile.ZipFile('example.zip', 'r') as zip_ref:
       with zip_ref.open('file_inside.zip') as file:
           content = file.read()
           print(content.decode())  # 如果是文本文件
   ```

注意：始终使用 `with` 语句以实现自动关闭。对于受密码保护的 ZIP 文件，请在 `ZipFile()` 中添加 `pwd=b'password'`。

### 写入 ZIP 文件

要创建新的 ZIP 文件或添加到现有 ZIP 文件：

1. **创建新的 ZIP 文件**：

   ```python
   with zipfile.ZipFile('new_archive.zip', 'w') as zip_ref:
       # 'w' 表示写入模式（如果存在则覆盖）
   ```

2. **添加文件**：
   - 添加单个文件：`zip_ref.write('source_file.txt', 'arcname.txt')`（可选参数 arcname 可重命名内部文件名）
   - 添加多个文件：遍历文件列表并调用 `write()` 方法。

3. **写入时压缩**（默认为 DEFLATE）：

   ```python
   with zipfile.ZipFile('archive.zip', 'w', zipfile.ZIP_DEFLATED) as zip_ref:
       zip_ref.write('large_file.txt')
   ```

   选项：`ZIP_STORED`（无压缩）、`ZIP_DEFLATED`、`ZIP_BZIP2` 等。

4. **追加到现有 ZIP 文件**（使用 'a' 模式代替 'w'）。

### 常见操作与技巧

- **检查文件是否为有效 ZIP**：使用 `zipfile.is_zipfile('file.zip')`。
- **获取文件信息**：`zip_ref.getinfo('file.txt')` 返回包含大小、日期等详细信息的 ZipInfo 对象。
- **处理大文件**：读取/提取大文件可能消耗内存；使用 `open()` 方法进行流式处理。
- **错误处理**：捕获 `BadZipFile` 或 `LargeZipFile` 异常。
- **跨平台兼容**：支持 Windows、macOS、Linux，但需注意路径分隔符（使用 `/`）。
- **加密**：支持基础密码保护，但强度较弱——如需更高安全性请使用更强大的工具。
- **高级用法**：如需更多功能（例如 shutil 集成），可结合使用 `shutil.make_archive()` 来创建 ZIP 文件。

完整脚本示例（压缩文件夹）：

```python
import zipfile
import os

def zip_folder(source_dir, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                zipf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file), os.path.join(source_dir, '..')))

zip_folder('my_folder', 'output.zip')
```

完整文档请参阅 [Python 官方文档](https://docs.python.org/3/library/zipfile.html)。如果你有特定需求（例如“如何提取到内存”），请提供更多细节！
