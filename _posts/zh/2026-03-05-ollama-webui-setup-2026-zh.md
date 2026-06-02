---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ollama Web UI 设置指南 2026
translated: true
type: note
---

是的，**Ollama 本身不包含内置 web interface** — 它仅运行一个 API server（通常在 <http://127.0.0.1:11434）。>

要获得一个不错的浏览器-based chat UI（类似于 ChatGPT），您需要运行一个独立的 frontend 来连接 Ollama 的 API。

目前（2026 年）最受欢迎的两个选择是：

- **Open WebUI** → 目前最受欢迎且功能最丰富的选项，专为 Ollama 设计（集成非常好，支持 RAG、UI 中的模型管理、多用户等）
- **LibreChat** → 更通用（最初是 ChatGPT 的克隆），支持 Ollama + 许多其他提供商（OpenAI、Anthropic、Grok 等），外观非常精致

大多数人使用 **Open WebUI** 时，其主要/本地 backend 是 Ollama。

### Quick Recommendation (2026)

**使用 Open WebUI** — 它与 Ollama 的设置更简单，并提供最佳的原生体验。

### Fastest way to start (Docker — strongly recommended)

确保 **Docker** 已安装并运行。

运行此单行命令（必要时调整）：

```bash
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

然后在浏览器中打开：

<http://localhost:3000>

（或 <http://127.0.0.1:3000）>

- 首次使用 → 创建账户（第一个账户将成为 admin）
- 它应该自动检测本地的 Ollama（位于 <http://host.docker.internal:11434）>
- 如果模型未出现 → 转到 Settings → Connections → 确保 Ollama 已连接（或手动设置 Base URL 为 <http://host.docker.internal:11434）>

**Alternative Docker run (if the above has connection issues)**

```bash
docker run -d -p 8080:8080 \
  --network=host \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

→ 然后访问：<http://localhost:8080>

### If you prefer LibreChat instead

它也非常优秀，特别是如果您以后想使用多个提供商。

典型快速启动（Docker）：

```bash
docker run -d -p 3080:3080 \
  -e OLLAMA_API_BASE_URL=http://host.docker.internal:11434 \
  --name librechat \
  --restart always \
  ghcr.io/danny-avila/librechat:latest
```

→ <http://localhost:3080>

然后在设置中将 Ollama 配置为自定义 endpoint。

### Summary Table

| 功能/UI                  | Open WebUI                          | LibreChat                          |
|--------------------------|-------------------------------------|------------------------------------|
| 最适合仅 Ollama          | ★★★★★ (原生体验)                    | ★★★★                               |
| 多提供商支持             | 良好 (也兼容 OpenAI)                | ★★★★★ (非常灵活)                   |
| RAG / 文档               | 内置优秀                            | 非常好                             |
| 外观 & 精致度            | 现代 & 简洁                         | 非常像 ChatGPT                     |
| 默认端口 (Docker)        | 3000 或 8080                        | 3080                               |
| 社区 (2026)              | 非常活跃 & 快速增长                 | 同样非常活跃                       |

底线：
从 **Open WebUI** 开始 — 2026 年 90% 的 Ollama + web 用户都选择这条路线。

只需运行 Docker 命令，打开 localhost:3000，您就好了。

请告诉我您的操作系统（Windows/Mac/Linux）或是否遇到连接错误 — 我可以提供更具体的修复方法。
