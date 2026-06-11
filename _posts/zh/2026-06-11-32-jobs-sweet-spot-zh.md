---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 32个工作的甜蜜点
translated: true
type: note
---

```
Jobs    Time     Speedup
────    ────     ───────
 8      24.1s    1.0x (基准)
 32      9.9s    2.4x  ← 新默认值
 64      9.6s    2.5x  (收益递减)

**32 是最佳值。** 64 相比 32 仅节省 0.3 秒——不值得增加连接压力。

修改内容：
1. `ww/git/git_update.py` — 默认 jobs 从 8 改为 32
2. `git config --global submodule.fetchJobs 4` — 并行子模块拉取
3. `git config --global http.postBuffer 524288000` — 为大型仓库设置 500MB 缓冲区

您仍可在每次运行时覆盖：`ww projects update -j 64` 或 `ww projects update -j 16`。

另外：那个失败的 1 个仓库——需要我检查是哪一个吗？
```