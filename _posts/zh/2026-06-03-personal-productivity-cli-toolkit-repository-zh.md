---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 个人生产力命令行工具集仓库
translated: true
type: note
---

## `ww` 仓库综合总结

### 它是什么

`ww` 是一个 Python CLI 工具包 (`pip install ww`)，包含 90 多个命令，组织成约 35 个组。它是一个个人生产力瑞士军刀——一个二进制文件取代了数十个脚本、别名和一次性工具。由你构建，为你所用。

### 架构

- **入口点**：`ww/main.py`（1573 行）——扁平化的 `if/elif` 分发器，每个命令延迟导入
- **模式**：每个模块暴露 `main()`，在 `elif` 分支内部按需导入
- **状态**：SQLite 数据库 (`ww.db`) 记录每次命令调用，包含时间戳、组、子命令、退出码
- **LLM 层**：`openrouter_client.py` 封装了 OpenRouter API（非流式 + 流式），用于 git-ai-commit、笔记处理、搜索、图片生成、whisper 优化、学位分类等
- **环境**：`.env` 文件从 3 个位置加载，键值包括：`OPENROUTER_API_KEY`、`MODEL`、`VISION_MODEL`、`BASE_PATH`

### 命令组（已接入 main.py）

| 类别 | 组 |
|----------|--------|
| **Git/GitHub** | git, github, action, actions |
| **内容** | note, screenshot, image, gif, pdf, md, marp, gen-image |
| **LLM/AI** | llm, openrouter, copilot, hf, env, whisper |
| **系统** | macos, linux, proc, host, alarm, display, ghostty |
| **网络** | network, clash, cloudflare |
| **搜索** | search (bing, ddg, startpage, tavily, web, code, filename) |
| **DevOps** | sync, projects, zed, amd-dev-cloud, completion |
| **数据** | read (RAG), weather, degree, db |
| **工具** | utils, encoding |

### 未接入模块（约 20+）

这些模块代码存在，但无法通过 `ww` CLI 访问：

`ww/agent/` (code_agent, fix_agent, refactor_agent, optimize_agent, merge_agent, table_agent, toc_agent, git_grammar_agent), `ww/ml/`, `ww/torch_llm/`, `ww/mmlu/`, `ww/trading/`, `ww/social/`, `ww/crawler/`, `ww/bot/`, `ww/selenium/`, `ww/ansible/`, `ww/arduino/`, `ww/canvas/`, `ww/graph/`, `ww/kalman/`, `ww/langchain_test/`, `ww/linear/`, `ww/ocr/`, `ww/pico/`, `ww/pl/`, `ww/plot/`, `ww/postgres/`, `ww/scheme/`, `ww/supabase/`, `ww/tooluse/`, `ww/video/`, `ww/vscode/`, `ww/wandbrun/`, `ww/youtube/`, `ww/auto_ss_config/`, `ww/cloud/`, `ww/encoding/`, `ww/content/`, `ww/pyperclip_client/`

### 预提交钩子（6 个仓库）

1. **pre-commit-hooks** —— 尾随空格、EOF 修复、YAML/TOML 检查、合并冲突、调试语句、AST 检查、大文件（500KB）
2. **ruff** —— 检查 + 格式化
3. **pyright** —— 类型检查（基础模式，附带 12 个额外依赖）
4. **bandit** —— 安全扫描（跳过 22 条规则）
5. **detect-secrets** —— 密钥检测，带基线
6. **本地 pytest** —— `uv run python -m pytest tests/ -x -q --tb=short`

### CI 工作流（3 个）

1. **Lint & Security** (`lint.yml`) —— ruff check, ruff format, pyright, bandit, pip-audit。在推送/PR 到 `ww/**`、`pyproject.toml`、`.pre-commit-config.yaml` 时运行
2. **单元测试** (`unit_test.yml`) —— `unittest discover` + 覆盖率（低于 60% 失败）。在推送/PR 到 `ww/**`、`tests/**` 时运行
3. **集成测试** (`integration_test.yml`) —— `unittest discover integration_tests`。在推送/PR 到 `ww/**`、`integration_tests/**` 时运行

### 测试

- `tests/` 下约 50 个测试文件，使用 unittest 风格
- conftest.py 延迟执行 `test_audio_pipeline`（模拟 sys.modules）
- 覆盖率阈值：60%
- 大多数未接入模块没有测试套件

### 构建与工具

- **构建**：Hatchling
- **包管理器**：uv
- **Python**：>=3.11
- **代码检查**：Ruff（有意排除：E731, E722, F841）
- **类型检查**：Pyright 基础模式，排除 ml/macos/trading/wandbrun/tests/arduino/ansible/pico
- **安全**：Bandit 跳过 22 条规则，detect-secrets 带基线
- **无测试框架**：pytest 用于运行，unittest 用于编写

### 关键观察

1. **main.py 是瓶颈** —— 1573 行的 elif 链。添加一个命令需要编辑 3 个地方：模块、分发器和帮助文本。脆弱但简单。

2. **Agent 模块已构建但隐藏** —— `ww/agent/` 有 8 个以上 agent（code, fix, refactor, optimize, merge, table, toc, git-grammar），如果接入可能很有价值。

3. **CI 不一致** —— pre-commit 运行 pytest，CI 运行 unittest discover。两者都有效但输出格式不同，可能以不同方式发现测试。

4. **集成测试为空** —— 工作流存在，触发，运行占位符。要么充实要么移除。

5. **大量 LLM 集成** —— OpenRouter 客户端支持流式 + 非流式，用于 git、笔记、搜索、音频、图片生成。通过环境变量选择模型。

6. **跨平台关注** —— macOS 和 Linux 路径分离，有条件的 pyobjc 依赖，平台特定命令（ghostty, display, alarm 仅限 macOS）。

7. **无依赖管理自动化** —— 所有版本手动锁定，没有 Dependabot/Renovate。

8. **无发布/发布工作流** —— 无 PyPI 发布，无 GitHub Releases，无变更日志生成。

### 缺少的内容

| 缺口 | 影响 |
|-----|--------|
| 没有 `ww doctor`（自诊断） | 调试损坏的环境需要手动 |
| 没有 `ww git blame-ai` | AI 优先 CLI 的差异化功能 |
| 没有 `ww db export`（CSV/JSON） | 无法轻松分析使用模式 |
| 没有 `ww openrouter budget` | 没有警报的支出追踪 |
| Agent 模块未接入 | 已构建的代码闲置 |
| 没有 Dependabot | 依赖会过时 |
| 没有发布工作流 | 手动发布 |
| CI 未运行 detect-secrets | 可通过 `--no-verify` 绕过 |
| CI 未缓存 uv 依赖 | CI 运行缓慢 |
| 没有 bash/fish 补全 | 仅支持 zsh |
| 没有 CONTRIBUTING.md | 新人入门困难 |
| 没有类型 stub 或 mypy 严格模式 | 类型安全仅为基础 |
| 20+ 未接入模块 | 代码腐烂风险 |
