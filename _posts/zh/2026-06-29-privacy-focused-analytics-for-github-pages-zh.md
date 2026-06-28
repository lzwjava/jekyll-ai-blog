---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向隐私保护的GitHub Pages分析工具
translated: true
type: note
---

**问题：** 对于我的 GitHub Pages 博客 lzwjava.github.io，最好的网站分析工具是什么？

**回答：**

对于静态 GitHub Pages 博客，隐私友好且轻量的工具胜过 Google Analytics。按使用场景推荐如下：

**Plausible** — 开源、可自托管，脚本约 1KB，无需 Cookie/GDPR 横幅。云端服务约 $9/月，但你可以在自己的工作机（`lzw@192.168.1.36`）上免费自托管。这最贴合你的技术栈。

```html
<!-- 放在 _layouts/default.html 或 _includes/head.html 中 -->
<script defer data-domain="lzwjava.github.io"
        src="https://plausible.io/js/script.js"></script>
```

使用 Docker 自托管：

```bash
git clone https://github.com/plausible/community-edition plausible-ce
cd plausible-ce
docker compose up -d   # 在 :8000 提供服务，前面放 Caddy/nginx
```

**Umami** — 同样开源、可自托管，后端使用 Postgres/MySQL。运维比 Plausible 更轻量，单一 Node 服务。如果你希望完全掌控并能通过 SQL 访问自己的分析数据，这很合适。

```bash
docker run -d --name umami \
  -e DATABASE_URL=postgresql://<USER>:<PASSWORD>@<IP_ADDRESS>:5432/umami \
  -p 3000:3000 ghcr.io/umami-software/umami:postgresql-latest
```

**GoatCounter** — 极其简单，非商业用途有免费托管层级，无需 Cookie，脚本极小。零基础设施，工作量最低。如果你只想看到页面浏览量而无需运行任何东西，这是个好选择。

```html
<script data-goatcounter="https://lzwjava.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
```

**Cloudflare Web Analytics** — 免费，无脚本体积问题，但仅当你通过 Cloudflare 代理时才有效。由于你用的是原始 GitHub Pages（`github.io` 域名无法使用 Cloudflare 代理），除非你切换到自定义域名并放在 Cloudflare 后面，否则无法使用。

**我的推荐：** 在你的 RTX 4070 工作站上自托管 **Umami**。它仅需一个容器加 Postgres，能让你通过原始 SQL 访问流量数据（可以针对访客模式运行自己的查询/嵌入/分析），无第三方数据泄露，并且符合你自托管/自主掌控的理念。如果你更喜欢开箱即用的精致界面，Plausible 是备选。

一个注意事项：你的家庭工作站需要一个稳定的公网端点（Cloudflare Tunnel 或 Tailscale Funnel）以便追踪脚本能够访问。如果你不希望暴露它，可以使用 GoatCounter 的托管层级作为零运维的备用方案。

**参考：**

- [Plausible Community Edition](https://github.com/plausible/community-edition)
- [Umami](https://github.com/umami-software/umami)
- [GoatCounter](https://www.goatcounter.com/)
- [Cloudflare Web Analytics](https://www.cloudflare.com/web-analytics/)
