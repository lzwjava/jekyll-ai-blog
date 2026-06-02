---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 增强工作流安全漏洞
translated: true
type: note
---

以下是我发现的内容：

== 当前状态 ==

预提交（.pre-commit-config.yaml）：
  [x] trailing-whitespace
  [x] end-of-file-fixer
  [x] check-yaml
  [x] check-toml
  [x] check-merge-conflict
  [x] debug-statements
  [x] ruff（lint + 格式化）
  [x] pyright

CI（.github/workflows/）：
  [x] unit_test.yml — 单元测试 + 覆盖率
  [x] integration_test.yml — unittest 发现
  [ ] 缺少 lint/类型检查 CI 工作流
  [ ] 缺少安全扫描 CI
  [ ] 缺少覆盖率阈值强制执行

.gitignore：
  [x] .env, __pycache__, .coverage, .pytest_cache

测试：50+ 个测试文件 — 存在稳健的覆盖率。

== 差距 — 按对 ww 的价值排序 ==

1. 缺失：完全没有安全钩子
   ww 处理 API 密钥（OpenRouter、GitHub、AMD 云）、SSH
   连接、云凭证。一次 .env 泄露 = 灾难。
   需要：bandit + detect-secrets

2. 缺失：缺少大文件防护
   ML 项目 — 容易意外提交模型权重或
   大型数据集。需要：check-added-large-files

3. 缺失：缺少针对 ruff/pyright 的 CI 工作流
   预提交在本地捕获，但跳过预提交（--no-verify）的贡献者
   什么也得不到。需要：lint CI 任务。

4. 缺失：缺少依赖审计
   27 个直接依赖，许多云/LLM SDK。需要：pip-audit

5. 缺失：缺少覆盖率阈值
   单元测试 CI 运行覆盖率但未设置门槛。
   测试可能无声下降到 20%，CI 仍然通过。

6. 缺失：缺少 no-commit-to-branch
   没有措施阻止直接推送到 main。

== 快速解决（按此顺序添加）==

1. 添加到 .pre-commit-config.yaml：
   - bandit（安全）
   - detect-secrets（凭证泄露预防）
   - check-added-large-files（最大 500KB）
   - check-ast（Python 语法有效性）
   - no-commit-to-branch（保护 main）

2. 添加 lint CI 任务：
   - ruff check + ruff format --check
   - pyright
   - bandit -r ww/ -ll

3. 添加覆盖率阈值到 unit_test.yml：
   --cov-fail-under=60

4. 添加 pip-audit 到 CI

需要我实现其中任何一项吗？我建议从预提交添加（#1）开始，因为这是影响力最高、工作量最低的更改。
