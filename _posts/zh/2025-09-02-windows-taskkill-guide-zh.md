---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows任务终止命令指南
translated: true
type: note
---

在 Windows 系统中，`taskkill` 是一个内置命令行工具，可用于通过**进程 ID (PID)** 或**映像名称（可执行文件名）**来终止进程。

### 基础语法

```bat
taskkill /PID <进程ID> [/F]
taskkill /IM <映像名称> [/F]
```

* `/PID <进程ID>` → 通过进程 ID 终止进程
* `/IM <映像名称>` → 通过进程名称终止进程（例如 `notepad.exe`）
* `/F` → 强制终止进程
* `/T` → 终止指定进程及其所有子进程

---

### 使用示例

1. **通过 PID 终止进程：**

```bat
taskkill /PID 1234
```

此命令将尝试终止 PID 为 1234 的进程。

2. **通过 PID 强制终止进程：**

```bat
taskkill /PID 1234 /F
```

3. **通过进程名终止进程：**

```bat
taskkill /IM notepad.exe
```

4. **通过进程名强制终止：**

```bat
taskkill /IM notepad.exe /F
```

5. **终止进程及其子进程：**

```bat
taskkill /IM cmd.exe /T /F
```

---

### 查找进程 PID

若不清楚进程 PID：

```bat
tasklist
```

该命令将列出所有运行中的进程及其 PID，随后即可对目标进程使用 `taskkill /PID` 命令。

---

⚠️ **注意事项**

* 部分系统进程无法被终止
* 终止受保护进程时可能需要以**管理员身份**运行命令提示符

---

需要我演示如何将 `tasklist` 和 `taskkill` 组合使用吗（例如自动终止所有匹配指定名称的进程）？
