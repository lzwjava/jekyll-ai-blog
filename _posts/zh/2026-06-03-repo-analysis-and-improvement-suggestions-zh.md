---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 仓库分析与改进建议
translated: true
type: note
---

现在我对代码库有了全面的了解。以下是我的分析：

---

## 对 `ww` 仓库的分析

**现有内容：**

- 90+ 个命令模块位于扁平化的 `main.py` 调度器中（约 1573 行）
- 预提交钩子：尾部空格、ruff、pyright、bandit、detect-secrets、pytest
- CI：3 个工作流（lint、单元测试、集成测试）
- SQLite 命令日志记录（`ww/db.py`）
- `tests/` 中的测试（unittest 风格，通过预提交中的 pytest 运行）
- 集成测试目录存在但只占位（`test_placeholder.py`）
- 约 20+ 个未连接的模块（ml、agent、trading、social、crawler、bot 等）

**当前发现的问题：**

1. CI 使用 `unittest discover`，预提交使用 `pytest` —— 不一致
2. CI 未运行 detect-secrets（仅在预提交中）
3. 集成测试工作流在 `integration_tests/**` 上触发，但仅有一个占位文件
4. CI 中没有依赖缓存（setup-uv 但无缓存）
5. 预提交中的 Ruff 版本为 `v0.9.10`，但 `.ruff_cache` 中为 `0.14.13` —— 版本过时

---

## 建议添加的内容

### 高影响、低工作量

1. **统一 CI 使用 pytest** —— 将 unit_test.yml 从 `unittest discover` 改为 `uv run pytest tests/ -x -q`。这与预提交保持一致，提供一致的行为。

2. **将 `detect-secrets` 加入 CI** —— 目前仅在预提交中。如果有人跳过预提交（`--no-verify`），机密可能泄露。在 lint.yml 中添加一个步骤。

3. **为 CI 添加依赖缓存** —— `astral-sh/setup-uv` 支持缓存。添加 `enable-cache: true` 以加快工作流速度。

4. **添加 Dependabot 或 Renovate** —— 自动更新 `pyproject.toml` 中的依赖和预提交钩子的版本。目前一切都是手动的。

5. **删除集成测试占位文件** 或用真实测试替换。工作流存在、触发，但毫无用处——只是噪音。

### 中等影响

6. **添加 `ww doctor`** —— 一个自诊断命令，检查：Python 版本、.env 键是否存在、代理是否可达、OpenRouter API 是否响应、磁盘空间、GPU 是否可用。你已经有了 `_check_proxy()` 和环境加载——只需组合起来。

7. **添加 `ww openrouter cost`** —— 你的活动命令显示花费，但快速查看“今天/本周我花了多少”的一行命令很有用，因为你每年消耗约 15 亿个 token。数据已在 `get_activity()` 中。

8. **添加 `ww db export`** —— 将命令历史导出为 CSV/JSON 以便分析。SQLite 数据库已经记录了所有内容。

9. **连接 `ww/agent/` 模块** —— 你有 `code_agent`、`fix_agent`、`refactor_agent`、`optimize_agent`、`merge_agent` 等模块尚未连接。这些对于你的 AI 优先工作流具有高价值。

10. **添加 `ww llm cost`** —— 按模型划分的 OpenRouter 成本分解，类似于 `openrouter activity`，但专注于成本优化（任务类型最便宜的模型、浪费检测）。

11. **添加 `ww db autocomplete`** —— 基于历史使用频率的命令建议。你已经有了 `db top`——扩展它以支持 zsh 自动补全。

### 锦上添花

12. **添加 ruff 规则 `I`（isort）和 `UP`（pyupgrade）** —— 你已经在使用 ruff-format，添加导入排序和 pyupgrade 是免费的。

13. **在 CI 中添加 `coverage` 并设置 `--fail-under`** —— 已经存在 60% 的阈值，但添加一个覆盖率上传步骤（Codecov 或 Coveralls）以在 PR 评论中显示。

14. **添加每月 cron 任务运行 `pre-commit autoupdate`** —— 保持钩子版本更新。

15. **添加 `ww openrouter budget`** —— 设置月度预算，接近时发出警报。管理 API 已包含限额信息。

16. **添加 `ww git blame-ai`** —— 基于 LLM 的 `git blame`，解释更改的*原因*，而不仅仅是*谁*。将提交消息和 diff 发给 OpenRouter。

---

## 我建议优先实现的内容

考虑到你朝着 AI 工程的发展方向，并且你是主要用户：

1. **`ww doctor`** —— 在出现问题时节省调试时间
2. **`ww git blame-ai`** —— 差异化功能，利用你的 LLM 基础设施
3. **统一 CI 使用 pytest** —— 5 分钟修复，避免混淆
4. **连接 `ww/agent/` 模块** —— 你已经构建了它们，只需公开
5. **Dependabot** —— 一次性设置，保持依赖更新

需要我实现其中任何一个吗？
