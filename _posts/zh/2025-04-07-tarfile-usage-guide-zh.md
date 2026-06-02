---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Python tarfile模块使用指南
translated: true
type: note
---

### 导入 tarfile 模块
要在 Python 中使用 `tarfile` 库，首先需要导入它：
```python
import tarfile
```
该模块是 Python 标准库的一部分，无需安装。它基于 POSIX tar 格式，支持读写压缩或未压缩的 tar 归档文件。

### 打开和创建 Tar 归档文件
- **打开现有 tar 文件**：使用 `tarfile.open()` 并指定模式。模式包括 `'r'`（读取）、`'w'`（清空写入）、`'a'`（追加），以及带压缩的变体如 `'r:gz'`（gzip 压缩）。
  ```python
  import tarfile

  # 以读取模式打开（未压缩）
  with tarfile.open('example.tar', 'r') as tar:
      # 在此处操作 tar 文件
      pass
  ```
- **创建新的 tar 文件**：使用 `'w'` 模式创建空归档。可添加压缩前缀如 `'w:gz'`（gzip）或 `'w:bz2'`（bzip2）。
  ```python
  # 创建压缩的 tar.gz 文件
  with tarfile.open('archive.tar.gz', 'w:gz') as tar:
      pass
  ```

### 向归档添加文件
- **添加单个文件**：在 tar 文件对象上调用 `add()` 方法，传入文件路径。可通过 arcname 指定归档内的不同名称。
  ```python
  with tarfile.open('archive.tar.gz', 'w:gz') as tar:
      tar.add('file.txt')  # 按原样添加 file.txt
      tar.add('data.csv', arcname='renamed_data.csv')  # 在归档内重命名
  ```
- **添加多个文件或目录**：在循环中使用 `add()`，或递归添加整个目录。
  ```python
  import os

  with tarfile.open('backup.tar', 'w') as tar:
      for root, dirs, files in os.walk('my_folder'):
          for file in files:
              tar.add(os.path.join(root, file))
  ```

### 从归档提取文件
- **提取所有文件**：使用 `extractall()` 提取到指定目录（默认为当前目录）。
  ```python
  with tarfile.open('archive.tar.gz', 'r:gz') as tar:
      tar.extractall(path='extracted_folder')  # 必要时创建文件夹
  ```
- **提取特定文件**：先用 `getmembers()` 列出成员，再使用 `extract()`。
  ```python
  with tarfile.open('example.tar', 'r') as tar:
      members = tar.getmembers()
      for member in members:
          if 'important' in member.name:  # 示例过滤条件
              tar.extract(member, path='output_dir')
  ```
- 注意：出于安全考虑，应过滤路径（例如避免 `..`）以防止路径遍历攻击。`tarfile` 会进行一些检查，但对于不受信任的归档建议手动过滤。

### 列出归档内容
- **遍历文件**：使用 `getmembers()` 或直接迭代 tar 对象获取 TarInfo 对象。
  ```python
  with tarfile.open('example.tar', 'r') as tar:
      for member in tar.getmembers():
          print(f"{member.name}: {member.size} bytes")
  ```

### 关键模式与压缩
- `'r'`：读取未压缩 tar
- `'r:gz'`、`'r:bz2'`、`'r:xz'`：读取压缩格式
- `'w'`：新建未压缩 tar（覆盖）
- `'a'`：追加到现有 tar
- 读取时自动检测压缩；写入时需明确指定

### 提示与最佳实践
- 始终使用上下文管理器（`with` 语句）确保文件正确关闭
- 对于大型归档，建议通过过滤或选择性提取来节省内存
- `tarfile` 不直接处理加密归档——如需加密请使用外部工具或手动结合 `gzip`
- 错误处理：捕获 `tarfile.TarError` 处理归档问题
- 完整文档：参考 Python 官方 [tarfile 文档](https://docs.python.org/3/library/tarfile.html)了解自定义过滤器等高级功能
