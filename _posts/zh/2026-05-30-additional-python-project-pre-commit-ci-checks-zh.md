---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 额外的Python项目预提交CI检查
translated: true
type: note
---

**问题：** 除了已经在运行的检查外，我们还可以为 Python 项目添加哪些 pre-commit / CI 检查？

**回答：**

你已经运行了一套扎实的基础检查。以下是值得添加的检查，按价值分组：

## 高价值 —— 优先添加这些

### `pytest` + `pytest-cov`
```yaml
- repo: local
  hooks:
    - id: pytest
      name: pytest
      entry: pytest tests/ --tb=short -q
      language: system
      pass_filenames: false
      always_run: true
```
覆盖率门禁：
```yaml
entry: pytest --cov=ww --cov-fail-under=80 -q
```

### `bandit` —— 安全 lint 检查
捕获硬编码的机密信息、Shell 注入、不安全的 `eval` 等。
```yaml
- repo: https://github.com/PyCQA/bandit
  rev: 1.8.3
  hooks:
    - id: bandit
      args: ["-r", "ww/", "-ll"]  # -ll = 仅中高严重性
```

### `detect-secrets`
在提交前扫描 API 密钥、令牌、密码等。
```yaml
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.5.0
  hooks:
    - id: detect-secrets
      args: ['--baseline', '.secrets.baseline']
```
初始化一次：`detect-secrets scan > .secrets.baseline`

---

## 中等价值 —— 视情况添加

### `mypy` —— 严格类型检查
你已经使用了 `pyright`，但 `mypy` 能捕获不同的边界情况。同时运行两者有些过度 —— 除非某个依赖只有 mypy 的存根，否则坚持用 pyright。

### `pip-audit` —— 依赖项 CVE 扫描
```yaml
- repo: https://github.com/pypa/pip-audit
  rev: v2.9.0
  hooks:
    - id: pip-audit
```
检查 `requirements.txt` / `pyproject.toml` 与 OSV/PyPI 漏洞数据库的对比。

### `vulture` —— 死代码检测
```yaml
- repo: https://github.com/jendrikseipp/vulture
  rev: v2.14
  hooks:
    - id: vulture
      args: ["ww/", "--min-confidence", "80"]
```
对于像 `ww` 这样的 CLI 工具尤其有用，因为命令会不断积累。

### `interrogate` —— 文档字符串覆盖率
```yaml
- repo: https://github.com/econchick/interrogate
  rev: 1.7.0
  hooks:
    - id: interrogate
      args: ["-vv", "--fail-under", "70", "ww/"]
```

---

## 低开销 —— 值得添加到 `pre-commit` 中

```yaml
# 你可能已经有其中一些，但以下这些常被遗漏：
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v5.0.0
  hooks:
    - id: check-added-large-files     # 阻止超过 500KB 的文件
      args: ['--maxkb=500']
    - id: check-ast                   # Python 语法有效性
    - id: check-json
    - id: check-symlinks
    - id: no-commit-to-branch         # 保护 main/master 分支
      args: ['--branch', 'main']
    - id: check-executables-have-shebangs
    - id: mixed-line-ending
```

---

## 仅限 CI（对 Pre-commit 来说太慢）

这些检查属于 GitHub Actions / GitLab CI，不适合本地 hook：

| 检查项 | 工具 | 仅限 CI 的原因 |
|---|---|---|
| 集成测试 | `pytest -m integration` | 需要网络/AMD 云端 |
| 变异测试 | `mutmut` | 耗时数分钟 |
| 完整覆盖率报告 | `pytest-cov` + Codecov | 需要上传令牌 |
| 依赖许可检查 | `pip-licenses` | 扫描较慢 |
| 容器扫描 | `trivy` | 需要 Docker |

```yaml
# .github/workflows/ci.yml 片段
- name: pip-audit
  run: pip-audit --requirement requirements.txt

- name: bandit full scan
  run: bandit -r ww/ -f json -o bandit-report.json
```

---

## 针对 `ww` 项目的具体建议

鉴于这是一个面向 AMD Dev Cloud / 云端 API 的 CLI 代理工具，我建议优先考虑：

1. **`bandit`** —— 你正在处理云端凭据、SSH 密钥、API 密钥
2. **`detect-secrets`** —— 同样原因；泄露一个 AMD 密钥代价高昂
3. **`pip-audit`** —— 你为 LLM/云端 SDK 使用了大量依赖
4. **`check-added-large-files`** —— 防止意外提交模型权重或日志
5. **`pytest` 配合 `--cov`** —— 哪怕 CLI 入口点的覆盖率只有 60%，也能节省调试时间

在项目稳定之前跳过 `interrogate` 和 `vulture` —— 它们会在快速迭代时制造噪音。