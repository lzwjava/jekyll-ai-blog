---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 全部1652项测试均通过
translated: true
type: note
---

所有 **1652 项测试通过**，3 项跳过（与之前相同——跳过的测试针对可选依赖项）。零错误，零失败。

## 修复摘要

以下是发现的问题及修复内容：

### 1. `ww/env/__init__.py` — `load_env()` 仅从 `~/.config/ww/.env` 加载

**问题**：`load_env()` 函数仅从 `~/.config/ww/.env` 加载，但 AGENTS.md 文档和测试期望它也从 `BASE_PATH`、当前工作目录和项目根目录加载。

**修复**：更新了 `load_env()`，使其按顺序从以下 4 个位置加载 `.env`（后加载的覆盖先加载的）：

- 当前工作目录
- 项目根目录（`ww/` 的父目录）
- `BASE_PATH` 环境变量（如果已设置）
- `~/.config/ww/.env`

### 2. `tests/social/test_x_bulk_unfollow.py` — 11 个错误 + 1 个失败

源文件 `ww/social/x_bulk_unfollow.py` 经历了重大重构（基于批处理的 LLM 选择、`launch_chrome` 中的重试循环），但测试未相应更新。

**修复**：

- **`test_launch_chrome`**：将模拟目标从 `ww.social.x_bulk_unfollow.socket.create_connection`（因 `socket` 在函数内部导入而失败）改为 `socket.create_connection`。更新了 sleep 断言，因为该函数现在包含连接重试循环，在模拟情况下会立即退出。
- **`TestAskLlmShouldUnfollow` → `TestAskLlmPickUnfollow`**：重写了所有 5 项测试，以匹配新的 `ask_llm_pick_unfollow(profiles)` 函数，该函数返回 `(index, reason)`，而非旧的 `ask_llm_should_unfollow(profile)` 返回的 `(decision, reason)`。
- **`TestUnfollowWithLlm`**：完全重写了所有 5 项测试。旧测试使用了 `dry_run`（已从 API 中移除）、模拟了 `ask_llm_should_unfollow`（已重命名），并包含复杂的页面模拟逻辑，与新代码的控制流不匹配。新测试在高层模拟 `collect_batch` 和 `do_unfollow`，并使用了适当的 `side_effect` 函数来处理每次迭代的双重调用模式。
- **`_make_page_with_cells` 辅助函数**：简化后返回一致的单元格数量（旧版本在首次调用后会递减计数）。
