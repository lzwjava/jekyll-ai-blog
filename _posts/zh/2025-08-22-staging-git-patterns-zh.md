---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 使用Git模式暂存文件
translated: true
type: note
---

### 使用模式匹配暂存 Git 文件

Git 的 `git add` 命令支持文件路径和通配符模式（如 `*.java`）来暂存匹配的文件。您可以运行多个 `git add` 命令来暂存不同的文件集，然后分别提交。这样可以实现选择性暂存以进行分组提交（例如，一个提交用于 Java 文件，另一个用于其余文件）。

#### 基础示例：先暂存并提交 Java 文件
1. **暂存所有 .java 文件**：
   ```bash
   git add "*.java"
   ```
   - 这会暂存当前目录及子目录中所有以 `.java` 结尾的未跟踪或已修改文件。
   - 使用双引号（`"`）可避免在许多系统（如 Bash）中出现 shell 扩展问题。

2. **提交已暂存的 Java 文件**：
   ```bash
   git commit -m "添加 Java 文件"
   ```
   - 此操作仅提交已暂存的文件（Java 文件）。

3. **暂存其余所有文件**：
   ```bash
   git add .
   ```
   - 这会暂存所有剩余的未跟踪/已修改文件（包括当前目录的内容）。

4. **提交剩余文件**：
   ```bash
   git commit -m "添加其他文件"
   ```

- **注意事项**：
  - 首次提交后，`git add .` 不会重新暂存已提交的文件；它仅影响未暂存的更改。
  - 每次执行 add 后检查 `git status` 以验证暂存内容。
  - 如果存在嵌套目录，`*.java` 会匹配任意深度的文件。

#### 处理排除项或更多模式
如果您需要实现类似包含 `*.java` 但排除其他文件的单步操作，Git 的 `git add` 不支持直接否定模式（如 `"!*.java"` 在 Git 命令中无效）。请改用上述多次 `git add` 调用，或：

- 使用具体路径：`git add file1.txt file2.md` 进行手动选择。
- 高级排除方案：临时使用 `.gitignore` 隐藏文件，添加目标文件后恢复 `.gitignore`。或使用 `git add -A`（添加所有内容）配合选择性暂存。
- 交互式暂存：`git add -p` 进行代码块逐项暂存。
- 预览更改：`git add --dry-run "*.java"` 显示将会暂存的文件（但不实际执行）。

#### 分离提交技巧
- 提交前始终使用 `git diff --cached` 复查更改。
- 大型仓库中可考虑使用 `git add --all` 或 `git add -A` 一次性暂存所有更改，再通过 `git reset HEAD <文件>` 选择性取消暂存。
- 若模式不生效，请确认使用了引号且您的 shell 支持通配符（如在 Windows 中请使用 Git Bash）。关于大小写敏感度，Git 遵循系统设置（参见 `core.ignorecase`）。

如果这与您的需求不符（例如您需要类似 `.gitignore` 的排除模式），请提供更多细节！
