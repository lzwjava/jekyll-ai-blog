---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 同时进行 Git 推送导致的竞态条件错误
translated: true
type: note
---

Question: 为什么在打开两个窗口/Terminal 执行 `git add -A`、`git commit` 和 `git push` 时会出现错误 "! [remote rejected] main -> main (cannot lock ref 'refs/heads/main': is at b2c0835c1c7c14323a162a90e17f8a78145e3f0a but expected 59383ebd13b30aab988c8eefcc0f64f103f0f44d)"？

Answer:

出现这个错误是因为 **两个 Git 进程尝试在几乎同一时间更新远程服务器上相同的 branch reference (`refs/heads/main`)**，从而导致了竞态条件 (race condition)。

### 逐步分析实际发生的过程

1. 你在 **同一个本地 repository** 中打开了 **两个 Terminal 窗口**。
2. 在两个窗口中你都运行了：
   - `git add -A`
   - `git commit` → 由于 working tree 和 index 通常是共享的，两者由于提交时间或内容微差会生成 **两个不同的 commits**。
   - `git push` (或 `git push origin main`)

由于文件系统 (index + working tree) 在两个 Terminal 之间是共享的：

- 两个 commit 通常在本地都能成功（它们只是创建了两个不同的 commit objects）。
- 但当两者几乎同时尝试执行 `git push` 时：

  Git push 协议流程（简化版）：
  - Client 询问 Server：“main 分支当前的 tip 是什么？”
  - Server 回复：例如 `59383ebd...`
  - Client 说：“我想将 main 从 `59383ebd...` fast-forward 到我的新 commit `b2c0835c...`。”
  - Server 检查：“main 还在 `59383ebd...` 吗？”
    → 如果 **另一个 push 已经抢先成功**，main 现在已经指向了不同的 hash → Server 拒绝并报错：

    ```
    cannot lock ref 'refs/heads/main': is at b2c0835c... but expected 59383ebd...
    ```

这本质上就是两个 push 操作之间的 **race condition**。

### 在你的场景中最常见的原因

- 你在窗口 1 运行 `git commit && git push`（或拆分运行）。
- 几乎同一时刻，你在窗口 2 做了同样的操作。
- 窗口 1 赢得了竞赛 → push 成功。
- 窗口 2 发现远程分支已经移动 → 收到 “is at … but expected …” 的拒绝信息。

### 如何避免

- **切勿** 在同一个 repo 的两个 Terminal 中同时运行 `git commit` 或 `git push`。
- 只使用 **一个 Terminal** 进行 commit 和 push。
- 如果你确实需要并行工作：
  - 在每个 Terminal 中操作 **不同的 branches**。
  - 或者只用一个 Terminal 负责 commit + push，第二个 Terminal 仅用于查看 logs / diff / status。

### 看到此错误时的快速恢复方法

通常只需运行：

```bash
git pull --rebase    # 或 git pull --autostash
git push
```

这会让你的本地分支保持最新，然后再 push 你的新 commit。

### 总结

该错误 **并非数据损坏** —— 它是 Git 保护远程分支免受并发冲突更新的一种机制。
它的发生正是 **因为你几乎同时从两个 Terminal 发起了 push**。

References:

- <https://stackoverflow.com/questions/11796580/git-pull-error-error-remote-ref-is-at-but-expected>
- <https://graphite.com/guides/git-error-cannot-lock-ref>
- <https://stackoverflow.com/questions/12416643/notorious-git-error-remote-rejected-failed-to-lock>
