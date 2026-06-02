---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 软件工程师的自托管工具
translated: true
type: note
---

Question: 鉴于我们现在有了 OpenClaw，我们能否轻松在第二台家用电脑上安装类似 Nextcloud 的东西？有哪些类似的自托管工具可以帮助改善我们的日常生活，尤其是作为软件工程师？

Answer:

是的，就像 **Nextcloud**（来自你分享的 GitHub 链接：<https://github.com/nextcloud/server），这是一个流行的自托管文件同步、共享和协作平台（你自己的> Dropbox/Google Drive），你可以在第二台家用电脑上轻松安装它——或者许多类似的有用工具。

大多数现代自托管软件（包括 Nextcloud 和下面列出的那些）都可以使用 **Docker**（通常配合 docker-compose）非常简单地安装，这非常适合第二台/家用机器。通常：

- 在机器上安装 Docker + docker-compose（一次性设置，在 Ubuntu/Debian 上大约 10 分钟）。
- 克隆或复制 docker-compose.yml 文件。
- 运行 `docker compose up -d` —— 就启动了。
- 通过浏览器访问 <http://your-home-ip:port（或者使用像> Traefik/Caddy + Let's Encrypt 这样的反向代理来实现 HTTPS 和漂亮的域名）。

许多工具都有优秀的官方镜像，并且可以通过 CasaOS、Yacht 或 Portainer 等工具实现一键式设置，如果你想要 GUI 仪表板。

**OpenClaw**（一个自托管的个人 AI 助手/代理，可以运行任务、访问文件、集成聊天应用等）完美融入这个生态系统——你可以在同一台机器上与其他服务一起运行它。

以下是 2026 年一些最有用的自托管工具，它们往往能显著改善日常生活和工作——尤其是对软件工程师：

### 针对开发者/家用的顶级推荐

- **Vaultwarden** (Bitwarden compatible)
  自托管密码管理器。极其轻量、安全，与所有 Bitwarden 应用/客户端兼容。完美替代 1Password/LastPass。

- **Gitea** 或 **Forgejo**
  你自己的轻量级 GitHub/GitLab。托管私有仓库、问题跟踪、CI 运行器（配合 Woodpecker 或 Drone）、维基。非常适合个人项目、脚本、dotfiles 或小团队使用，而无需支付 GitHub 的费用。

- **Immich**
  Google Photos 替代品——自托管照片/视频备份、人脸识别、相册、共享。通过应用自动手机备份。近年来非常精致。

- **Jellyfin**
  你个人的 Netflix/Plex，用于电影、电视剧、音乐。可流式传输到任何设备，无需订阅。

- **Home Assistant**
  如果你有任何智能设备（灯、传感器、插座），这是最好的开源家庭自动化中心。本地集成一切，无需云服务。

- **n8n**
  无代码/低代码自动化工作流（像 Zapier 但自托管）。连接 API、GitHub webhooks、日历、文件——对工程师来说超级有用，用于自动化重复任务。

- **Uptime Kuma**
  简单、美观的监控仪表板。检查你的网站、服务器、API 是否正常运行——通过 Telegram/Discord/邮件发送警报。

- **SearXNG**
  注重隐私的元搜索引擎。从 Google/Bing/DuckDuckGo 等聚合结果，无跟踪——可设置为浏览器默认搜索。

- **Ollama** (local LLMs)
  在你的机器上完全离线运行 AI 模型（Llama、Mistral 等）。搭配 Open WebUI 使用 ChatGPT 风格界面。与 OpenClaw 完美互补。

- **AdGuard Home** 或 **Pi-hole**
  网络范围的广告/跟踪器阻挡器 + DNS 服务器。让整个家庭的浏览更干净/更快。

### 开发者专属奖励工具

- **Code-Server** —— 在浏览器中运行 VS Code，从任何地方访问你的开发环境。
- **Portainer** 或 **CasaOS** —— Web GUI，轻松管理所有 Docker 容器。

这些都是免费/开源的、积极维护的，并且 Docker 友好。许多人会在一台普通的机器上运行 10–20 个（旧 PC、NUC、迷你服务器，甚至某些情况下是优秀的 Raspberry Pi 5）。

从解决你最大痛点的 2–3 个开始（例如，密码 + git + 照片），然后扩展。自托管社区（r/selfhosted、awesome-selfhosted 列表）几乎为所有工具提供了 docker-compose 示例。

参考资料：

- [awesome-selfhosted GitHub list](https://github.com/awesome-selfhosted/awesome-selfhosted)
- [selfh.st/apps directory](https://selfh.st/apps)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Nextcloud GitHub](https://github.com/nextcloud/server)
