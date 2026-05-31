---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 预提交 Pytest Hook 实现摘要
translated: true
type: note
---

以下是摘要：

WHAT WE DID：将 `pytest` 添加为 pre-commit 钩子，使每次 `git commit` 时自动运行测试（约8秒，1860个测试，全部通过）。

PARALLEL TESTS：使用 `pytest-xdist` 测试了 `-n 2`、`-n 4`、`-n auto` 参数。没有性能提升——单个测试太快（每个约4毫秒），并行化的开销无法得到回报。此外，I/O 测试与进程分叉冲突，出现 `Bad file descriptor` 错误。

VERDICT：保持串行。只有当单个测试耗时100毫秒以上（如 API 调用、模型加载）时，并行才会有帮助。不过还是将 `pytest-xdist` 添加到开发依赖中，供未来与较慢的测试套件一起使用。

FILES CHANGED：
- `.pre-commit-config.yaml` — 添加了 `unit-tests` 本地钩子
- `pyproject.toml` — 添加了 `[dependency-groups]`，包含 pytest、pytest-xdist、coverage