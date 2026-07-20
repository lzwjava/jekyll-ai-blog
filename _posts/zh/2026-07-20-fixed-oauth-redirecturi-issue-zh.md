---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复了OAuth redirect_uri问题
translated: true
type: note
---

修复已应用。问题原因如下：

1. **根本原因**：`flow.authorization_url()` 在本地服务器启动**之前**被调用，导致授权 URL 中未包含 redirect_uri（`http://localhost:8080/`）。Google 因"缺少必需参数：redirect_uri"而拒绝请求。

2. **修复方案**：移除了手动的 `webbrowser.open(flow.authorization_url()[0])` 调用。现在由 `flow.run_local_server(port=8080)` 处理整个流程——自动启动服务器、生成带正确 redirect_uri 的 URL、打开浏览器并等待回调。

3. **新增提示**：已添加明确说明，要求在 Google Cloud 控制台中将 `http://localhost:8080/` 添加为授权重定向 URI——这是一个容易遗漏但必须完成的步骤。

请重新尝试运行：
```bash
uv run ww gen-video upload /Users/lzwjava/projects/jekyll-ai-blog/notes/2026-07-20-tesla-p100-vs-m60-for-ai-en.md /Users/lzwjava/Downloads/test_gen_video.mp4
```

如果尚未完成配置，请在 Google Cloud 控制台的 **API 与服务 → 凭据 → 您的 OAuth 2.0 客户端 ID → 已获授权的重定向 URI** 中添加 `http://localhost:8080/`。