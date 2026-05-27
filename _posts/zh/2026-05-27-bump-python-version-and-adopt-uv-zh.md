---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更新Python版本并采用UV
translated: true
type: note
---

以下是所有更改的总结：

修改的文件：

1. pyproject.toml
   - requires-python: ">=3.8" → ">=3.9"（google-genai 需要 3.9+，uv 严格强制执行）
   - pyright pythonVersion: "3.8" → "3.9"（保持一致）

2. README.md
   - 新增 uv 作为推荐安装方式（uv sync）
   - 保留 pip install -e . 作为备选方案

3. README-CN.md
   - 中文版本同样添加了 uv 相关内容

4. .github/workflows/unit_test.yml
   - 将 actions/setup-python + pip 替换为 astral-sh/setup-uv + uv sync
   - 所有测试命令均使用 uv run python ...

5. .github/workflows/integration_test.yml
   - 同样迁移至 uv，移除了额外的 pip install PyJWT numpy Pillow（现在已包含在 lockfile 中）

6. uv.lock（新增）
   - 由 uv lock 生成，已提交以支持可重复安装

现在的运行方式：

  # 全新克隆 + 安装
  uv sync          # 创建 .venv，根据 lockfile 安装依赖
  uv run ww note   # 通过 uv 运行任意命令

  # 或作为全局工具安装
  uv tool install -e .

  # pip 仍然像以前一样可用
  pip install -e .

关键说明：
- uv sync 会尊重现有的 .venv/（如果存在），否则会创建新的
- uv lock 锁定所有传递依赖，确保跨机器/CI 的可重复安装
- CI 现在使用 astral-sh/setup-uv，自动缓存依赖——比 pip 快得多
- requires-python 从 3.8 提升到 3.9 在实践中没有实际影响（google-genai 已经要求 3.9，uv 只是现在强制执行）