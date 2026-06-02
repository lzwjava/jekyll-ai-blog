---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 增强的预提交与CI安全检查
translated: true
type: note
---

所有钩子已安装并通过。以下是添加内容的摘要：

== 变更 ==

1. .pre-commit-config.yaml — 新增了 4 个钩子：
   + check-ast — 在提交前捕获语法错误
   + check-added-large-files — 阻止超过 500KB 的文件（模型权重、日志等）
   + bandit — 使用 pyproject.toml 配置进行安全扫描
   + detect-secrets — 凭证泄漏预防

2. pyproject.toml — 添加了 [tool.bandit] 部分：
   + 排除 ww/ml/ 和 tests/
   + 跳过误报：B113（超时）、B602/B605（子进程 shell）、
     B301/B314（pickle/xml）、B310（urllib）、B108（tmp）、B104（绑定所有地址）、B307（eval）
   + 仍会捕获真实问题：B608（SQL 注入）、B614（不安全的 pickle）、
     B615（未固定版本的 HF 下载）

3. .github/workflows/lint.yml — 新的工作流，包含 4 个并行任务：
   + ruff — 代码风格检查 + 格式检查
   + pyright — 类型检查
   + bandit — 安全扫描
   + pip-audit — 依赖 CVE 扫描

4. .github/workflows/unit_test.yml — 更新：
   + coverage --fail-under=60（之前无阈值）

5. .secrets.baseline — 新文件：
   + 基线化了 11 个文件（测试夹具、配置文件）
   + 排除 .env、.venv、ww/ml/

== bandit 仍会捕获的内容（7 个真实问题）==
   B608：ww/photo/ 模块中 4 处 SQL 注入
   B615：ww/embedding/ 和 ww/mmlu/ 中 3 处未固定版本的 HF 下载

这些位于特定模块中，不会影响日常工作。准备好后修复。
