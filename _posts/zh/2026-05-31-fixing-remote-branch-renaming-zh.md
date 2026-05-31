---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复远程分支重命名
translated: true
type: note
---

已修复。以下是总结：

  故障仓库：/Users/lzwjava/projects/rust (rust-lang/rust)
  根本原因：远程仓库将默认分支从 `master` 重命名为 `main`
               你的本地 `master` 跟踪的 `origin/master` 已不存在，
               且 fetch 的 refspec 被硬编码为仅 `master`。

  修复内容：
    1. 本地分支重命名：    master → main
    2. 修复 fetch refspec：+refs/heads/master:... → +refs/heads/*:refs/remotes/origin/*
    3. 浅获取 origin/main（仓库约 3GB，完整获取会超时）
    4. 设置上游跟踪：   main → origin/main

  当前状态：正在跟踪 origin/main（因浅获取导致领先 168 个提交，落后 1 个提交）。

注意：下次对此仓库执行完整的 `git pull` 可能会花费较长时间（rust-lang/rust 仓库很大）。如果不需要完整历史，使用 `git pull --depth=1` 或 `git fetch --depth=1` 会更快。