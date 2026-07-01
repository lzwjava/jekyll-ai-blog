---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 优化预提交与持续集成检查
translated: true
type: note
---

**问题：** 鉴于你的代码库和工作流程，应如何设计 pre-commit hooks 与 GitHub Actions 的架构，以在开发者速度与代码质量之间取得平衡？

**回答：**

你已正确识别了核心权衡：**pre-commit 是同步摩擦，CI 是异步安全保障**。以下是决策框架：

### 按延迟分类

| 检查项 | 延迟 | 阻碍开发者？ | 判定结果 |
| ------- | --------- | ------------ | --------- |
| **快（<100ms）** | 尾随空格、文件末尾、yaml、toml、json、合并冲突、ast、大小写冲突 | ✅ 是 | Pre-commit |
| **中等（500ms-2s）** | ruff（检查+格式化）、shellcheck、混合换行符 | ⚠️ 可能 | Pre-commit，但需优化速度配置 |
| **慢（5s+）** | pyright（含依赖的类型检查）、bandit（递归扫描） | ❌ 否 | 仅 GitHub Actions |
| **依赖上下文** | 大文件检查、测试 | ❌ 否 | GitHub Actions |

### 当前配置的问题

1. **`pyright` 依赖 20+ 个包** —— 这是你的瓶颈。在快速机器上用 torch、tensorflow、云 SDK 进行 Python 类型检查也可能耗时 5-15 秒。会阻塞每次提交。移至 GitHub Actions。

2. **`bandit -r scripts/`** —— 对不断增长的代码库进行递归安全扫描会线性变慢。要么：
   - 移至 GitHub Actions（只运行一次，非每次提交）
   - 或者保留但只扫描变更文件（需配置 pre-commit 插件）

3. **大型代码库上的 `ruff-format`** —— 如果你有数百个 Python 文件，格式化可能耗时 2-5 秒。本地测试：`time ruff format .`

### 推荐拆分方案

**Pre-commit（保留本地，快速反馈）：**

```yaml
- 基本规范：trailing-ws, end-of-file, mixed-line-ending, case-conflict
- 结构化数据：check-yaml, check-toml, check-json（快速、确定）
- 代码语法：check-ast, debug-statements, check-executables-have-shebangs
- 冲突标记：check-merge-conflict
- 大小限制：check-added-large-files（捕获意外提交二进制文件）
- Ruff 格式化与 lint（仅针对已变更文件，暂存它们）
```

**GitHub Actions（异步，全面）：**

```yaml
- pyright（类型检查）
- bandit（安全扫描）
- 其他 linter（eslint、markdown lint）
- 测试（pytest、集成测试）
- 构建检查（如适用）
```

### 配置优化

**让 ruff 在 pre-commit 中更快：**

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.9.10
  hooks:
    - id: ruff
      args: [--fix, --select, "E,W,F,I,UP"]  # 聚焦核心规则，而非全部
    - id: ruff-format
      stages: [commit]  # 仅在提交时，而非推送时
```

**将 pyright 移至 GitHub Actions：**

```yaml
# .github/workflows/type-check.yml
name: 类型检查
on: [pull_request, push]
jobs:
  pyright:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - run: pip install pyright torch ... (依赖)
      - run: pyright scripts/
```

**Bandit 仅放在 GitHub Actions：**
从 pre-commit 中完全移除。添加到 GitHub Actions，每个 PR 运行一次。

### 测量影响

在更改任何内容之前，先测量当前设置：

```bash
# 计时每个 hook
time pre-commit run --all-files
time pre-commit run pyright --all-files
time pre-commit run bandit --all-files
```

如果任何 hook 耗时 >2 秒，将其移至 CI。经验法则：**如果开发者总 pre-commit 延迟超过 3 秒，他们就会开始使用 `--no-verify`**。

### 你的具体案例

鉴于你：

- 快速交付
- 使用 CLI 优先的工作流
- 拥有异构代码库（Python、shell、YAML、markdown）
- 重视 CI 严谨性（安全、类型）

**我推荐：**

```yaml
# 保留在 pre-commit（总耗时 < 1 秒）
- trailing-whitespace, end-of-file, mixed-line-ending
- check-yaml, check-toml, check-json
- check-ast, debug-statements, check-merge-conflict
- ruff（格式化 + 仅核心 lint 规则）
- shellcheck

# 从 pre-commit 移除，移至 GitHub Actions
- pyright（昂贵的类型检查）
- bandit（安全，异步运行）
```

然后在 `.github/workflows/quality.yml` 中添加：

- 完整的 pyright 扫描
- bandit 安全扫描
- 任何集成测试

这样：**提交即时完成，反馈全面异步，本地迭代时毫无摩擦**。

### 你问的问题：“它们失败的频率如何？”

这取决于团队纪律。在维护良好的代码库中：

- 基本规范检查失败率 <1%（多为偶然）
- Ruff lint 失败率约 5-10%（捕获真实问题）
- Pyright 失败率约 10-20%（类型更严格）
- Bandit 失败率 <1%（多为你会跳过的误报）

如果任何 hook 失败率超过 30%，要么：

1. hook 过于严格（禁用或配置）
2. 你的代码库质量在下降（解决根本原因）

**TL;DR:** Pre-commit = 快速的本地反馈循环。CI = 全面的异步检查。将任何耗时 >2 秒的检查移至 CI。你将交付更快，并在 PR 合并前捕获问题。
