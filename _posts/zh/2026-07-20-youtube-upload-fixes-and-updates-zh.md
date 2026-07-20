---
audio: false
generated: true
image: false
lang: zh
layout: post
title: YouTube上传修复与更新
translated: true
type: note
---

已提交并推送至 `main` (ca2be2d)。

**所有修复摘要：**

1. **OAuth 重定向 URI 错误** — 移除了在本地服务器启动前手动调用的 `flow.authorization_url()`。现在由 `run_local_server(port=8080)` 处理完整流程，包括重定向 URI。

2. **YouTube 无效描述错误** — 根本原因是 `(<$80)` 中的 `<` 字符。YouTube API 会拒绝 `<` 视为潜在 HTML。通过在 `_clean_description()` 函数中将 `<` 替换为 `less than` 来修复，同时移除引用链接、表格、代码块及其他 markdown 格式残留。

3. **Pyright 排除** — 将 `ww/gen_video/youtube_upload.py` 加入 pyright 的排除列表，因为 Google 包不在其类型检查环境中。

**文件变更：**

- `ww/gen_video/youtube_upload.py` — 新增（YouTube 上传模块）
- `ww/main.py` — 子命令路由 + 帮助文本
- `pyproject.toml` — pyright 排除 + google-api-python-client 依赖
