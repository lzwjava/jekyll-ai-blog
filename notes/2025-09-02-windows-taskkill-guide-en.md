---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows Taskkill Command Guide
translated: false
type: note
---

In Windows, `taskkill` is a built-in command-line tool you can use to stop (kill) processes by their **process ID (PID)** or **image name (executable name)**.

### Basic Syntax

```bat
taskkill /PID <process_id> [/F]
taskkill /IM <image_name> [/F]
```

* `/PID <process_id>` → Kill by process ID.
* `/IM <image_name>` → Kill by process name (e.g., `notepad.exe`).
* `/F` → Forcefully terminate the process.
* `/T` → Kill the specified process and all child processes.

---

### Examples

1. **Kill a process by PID:**

```bat
taskkill /PID 1234
```

This will try to stop the process with PID 1234.

2. **Force kill a process by PID:**

```bat
taskkill /PID 1234 /F
```

3. **Kill a process by name:**

```bat
taskkill /IM notepad.exe
```

4. **Force kill by name:**

```bat
taskkill /IM notepad.exe /F
```

5. **Kill a process and its children:**

```bat
taskkill /IM cmd.exe /T /F
```

---

### Finding the PID

If you don’t know the PID:

```bat
tasklist
```

This lists all running processes with their PIDs. You can then use `taskkill /PID` on the right one.

---

⚠️ **Notes**

* Some system processes can’t be killed.
* You may need to run Command Prompt as **Administrator** to terminate protected processes.

---

Do you want me to also show you how to combine `tasklist` and `taskkill` in one command (e.g., kill all processes matching a name automatically)?
