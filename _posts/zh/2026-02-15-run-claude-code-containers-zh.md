---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在容器中运行 Claude Code
translated: true
type: note
---

Question: 如何在容器或云服务器中运行 Claude code (Claude Code interpreter/agent)？

Answer:

**Claude Code**（Anthropic 推出的基于终端的 AI coding agent / code interpreter 工具）通常在 **Docker containers** 中运行，以确保安全和隔离。这是许多场景下官方推荐的方法，因为 Claude Code 可以执行任意代码、安装软件包、运行服务器等。

以下是 2026 年人们运行它的几种主要实践方式（本地容器或云端 / VPS）：

### 1. 最快且推荐的方式：使用 Docker Sandbox (本地或云端 VM)

Docker 引入了内置支持，用于在隔离的 sandboxes 中运行像 Claude Code 这样的 coding agents。

```bash
# 确保安装了最新版本的 Docker
docker sandbox run claude ~/my-project
```

- 挂载当前文件夹
- 在安全、隔离的环境中运行 Claude Code
- 设置成本极低

你也可以直接传递 prompt：

```bash
docker sandbox run claude -- "refactor this API client to use async/await"
```

适用于 Mac, Windows, Linux。

### 2. 在 VS Code Dev Container 中运行 (非常流行且安全)

最面向开发者的路径：

1. 安装 **Docker Desktop** + **VS Code** + **Dev Containers** 扩展
2. 使用 Anthropic 官方模板或社区模板：
   - <https://github.com/anthropics/claude-code> (查找 `.devcontainer` 文件夹)
   - 存在许多社区分支 / 模板（搜索 "claude code devcontainer"）
3. 打开文件夹 → 选择 "Reopen in Container"
4. Claude Code 在具有强隔离性的容器内运行
5. 你可以使用 `--dangerously-skip-permissions` 参数进行完全自主模式

这种设置经常用于长时间运行的 agents。

### 3. 普通 Docker 容器 (自定义 / 云端 VPS 友好)

最小化的 Dockerfile 示例：

```dockerfile
FROM ubuntu:24.04

RUN apt-get update && apt-get install -y curl git build-essential
RUN curl -fsSL https://claude.ai/install.sh | bash

# 可选：安装 Claude Code 偏好的常用工具
RUN apt-get install -y python3 python3-pip nodejs npm

WORKDIR /workspace

CMD ["claude"]
```

构建并运行：

```bash
docker build -t claude-code .
docker run -it --rm \
  -v "$(pwd)":/workspace \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  claude-code
```

在 **云端 VPS** (RunPod, Hostinger, AWS EC2, DigitalOcean 等) 上：

- 通过 SSH 进入服务器
- 安装 Docker
- 使用上述方法之一
- 许多人配合使用 `tmux` + `claude`，或者通过 **ShellHub** / Tailscale 暴露访问权限，以便从手机/笔记本电脑进行远程访问

### 4. 特定云端 / 托管 Sandbox 选项

- **Cloudflare Sandboxes** → 通过其 sandbox SDK 运行 Claude Code
- **E2B**, **Daytona**, **Vercel Sandbox**, **Fly Machines** —— 为 AI agents 提供托管的安全容器
- **RunPod** —— 流行于 GPU pods + Claude Code 设置（已有成熟模板）
- **AWS ECS Fargate** / **Google Cloud Run** —— 将 Claude Code 容器化并以 serverless / 始终在线的方式运行

### 5. 如果你想运行完全本地模型 (无 Anthropic API)

一些人通过 **Docker Model Runner** 或 Ollama + Anthropic 兼容端点，将 Anthropic 后端替换为本地模型：

```bash
ANTHROPIC_BASE_URL=http://localhost:12434 claude --model your-local-model ...
```

但大多数人仍然通过 API key 使用真实的 Claude 模型 (Sonnet 3.7 / Opus 4 / 等)。

**安全提示**：始终在容器中运行 Claude Code —— 永远不要直接在你的主机器上带危险标志运行，特别是当交给它长时间运行的 / 自主任务时。

根据你的目标选择方法：

- 快速且本地使用 → `docker sandbox run claude`
- 开发工作流 → VS Code Dev Container
- 24/7 云端 agent → VPS + Docker 或托管 sandbox (E2B, Cloudflare, RunPod)

References:

- [Docker Sandboxes for Claude Code](https://docs.docker.com/ai/sandboxes/claude-code)
- [Claude Code official docs – Dev Containers](https://code.claude.com/docs/en/devcontainer)
- [Run Claude Code in DevContainer guide](https://codewithandrea.com/articles/run-ai-agents-inside-devcontainer)
- [Cloudflare Sandbox – Claude Code example](https://developers.cloudflare.com/sandbox/tutorials/claude-code)
- [RunPod Claude Code setup guide](https://www.runpod.io/blog/your-first-claude-code-project-within-runpod-a-complete-setup-guide)
