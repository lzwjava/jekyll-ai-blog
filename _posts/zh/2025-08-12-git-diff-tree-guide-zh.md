---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Git Diff-Tree 使用指南
translated: true
type: note
---

这是一份实用的端到端 `git diff-tree` 指南——包括它的功能、使用时机以及实际工作中真正会用到的选项。我将避免使用大型表格，专注于提供可直接复制的示例说明。

# `git diff-tree` 的实际功能

* 它比较**树对象**。在日常使用中通常表示：“显示**提交**与其父提交相比发生了哪些变化。”
* 它是**底层命令**（适合脚本编写），不同于面向用户的 `git show`/`git log`（高层命令）。
* 它从不查看工作目录，仅比较存储在仓库中的树对象（提交、指向提交的标签或原始树ID）。

# 你会用到的基本形式

1. 将提交与其父提交进行比较

```bash
git diff-tree -p <commit>
```

如果 `<commit>` 有一个父提交，你会看到常规补丁。如果是合并提交，除非特别要求（见下文），否则不会显示任何内容。

2. 显式比较两个树对象/提交

```bash
git diff-tree -p <旧树对象或提交> <新树对象或提交>
```

当你想要比较任意两个时间点，而不仅仅是“提交与父提交”时非常有用。

3. 仅显示文件名（无补丁）

```bash
git diff-tree --name-only -r <commit>
```

添加 `-r` 可递归到子目录，从而获得扁平列表。

4. 显示带变更类型的文件名

```bash
git diff-tree --name-status -r <commit>
# 输出类似以下内容：
# A 路径/到/新文件
# M 路径/到/修改的文件
# D 路径/到/删除的文件
```

5. 显示补丁（完整差异）

```bash
git diff-tree -p <commit>            # 类似 `git show` 的统一差异格式
git diff-tree -U1 -p <commit>        # 较少的上下文（1行）
```

# 必须了解的选项（含原因/时机）

* `-r` — 递归到子树中，以便查看所有嵌套路径。不使用此选项时，发生变更的目录可能仅显示为单行。
* `--no-commit-id` — 在编写按提交输出的脚本时，抑制“commit <sha>”标头。
* `--root` — 当提交**没有父提交**（初始提交）时，仍显示其与空树的差异。
* `-m` — 对于合并提交，显示**与每个父提交的差异**（生成多个差异）。
* `-c` / `--cc` — 组合合并差异。`--cc` 是一种优化视图（`git show` 用于合并提交的显示方式）。
* `--name-only` / `--name-status` / `--stat` / `--numstat` — 不同的摘要样式。`--numstat` 对脚本友好（添加/删除的行数统计）。
* `--diff-filter=<集合>` — 按变更类型筛选，例如 `--diff-filter=AM`（仅添加或修改）；常用字母：`A`dd（添加）、`M`odified（修改）、`D`eleted（删除）、`R`enamed（重命名）、`C`opied（复制）、`T`ype changed（类型更改）。
* `-M` / `-C` — 检测重命名和复制。可添加相似度阈值，例如 `-M90%`。
* `--relative[=<路径>]` — 将输出限制在子目录内；不带参数时，使用当前工作目录。
* `-z` — 使用 **NUL 终止符** 处理路径，以便进行明确的机器解析（处理文件名中的换行符或制表符）。
* `--stdin` — 从标准输入读取提交列表（或提交对）。这是实现快速批量操作的秘诀。

# 规范的脚本模式

### 1) 列出单个提交中更改的文件

```bash
git diff-tree --no-commit-id --name-status -r <commit>
```

### 2) 批量处理多个提交（快速！）

```bash
git rev-list main --since="2025-08-01" |
  git diff-tree --stdin -r --no-commit-id --name-status
```

`--stdin` 避免了为每个提交生成 `git` 进程，对于大范围操作速度更快。

### 3) 仅显示目录中的添加和修改

```bash
git diff-tree -r --no-commit-id --name-status \
  --diff-filter=AM <commit> -- src/backend/
```

### 4) 统计每个文件添加/删除的行数（脚本友好）

```bash
git diff-tree -r --no-commit-id --numstat <commit>
# 输出："<添加行数>\t<删除行数>\t<路径>"
```

### 5) 检测并显示提交中的重命名

```bash
git diff-tree -r --no-commit-id -M --name-status <commit>
# 输出类似："R100 旧/名称.txt\t新/名称.txt"
```

### 6) 合并提交的补丁

```bash
git diff-tree -m -p <合并提交>     # 按父提交显示补丁
git diff-tree --cc <合并提交>      # 组合视图（单个补丁）
```

### 7) 初始提交（无父提交）

```bash
git diff-tree --root -p <初始提交>
```

# 理解原始记录格式（如需手动解析）

使用 `--raw`（某些模式隐式使用）获取最小化、稳定的记录：

```
:100644 100644 <旧sha> <新sha> M<TAB>路径
```

* 数字是文件模式：`100644` 常规文件，`100755` 可执行文件，`120000` 符号链接，`160000` gitlink（子模块）。
* 状态是单个字母（`A`、`M`、`D` 等），可能带有分数（例如 `R100`）。
* 对于重命名/复制，你会看到两个路径。使用 `-z` 时，字段以 NUL 分隔；不使用 `-z` 时，以制表符分隔。

**提示：** 如果你正在构建可靠的工具，请始终传递 `-z` 并按 NUL 分割。存在包含换行符的文件名。

# 比较 `git diff-tree` 与相关命令（以便选择正确的命令）

* `git diff`：比较**索引/工作树**与 HEAD 或任意两个提交/树；用于交互式开发。
* `git show <commit>`：一个美观的包装器，用于“与父提交的差异 + 元数据”。非常适合人类阅读。
* `git log -p`：历史记录加补丁。对于范围比较，通常比手动循环 `diff-tree` 更方便。
* `git diff-tree`：用于**精确、可编写脚本的按提交差异**的底层命令，可通过 `--stdin` 进行批处理。

# 实际示例

### “这个 PR 合并提交中更改了什么？”

```bash
git diff-tree --cc <合并提交> | less
```

如果需要按父提交查看详细信息：

```bash
git diff-tree -m -p <合并提交> | less
```

### “为 CI 步骤提供最新提交修改的文件列表”

```bash
git diff-tree --no-commit-id --name-only -r HEAD > changed.txt
```

### “最近 20 次提交中仅添加或修改的 Java 文件”

```bash
git rev-list -n 20 HEAD |
  git diff-tree --stdin -r --no-commit-id --name-only --diff-filter=AM |
  grep -E '\.java$'
```

### “统计发布标签间的代码变动（添加/删除的行数）”

```bash
git diff-tree -r --no-commit-id --numstat v1.2.0..v1.3.0
```

### “安全处理奇怪的文件名”

```bash
git diff-tree -z -r --no-commit-id --name-status <commit> |
  awk -v RS='\0' 'NR%2{status=$0; next}{printf "%s %s\n", status, $0}'
```

# 性能注意事项

* 对于大范围操作，优先使用 `--stdin` 与 `git rev-list`；这可以避免进程频繁创建。
* 当不需要行级变更时，跳过补丁（使用 `--name-only`/`--name-status`）。
* 如果更关心速度而非准确性，请避免使用重命名检测（`-M`、`-C`）。

# 注意事项与边界情况

* **默认情况下，合并提交无输出。** 你必须传递 `-m`（按父提交）或 `--cc`/`-c`（组合视图）。
* **初始提交是“空树 vs 树”。** 使用 `--root` 强制显示差异。
* **子模块** 显示模式 `160000` 和一个 SHA（gitlink）。除非在子模块仓库内部进行差异比较，否则不会看到内部差异。
* **路径规范放在 `--` 之后。** 如果按路径筛选，请将它们放在 `--` 之后以避免歧义。
* **文件名包含空格/换行符。** 如果要进行解析，请始终添加 `-z`。

# 可直接复用的“速查代码片段”

```bash
# 更改的文件（扁平列表）
git diff-tree --no-commit-id --name-only -r <commit>
```
