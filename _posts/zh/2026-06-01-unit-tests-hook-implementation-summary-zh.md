---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 单元测试钩子实现总结
translated: true
type: note
---

一切正常。单元测试钩子已生效。以下是总结：

**新增内容：**

1. `.pre-commit-config.yaml` — 末尾新增 `unit-tests` 本地钩子  
   - 运行命令：`uv run python -m pytest tests/ -x -q --tb=short`  
   - `-x` 表示首次失败即停止（快速反馈）  
   - `-q` 表示静默输出  
   - `--tb=short` 表示简短回溯信息  
   - `always_run: true` 表示每次提交都运行，无论哪些文件变更

2. `pyproject.toml` — 新增 `[dependency-groups]`，将 `pytest` 和 `coverage` 列为开发依赖  
   - 现在执行 `uv sync` 会自动安装它们

**性能：** 1707 通过，153 跳过，耗时约 8 秒。对每次提交来说可以接受。

**注意：** 其他已有的钩子失败（ruff E741、pyright 缺失导入、bandit 参数错误）与本变更无关——它们在此之前就已存在。单元测试钩子本身干净通过。

如果 8 秒日后感觉太慢，可以添加 `stages: [pre-push]` 将其移至仅推送前执行，或添加 `--ignore=tests/slow_test.py` 跳过特定慢速测试文件。