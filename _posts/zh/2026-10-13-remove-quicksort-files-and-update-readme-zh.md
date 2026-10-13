---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 移除快速排序文件并更新README
translated: true
type: note
---

已完成。

**已移除：**

- `Quicksort.java`
- `quicksort.py`

**同时更新了** `README.md` —— 删除了 "quicksort benchmarks" 介绍句和整个 "Quick Sort Benchmarks" 部分，因为该部分指向的文件已不存在。

当前工作树状态：

```
 D Quicksort.java
 D quicksort.py
 M README.md
 M src/main.rs        （之前的 Ctrl+C 退出修改）
```

尚未提交任何更改 — 如果你需要我提交这些更改，请告诉我（例如 `chore: remove quicksort benchmarks and update README`，外加一个单独的提交用于 Ctrl+C 修复），或者是否需要添加 `cargo run -- bench`（一个 Rust 快速排序），因为 Rust 版本从未存在于 `src/` 中。
