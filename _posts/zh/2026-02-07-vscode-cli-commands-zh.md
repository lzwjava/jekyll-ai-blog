---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 精通 VS Code CLI 命令
translated: true
type: note
---

**Question:** 请提供关于 VS Code 的 `code` 命令行选项的全面介绍。

**Answer:**

`code` 命令是 Visual Studio Code 的 **command-line interface (CLI)**。它允许你在 Terminal 或脚本中启动 VS Code、打开文件或文件夹、安装 extensions、对比文件、设置偏好选项等。

### 第一步：使 `code` 在你的 Terminal 中可用

- 在 **macOS** 和 **Linux** 上：打开 VS Code → 按下 `Ctrl+Shift+P` (或 `Cmd+Shift+P`) → 输入 "shell command" → 运行 **Shell Command: Install 'code' command in PATH**。
- 在 **Windows** 上：安装程序通常会自动将其添加到 PATH。如果没有，请手动添加 VS Code 的 bin 文件夹（通常为 `C:\Users\<YourUser>\AppData\Local\Programs\Microsoft VS Code\bin`）。

完成此步骤后，你只需在任何 Terminal 中输入 `code` 即可。

检查是否正常运行：

```bash
code --version
# 或
code -v
```

### 获取完整选项列表

通过运行以下命令，始终可以获得最新的列表：

```bash
code --help
```

这将显示版本、使用示例以及所有当前的 flags（新的 VS Code 版本中会出现新选项）。

### 最常用的选项 (Core CLI Flags)

| Flag / 简写 | 长格式 | 描述 / 典型使用场景 |
|--------------|----------------------------|------------------------------------------------------------------------------------------------|
| `-h`         | `--help`                   | 显示所有可用选项 |
| `-v`         | `--version`                | 显示 VS Code 版本和 commit ID |
| `.`          | (无 flag)                  | `code .` → 打开当前目录 |
| `file.txt`   | (无 flag)                  | `code README.md` → 打开特定文件 |
| `-n`         | `--new-window`             | 强制打开新窗口（即使 VS Code 已经打开） |
| `-r`         | `--reuse-window`           | 强制在最后活动的窗口中打开（当你已经打开 VS Code 时最常用） |
| `-g`         | `--goto`                   | 在特定位置打开文件：`code -g file.py:42:10` (第 42 行，第 10 列) |
| `--diff`     | `--diff file1 file2`       | 在两个文件之间打开 diff editor |
| `-w`         | `--wait`                   | 等待打开的文件关闭后再返回 Terminal（在 git editors 中很有用） |
| `--locale`   | `--locale=zh-cn`           | 强制显示语言 (en, es, zh-cn 等) |
| `--user-data-dir` | `--user-data-dir <path>` | 使用自定义用户数据文件夹（适用于测试 / portable 设置 / 多个实例） |
| `--extensions-dir` | `--extensions-dir <path>` | 自定义 extensions 文件夹 |
| `--disable-extensions` | —                       | 启动时不加载任何 extensions（对排查故障非常有用） |
| `--disable-gpu` | —                       | 禁用硬件加速（有助于解决某些图形/驱动程序问题） |
| `--status`   | `--status`                 | 打印详细的状态信息 |

### 在特定位置打开文件

```bash
# 打开文件并跳转到第 15 行
code main.py:15

# 第 30 行，第 5 列
code src/App.tsx:30:5

# 多个文件 + goto
code -g index.html:10 src/styles.css
```

### 实用日常示例

```bash
# 在新窗口中打开当前文件夹
code . -n

# 在已打开的 VS Code 窗口中打开项目
code ~/projects/my-app -r

# 对比两个文件
code --diff old-version.py new-version.py

# 从 stdin 打开文件（配合管道非常强大）
echo "Hello" | code -

# 等待文件关闭（非常适合作为 git commit message editor）
git config --global core.editor "code --wait"

# 使用特定 profile 打开文件夹
code ~/work/project --profile "Work"

# 故障排除：以纯净状态启动
code --disable-extensions --user-data-dir=/tmp/vscode-test
```

### 从 CLI 管理 Extension

```bash
# 安装 extension
code --install-extension ms-python.python

# 卸载
code --uninstall-extension ms-python.python

# 列出已安装的 extensions
code --list-extensions

# 列出并显示版本号
code --list-extensions --show-versions
```

### 高级 / 较少使用的 Flags (来自 --help)

- `--max-memory=...` — 设置内存限制
- `--telemetry` / `--disable-telemetry`
- `--verbose` — 输出更多日志
- `--log debug|info|warn|error`
- `--profile <name>` — 使用指定的 profile
- `--folder-uri` / `--file-uri` — 使用 URI scheme 打开
- 子命令如 `code tunnel`（用于 remote tunnels）

要获取绝对最新且完整的列表（包括 2025 年之后添加的任何新 flags），请始终运行：

```bash
code --help
```

官方文档页面也会持续更新：

**References:**

- [Command Line Interface (CLI) - Visual Studio Code](https://code.visualstudio.com/docs/editor/command-line)
- [Getting Started: Tips and Tricks (includes CLI examples)](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)
