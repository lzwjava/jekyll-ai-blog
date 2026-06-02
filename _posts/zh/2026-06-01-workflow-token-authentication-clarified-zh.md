---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 工作流令牌认证说明
translated: true
type: note
---

一切正常。`ww action` 刚刚成功执行并触发了工作流。

这个错误并不是由你从 SSH 切换到 HTTPS 引起的。实际情况如下：

1. `ww action` 底层使用的是 `gh workflow run`（`gh` CLI），它使用存储在 macOS 钥匙串中自己的 OAuth token——与 SSH 密钥或 `GITHUB_PAT_TOKEN` 完全无关。

2. 当省略 `--ref` 参数时，`gh` 会调用 GitHub 的 GraphQL API 来确定仓库的默认分支。那次调用返回了 401 Bad credentials——这是一个临时的认证问题（可能是 token 刷新竞争、GitHub API 临时故障，或者是通过 mihomo 的代理异常）。

3. 当时以及现在你的 `gh auth status` 都是正常的。现在无需任何改动就能正常运行。

为了避免将来出现此类问题，你可以固定 ref 参数，这样 `gh` 就不需要查询默认分支了：

```bash
ww action gh-pages.yml --ref main
```

另外请注意：`GITHUB_PAT_TOKEN`（用于 `ww github` 命令的 GraphQL 调用）在 REST 下可用，但在 GraphQL 下会失败。这是另一个问题——你的 PAT 很可能缺少 GraphQL 所需的权限。`gh` CLI 的 token 对两者都有效。如果你希望 `ww github` 命令也能正常工作，你需要用适当的权限重新生成 PAT，或者让 `github_mgmt.py` 回退到使用 `gh auth token`。
