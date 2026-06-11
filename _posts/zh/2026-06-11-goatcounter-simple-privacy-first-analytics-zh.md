---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'GoatCounter: 简单的隐私优先分析'
translated: true
type: note
---

**问题：** 什么是GoatCounter（goatcounter.com），以及如何使用它？

**回答：**

GoatCounter 是一个开源网站分析平台，你可以将其作为免费托管服务（在 goatcounter.com）使用，也可以在自己的服务器上自托管。它由 Martin Tournoij（arp242）编写，作为谷歌分析（Google Analytics）的隐私优先替代方案——无需唯一用户标识符，无需 GDPR 同意横幅，跟踪脚本仅为页面增加约 3.5KB。

架构简述：它是一个单独的 Go 二进制文件，默认使用 SQLite，对于自托管安装可选择 PostgreSQL。这使其成为目前最简单的可自托管分析栈之一——一个二进制文件、一个嵌入式数据库，没有 Redis/队列/JS 框架的蔓延。非常符合你喜欢的“简单、可理解的系统”理念。

在你的 Jekyll 博客（lzwjava.github.io）上集成只需在布局文件中添加一行：

```html
<script data-goatcounter="https://lzwjava.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
```

如果你更愿意不使用 JS，还有无 JS 跟踪像素、后端中间件集成或日志文件导入——如果你想把 Ubuntu 工作站的 nginx 访问日志导入进去，这些功能会很有用。

在 `lzw@192.168.x.x` 上自托管：

```bash
# grab the release binary (it's Go, single static binary)
wget https://github.com/arp242/goatcounter/releases/latest/download/goatcounter-dev-linux-amd64.gz
gunzip goatcounter-*.gz && chmod +x goatcounter-*

# create a site + serve (SQLite db auto-created)
./goatcounter db create site -vhost stats.example.com -user.email you@example.com
./goatcounter serve -listen :8081 -tls none
```

你也可以通过其 API 以编程方式拉取统计数据——这对于一个报告每周博客流量的 CLI 工具很方便：

```bash
curl -s -H "Authorization: Bearer <API_KEY>" \
  "https://lzwjava.goatcounter.com/api/v0/stats/hits" | jq '.hits[:5]'
```

它跟踪的内容：页面浏览量、引荐来源、浏览器/操作系统、屏幕尺寸、国家——大致就这些。与 Matomo/Plausible/Umami 相比，它故意保持基础，没有漏斗、没有会话回放、没有转化跟踪。托管的 goatcounter.com 层级对合理的公共使用是免费的（由捐赠支持）——个人网站和小项目没问题，每天数百万页面浏览量则不行。

何时选择它而非其他替代品：如果你想要零维护、免费且能回答“哪些文章获得了流量”，选 GoatCounter；如果你想要更漂亮的仪表板和事件追踪，选 Umami 或 Plausible；如果你确实需要 GA 级别的功能，选 Matomo。对于一个约 400 篇文章的技术博客，GoatCounter 的托管免费层级基本上就是正确的懒人答案——一个脚本标签就搞定了。

**参考：**

- [GoatCounter — 官方网站](https://www.goatcounter.com/)
- [arp242/goatcounter — GitHub](https://github.com/arp242/goatcounter)
- [GoatCounter 在 Hacker News 上](https://news.ycombinator.com/item?id=34265127)