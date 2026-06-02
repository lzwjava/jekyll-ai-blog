---
audio: false
generated: true
lang: en
layout: post
title: Count Files in a Directory
translated: false
type: note
---

To count the number of files in a directory, you can use various methods depending on your operating system and tools. Here are the most common approaches:

### **On Windows (Command Prompt)**

```cmd
dir /a-d | find /c /v ""
```

- Lists all files (not directories) and counts the lines, excluding empty ones.

### **On Windows (PowerShell)**

```powershell
(Get-ChildItem -File).Count
```

- Retrieves only files and counts them.

### **On Linux/macOS (Terminal)**

```bash
ls -l | grep ^- | wc -l
```

- Lists files (`ls -l`), filters for regular files (`grep ^-`), and counts them (`wc -l`).

OR, simpler:

```bash
find . -maxdepth 1 -type f | wc -l
```

- Finds only files (`-type f`) in the current directory (`-maxdepth 1`) and counts them.

### **Using Python**

```python
import os
file_count = len([f for f in os.listdir('.') if os.path.isfile(f)])
print(file_count)
```

- Lists directory contents, checks for files, and counts them.

Choose the method based on your environment. If you need details for a specific OS or tool, let me know!
