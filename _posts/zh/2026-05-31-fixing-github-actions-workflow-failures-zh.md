---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 GitHub Actions 工作流故障
translated: true
type: note
---

以下是我发现并修复的问题的摘要：

## GH Actions 失败 — 根本原因及已应用的修复

### 1. Lint 与安全工作流 (`lint.yml`) — 全部 3 个任务均失败

**已应用的修复** (`/Users/lzwjava/projects/ww/.github/workflows/lint.yml`)：

- **ruff 任务**: 在 `uv sync` 后添加了 `uv pip install ruff` — ruff 未在 pyproject.toml 依赖中列出
- **pyright 任务**: 添加了 `uv pip install pyright` — 同样的问题
- **bandit 任务**: 在 `uv pip install bandit[toml]` 前添加了缺失的 `uv sync` — 不存在虚拟环境

### 2. 单元测试工作流 — 45 个错误

**已应用的修复**：

- **`pyproject.toml`**: 向依赖中添加了 `PyJWT>=2.0.0`（12 个与 jwt 相关的测试错误）
- **`tests/test_main.py`**: 更新了 `_run()` 辅助函数，对无法导入的模块（macOS-only on Linux）添加了 `sys.modules` 回退。增加了 `MagicMock` 导入。
- **`tests/test_main_extended.py`**: 使用相同的 `sys.modules` 回退模式更新了 `_dispatch()` 函数
- **Note 测试**: 添加了 `patch.dict(os.environ, {"NOTE_ENTER_CONFIRM": "1"})` 以确保 `input()` mock 被触发（之前落到了 `note_workflow.main()` 导致 ValueError）
- **Update 测试**: 将 `["ww", "update"]` 改为 `["ww", "projects", "update"]`（命令已移至 `projects` 组下）
- **Ruff f-string**: 在 `ww/amd_dev_cloud/start_train.py` 中将 `f"\n--- Creating ---"` 修复为 `"\n--- Creating ---"`

### 3. 集成测试工作流 — 目录缺失

**已应用的修复**: 创建了 `integration_tests/__init__.py`

### 剩余的约 20 个预存错误（非本人提交导致）

这些都是由于可选依赖未在 `pyproject.toml` 中列出的 `ModuleNotFoundError`：

| 测试文件 | 缺失模块 |
|-----------|---------------|
| `tests/auto_ss_config/test_lightsail.py` | `yaml` (PyYAML) |
| `tests/bot/test_punch_bot.py` | `pytz` |
| `tests/cloud/test_ec2.py` | 可能是 `yaml` |
| `tests/ml/test_w2v_utils.py` | `torch` |
| `tests/ml/test_word_vectors.py` | `torch` |
| `tests/crawler/test_weibo.py` | selenium/weibo 依赖 |
| `tests/agent/test_agents.py` | `frontmatter` |

这些测试在**导入时**失败——测试模块本身无法加载，因为源模块在顶层导入了重型/可选依赖。每个问题的修复方法是用 `try/except ImportError` + `unittest.skip()` 包裹：

```python
try:
    from ww.auto_ss_config import lightsail
except ImportError:
    lightsail = None

@unittest.skipUnless(lightsail, "Missing optional dependency: PyYAML")
class TestGetLightsailInstances(unittest.TestCase):
    ...
```

您希望我继续修复剩下的测试文件吗？
