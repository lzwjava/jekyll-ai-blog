---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为可重现性提交uv.lock文件
translated: true
type: note
---

不——`uv.lock` 应该**提交**到版本控制，而不是被 `.gitignore` 忽略。原因如下：

**`uv.lock` 的作用：**
它锁定了所有依赖（包括传递依赖）的*确切*解析版本，确保每个开发者和 CI 环境获得完全一致的安装结果。`uv sync` 读取锁定文件；`uv pip compile` 根据 `pyproject.toml` 生成它。

**为什么应该提交它：**

1. **可重现性** — 如果没有它，在不同机器或不同时间运行 `uv sync` 时，如果有任何包发布了新版本，解析出的版本可能不同。这会导致“在我机器上能跑”的 bug。
2. **安全性** — 你能确切知道生产环境中运行的代码是什么。不会有意外的传递依赖版本提升。
3. **可审查的变更** — 更新依赖的 PR 会显示锁定文件的具体差异，便于审计变更内容。

**经验法则（与 `Cargo.lock`、`poetry.lock`、`package-lock.json` 相同）：**

- **库项目**（发布的包）：有时可以忽略锁定文件，因为使用者会自行解析依赖。
- **应用程序**（你的 CLI 工具、服务、脚本）：始终提交锁定文件。

你的项目属于应用程序。请提交 `uv.lock`。

如果你当前将其放在 `.gitignore` 中，只需移除它：

```bash
# 如果存在于 .gitignore 中则移除，然后跟踪它
git rm --cached uv.lock  # 如果之前被忽略但已存在
# 然后从 .gitignore 中删除 uv.lock 这一行
```

uv 文档明确推荐这样做：<https://docs.astral.sh/uv/concepts/projects/layout/#lockfile>
