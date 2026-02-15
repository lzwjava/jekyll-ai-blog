---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI 代码更改的 Git 状态
translated: true
type: note
---

Question: 在与 Claude 或 Codex 等 coding assistants 协作时，运行 "git status" 的用途和好处是什么，特别是在处理已修改（modified）和未跟踪（untracked）文件的情况下？

Answer: 

是的 —— 使用 `git status` 是快速了解 **coding assistant（如 Claude, Cursor, Windsurf, Aider, Codex 等）在你的项目中实际修改了什么** 最有效且轻量的方法之一。

### 使用 AI coding assistants 时的典型 workflow

1. 你要求 AI 实现一个 feature / 修复一个 bug / 进行 refactor 等。
2. assistant 通常会：
   - 在 chat 中编写代码 → 你手动 copy-paste
   - 直接编辑文件（IDE 中的 Claude, Cursor, Aider, continuedev 等）
3. 在 AI 完成任务后 → **立即** 运行：

```bash
git status
# 或者更简短的
git st
# 甚至
git diff --stat
```

这能为你提供即时的可见性：

| git status 显示的内容          | 在 AI coding 语境下的含义                                 | 常见的下一步操作                          |
|-------------------------------|---------------------------------------------------------------|---------------------------------------------|
| `modified: path/to/file.py`   | AI 修改了现有文件                                      | 使用 `git diff path/to/file.py` 进行 review        |
| `Untracked files: scripts/...`| AI 创建了新文件                                        | 如果正确则执行 `git add`，若不需要则执行 `rm`      |
| `deleted: oldfile.js`         | AI 删除了文件（有时是误删）                       | `git restore --staged` 或 `git rm --cached` |
| nothing to commit, working tree clean | AI 没有进行文件更改（可能只在 chat 中输出了代码）    | 检查 chat / terminal 输出                |

### 你的具体示例

```
Changes not staged for commit:
  modified: .claude/settings.local.json

Untracked files:
  scripts/clash/clash_select_provider.py
```

解读：

- Claude（或基于 Claude 的工具）极有可能 **修改了它自己的 config** → `.claude/settings.local.json`（非常常见）。
- Claude / 你 / 其他工具 **创建了一个新的 Python script** → `scripts/clash/clash_select_provider.py`。

因此，验证新脚本是否工作的最快方式是：

```bash
# 查看创建的内容
cat scripts/clash/clash_select_provider.py

# 或者在编辑器中打开
code scripts/clash/clash_select_provider.py     # VS Code
nvim scripts/clash/clash_select_provider.py     # Neovim

# 运行及测试
python scripts/clash/clash_select_provider.py
# 或者
python3 scripts/clash/clash_select_provider.py
# 如果需要，带上参数运行
python scripts/clash/clash_select_provider.py --help
```

### 推荐的 AI 完成工作后的 10 秒检查清单

```bash
git status -s          # 紧凑视图
git diff --stat        # 更改摘要
git diff               # 如果你想查看所有细节（内容多时可能较乱）
```

然后做出决定：

- 更改正确 → `git add . && git commit -m "feat: add clash provider selector (Claude)"`
- 更改错误 → `git restore .` 或 `git restore --staged .` 甚至 `git reset --hard`（请谨慎！）
- 只要部分文件 → `git add scripts/clash/clash_select_provider.py`

所以，当你频繁使用 AI assistants 编写或修改代码时，`git status` 可能是 **最有价值的 5 个字符命令**。

References:  

- 无需针对此 git 用法说明提供参考文献。