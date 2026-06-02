---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 并行 Git 更新提升性能
translated: true
type: note
---

完成。以下是摘要：

```
Before (sequential):  22.1s for 5 repos
After  (8 workers):    4.8s for 5 repos  → 4.6x speedup
```

对于你的 62 个仓库更新：

- 顺序执行：约 4.5 分钟（每个仓库约 4.4 秒）
- 并行 -j8：约 35 秒（62 × 4.4 秒 ÷ 8 个 worker）

所做的更改：

1. `ww/git/git_update.py` — 添加了 `ThreadPoolExecutor` 及 `--jobs/-j` 选项（默认 8）。通过 `as_completed()` 实现并行 git pull。原有的 12 个测试全部通过。

2. `~/.zsh/completions/_ww` — 为 `projects update --jobs/-j/--category/-c/--list` 添加了命令补全。

用法：

```
ww projects update              # 所有仓库，8 个 worker（默认）
ww projects update -j16         # 更激进
ww projects update -j1          # 顺序执行（旧行为）
ww projects update @ai          # 按类别筛选 + 并行
ww projects update pytorch llama.cpp  # 指定仓库 + 并行
```

瓶颈在于网络 I/O（git fetch），因此线程是合适的工具——无需使用多进程。每个线程几乎全部时间都在等待 SSH/HTTPS 套接字，因此 8-16 个 worker 可以很好地饱和网络链路而不会产生争用。
