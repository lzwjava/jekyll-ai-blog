---
audio: false
generated: true
lang: zh
layout: post
title: 统计目录中的文件数量
translated: true
type: note
---

要统计目录中的文件数量，可根据操作系统和工具采用多种方法。以下是常见方案：

### **Windows 系统（命令提示符）**

```cmd
dir /a-d | find /c /v ""
```

- 列出所有文件（不含目录）并统计非空行数

### **Windows 系统（PowerShell）**

```powershell
(Get-ChildItem -File).Count
```

- 获取文件对象并直接计数

### **Linux/macOS 系统（终端）**

```bash
ls -l | grep ^- | wc -l
```

- 列出详细信息，筛选常规文件（以`-`开头），最后进行计数

或使用更简洁的方式：

```bash
find . -maxdepth 1 -type f | wc -l
```

- 在当前目录（`-maxdepth 1`）查找文件类型（`-type f`）并计数

### **使用 Python 脚本**

```python
import os
file_count = len([f for f in os.listdir('.') if os.path.isfile(f)])
print(file_count)
```

- 遍历目录内容，验证文件属性后计数

请根据运行环境选择合适的方法。如需了解特定系统工具的详细用法，可随时告知！
