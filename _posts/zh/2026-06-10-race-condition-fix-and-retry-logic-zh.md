---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 竞态条件修复与重试逻辑
translated: true
type: note
---

修复已应用。以下是摘要：

---

**失败内容：** 运行 `27260998201`（部署 Jekyll，2026-06-10 07:39 UTC）

**失败位置：** “Lint Markdown files” 步骤 — 提交了 `chore(lint): Fix markdown lint issues`，随后推送被拒绝两次。

**根本原因：** 竞态条件。该工作流有 4 个独立的提交+推送步骤（语言更新、笔记翻译、表格修复、lint）。每个步骤都使用了这种脆弱模式：

```
git push || { git pull --rebase; git push; }
```

当另一个并发运行在 rebase 和第二次推送之间执行推送时，会导致失败且无法恢复。这次 lint 步骤不幸中招。

**修复内容：** 将全部 4 个推送块替换为一个 `push_with_retry()` 函数，该函数最多重试 3 次，每次重试时执行 `git pull --rebase`，并在尝试之间等待 2 秒：

```bash
push_with_retry() {
  for attempt in 1 2 3; do
    git push && return 0
    echo "推送失败（尝试 $attempt/3），正在拉取并变基..."
    git pull --rebase || true
    sleep 2
  done
  echo "3 次尝试后推送失败"
  return 1
}
```

---

**附注：** 还有一条弃用警告 — `actions/checkout@v4` 和 `actions/setup-python@v4` 运行在 Node.js 20 上，从 2026 年 6 月 16 日（6 天后）起将强制使用 Node.js 24。如果可用，建议升级到 `actions/checkout@v5` 和 `actions/setup-python@v5`，或者设置 `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true` 以提前选择。

需要我提交并推送此修复吗？