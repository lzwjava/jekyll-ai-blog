---
audio: false
generated: true
lang: zh
layout: post
title: 保留目录结构复制文件
translated: true
type: note
---

根据你的 `find` 命令输出，你希望将所有 `.log` 文件复制到 `/Users/lzwjava/projects/logs` 并保留它们的目录结构。例如，像 `./CoreSimulator/FC275C39-59CC-4483-A64E-5D459D7A1D57/system.log` 这样的文件应该最终出现在 `/Users/lzwjava/projects/logs/CoreSimulator/FC275C39-59CC-4483-A64E-5D459D7A1D57/system.log`。我将展示如何使用 `find` 结合 `cp` 或 `rsync` 来实现这一目标，确保目录层次结构得以保留。

---

### **解决方案 1：使用 `find` 和 `cp`**
你可以使用 `find` 来定位 `.log` 文件，并使用带有 `--parents` 选项的 `cp` 来复制它们，同时保留它们的目录结构。

#### **命令**
```bash
find . -name "*.log" -exec cp --parents {} /Users/lzwjava/projects/logs \;
```

#### **解释**
- **`find . -name "*.log"`**：定位当前目录及其子目录中的所有 `.log` 文件（如你的示例所示）。
- **`-exec cp --parents {} /Users/lzwjava/projects/logs \;`**：
  - `cp --parents`：复制文件并在目标位置重新创建其相对于源目录（`.`）的目录路径。
  - `{}`：`find` 找到的每个文件的占位符。
  - `/Users/lzwjava/projects/logs`：目标目录。
  - `\;`：终止 `-exec` 命令。

#### **结果**
- `./CoreSimulator/FC275C39-59CC-4483-A64E-5D459D7A1D57/system.log` → `/Users/lzwjava/projects/logs/CoreSimulator/FC275C39-59CC-4483-A64E-5D459D7A1D57/system.log`
- `CoreSimulator` 下的目录结构得以保留。

#### **运行前准备**
- 确保 `/Users/lzwjava/projects/logs` 目录存在：
  ```bash
  mkdir -p /Users/lzwjava/projects/logs
  ```

---

### **解决方案 2：使用 `rsync`**
`rsync` 是另一个强大的工具，可以在复制文件时保留目录结构，并且对于批量操作通常更高效。

#### **命令**
```bash
find . -name "*.log" -exec rsync -R -a {} /Users/lzwjava/projects/logs \;
```

#### **解释**
- **`-R`**：使用相对路径，保留源目录（`.`）的目录结构。
- **`-a`**：归档模式（保留时间戳、权限等）。
- `{}`：找到的每个 `.log` 文件。
- `/Users/lzwjava/projects/logs`：目标目录。

#### **结果**
与上述相同——文件连同其完整的相对路径一起被复制。

#### **运行前准备**
- 如果目标目录不存在，请创建它：
  ```bash
  mkdir -p /Users/lzwjava/projects/logs
  ```

---

### **验证复制结果**
运行任一命令后，检查目标目录：
```bash
ls -R /Users/lzwjava/projects/logs
```
你应该看到：
```
/Users/lzwjava/projects/logs:
CoreSimulator

/Users/lzwjava/projects/logs/CoreSimulator:
CoreSimulator.log  FC275C39-59CC-4483-A64E-5D459D7A1D57  Simulator.log

/Users/lzwjava/projects/logs/CoreSimulator/FC275C39-59CC-4483-A64E-5D459D7A1D57:
com.apple.itunesstored  system.log

/Users/lzwjava/projects/logs/CoreSimulator/FC275C39-59CC-4483-A64E-5D459D7A1D57/com.apple.itunesstored:
itunesstored.log
```

---

### **关键注意事项**
- **权限**：确保你对 `/Users/lzwjava/projects/logs` 有写入权限。如果没有，请使用 `sudo`（例如 `sudo cp ...`）或调整权限：
  ```bash
  chmod -R u+w /Users/lzwjava/projects/logs
  ```
- **覆盖**：如果目标位置已存在文件：
  - `cp` 会直接覆盖，不发出警告。
  - `rsync -a` 也会覆盖，但你可以添加 `--ignore-existing` 来跳过已存在的文件：
    ```bash
    find . -name "*.log" -exec rsync -R -a --ignore-existing {} /Users/lzwjava/projects/logs \;
    ```
- **试运行（先测试）**：
  - 对于 `cp`，添加 `echo` 来预览：
    ```bash
    find . -name "*.log" -exec echo cp --parents {} /Users/lzwjava/projects/logs \;
    ```
  - 对于 `rsync`，使用 `--dry-run`：
    ```bash
    find . -name "*.log" -exec rsync -R -a --dry-run {} /Users/lzwjava/projects/logs \;
    ```

---

### **选择哪种方法？**
- **`cp`**：更简单，不需要额外工具（所有类 Unix 系统都可用）。
- **`rsync`**：更灵活（例如，用于同步、跳过重复文件），但需要安装 `rsync`（大多数系统已标配）。

两种方法都适用于你的情况。为求简单，我建议从 `cp --parents` 开始。

---

### **最终命令（推荐）**
```bash
mkdir -p /Users/lzwjava/projects/logs
find . -name "*.log" -exec cp --parents {} /Users/lzwjava/projects/logs \;
```

从你的 `Logs` 目录（`lzwjava@anonymous Logs %`）运行此命令即可！如果你遇到任何问题或想要调整行为（例如，改为扁平化结构），请告诉我。
