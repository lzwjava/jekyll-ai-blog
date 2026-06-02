---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Git Check-Ignore 命令详解
translated: true
type: note
---

### 什么是 `git check-ignore`？

`git check-ignore` 是 Git 的一个工具命令，用于判断特定文件或路径是否被 Git 的忽略机制（如 `.gitignore` 文件、`.git/info/exclude` 或全局忽略文件）所忽略。该命令在调试文件未被跟踪或未添加到仓库的原因时特别有用。

如果路径被忽略，该命令会输出路径（并可选择显示匹配模式）。如果未被忽略，则无输出（退出码为 0）。这一特性使其易于在自动化脚本中使用。

### 基本用法

通过指定一个或多个路径来运行该命令：

```
git check-ignore <路径名>...
```

- **示例**：检查单个文件是否被忽略：
  ```
  git check-ignore 路径/到/我的文件.txt
  ```
  - 输出：若被忽略，则打印 `路径/到/我的文件.txt`；若未被忽略，则无输出。

- **示例**：检查多个文件：
  ```
  git check-ignore 文件1.txt 文件2.txt 目录/文件3.txt
  ```
  - 仅输出被忽略的路径，每行一个。

### 主要选项

| 选项 | 描述 | 示例 |
|------|------|------|
| `-v`, `--verbose` | 显示匹配的忽略模式（例如来自 `.gitignore` 的某一行）。 | `git check-ignore -v 路径/到/我的文件.txt`<br>输出：`路径/到/我的文件.txt: .gitignore:1:*.txt`（路径 + 文件:行号:模式） |
| `-q`, `--quiet` | 抑制输出，但仍使用退出码（0 表示未被忽略，1 表示被忽略）。适用于脚本。 | `git check-ignore -q 路径/到/我的文件.txt`<br>（无输出；通过 `$?` 检查退出码） |
| `--stdin` | 从标准输入读取路径，而非命令行参数。 | `echo "文件1.txt\n文件2.txt" \| git check-ignore --stdin` |
| `--non-matching` | 反转输出：显示*未被*忽略的路径。 | `git check-ignore --non-matching -v 文件1.txt 文件2.txt` |

### 常见使用场景

1. **调试 `.gitignore` 规则**：
   - 如果 `git status` 未显示你预期的文件，可运行 `git check-ignore -v <文件>` 来查看具体是哪条规则忽略了它。
   - 示例输出：`src/logs/app.log: .gitignore:5:logs/*`（表示 `.gitignore` 第 5 行的规则匹配）。

2. **在脚本中使用**：
   - 检查文件是否应被添加：
     ```
     if git check-ignore -q 我的文件.txt; then
         echo "文件被忽略，跳过..."
     else
         git add 我的文件.txt
     fi
     ```

3. **批量检查**：
   - 列出目录中所有被忽略的文件：
     ```
     find . -type f -print0 | xargs -0 git check-ignore
     ```

### 提示
- 该命令遵循 Git 的忽略规则栈：本地 `.gitignore`、全局排除规则等。
- 对未跟踪的文件或已存在于仓库中的文件均有效（但会检查忽略规则）。
- 更多详细信息，请参阅官方文档。

[Git check-ignore 文档](https://git-scm.com/docs/git-check-ignore)
[Stack Overflow：Git 命令显示哪些特定文件被忽略](https://stackoverflow.com/questions/466764/git-command-to-show-which-specific-files-are-ignored-by-gitignore)
[使用 git check-ignore 调试 .gitignore](https://alexwlchan.net/til/2020/using-git-check-ignore-to-debug-your-gitignore/)
