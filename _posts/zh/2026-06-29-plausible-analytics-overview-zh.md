---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Plausible Analytics 概览
translated: true
type: note
---

问题：请简要介绍 Plausible Analytics（github.com/plausible/analytics）。

答案：

Plausible 是一款开源、隐私优先、轻量级的网站分析工具——定位为 Google Analytics 的替代品。以下重点信息对你来说更有价值。

**核心卖点**
- **隐私优先**：无 Cookie、无持久标识符，开箱即符合 GDPR/CCPA/PECR 规范。由于不在访客设备上存储任何信息，因此无需 Cookie 弹窗。
- **轻量级**：追踪脚本小于 1 KB（而 Google Analytics 约 45 KB 以上）。这对注重页面加载速度的网站是巨大优势。
- **支持自托管**（AGPLv3 协议）或使用其付费托管云服务。该仓库是完整产品，而非精简社区版。

**技术栈——这才是你关心的重点**
- **后端：Elixir / Phoenix**。这是一个大规模生产级的 Elixir 代码库——如果你对 BEAM/OTP 并发模型感兴趣，值得研读。他们大量使用 Phoenix LiveView 构建仪表盘（服务端渲染的响应式 UI，极少量 JavaScript）。
- **分析存储：ClickHouse**。这是与你最相关的部分。所有事件数据存入 ClickHouse，这是一个列式 OLAP 数据库，专为数十亿行数据的快速聚合而设计。PostgreSQL 负责应用/配置/用户数据；ClickHouse 处理海量事件流。研究他们如何建模事件、按时间分区以及编写聚合查询，是学习 OLAP 架构设计的绝佳案例。
- **前端**：仪表盘组件使用 React，搭配 Tailwind。

**架构思维模型**
```
tracker.js（<1 KB）──POST──> /api/event（Phoenix）
                                  │
                    ┌─────────────┴─────────────┐
                PostgreSQL                  ClickHouse
            （用户、站点、                （页面浏览、事件——
             配置、计费）                  列式存储、只追加）
                                            │
                                    Phoenix LiveView 仪表盘
                                    （读取时执行聚合查询）
```

核心技巧：数据摄入是轻量的追加路径；所有繁重工作都在仪表盘渲染时通过对 ClickHouse 的下推聚合查询完成，而非预计算各种汇总。

**自托管快速开始**（推荐使用 Docker Compose）：
```bash
git clone https://github.com/plausible/community-edition plausible-ce
cd plausible-ce
# 生成 SECRET_KEY_BASE
openssl rand -base64 48
# 编辑 plausible-conf.env：设置 BASE_URL、SECRET_KEY_BASE 等
docker compose up -d
```
注意：自托管版本位于独立仓库（`plausible/community-edition`），它封装了主仓库 `plausible/analytics` 的镜像以及 PostgreSQL + ClickHouse 服务。主仓库才是源代码所在。

**为什么特别值得你关注**
1. 生产级 Elixir + ClickHouse 为任何高写入、读取聚合型系统提供了清晰的参考架构——如果你未来要构建 LLM 使用量/遥测分析层（你正在消耗约 20 亿 token），你会需要这种形式的存储来处理每个请求的事件分析。
2. ClickHouse 的事件 schema 和查询模式是学习 OLAP 设计的紧凑实战案例。
3. 隐私优先/无 Cookie 的计数方法（如何在不使用持久标识符的情况下去重独立访客——使用 IP + User-Agent + 域名的每日轮换加盐哈希）是一种精巧的约束驱动型设计。

我建议先浏览 `lib/plausible/`（Elixir 核心代码）和 ClickHouse 迁移文件——精华都在那里。

需要说明的是，我是基于对该项目的普遍了解而非当前仓库的实时代码给出回答；如果你需要，我可以拉取最新的 README 以及当前的 schema/迁移文件来验证具体的社区版设置步骤和 ClickHouse 表定义。

参考链接：

- [plausible/analytics](https://github.com/plausible/analytics)
- [plausible/community-edition](https://github.com/plausible/community-edition)