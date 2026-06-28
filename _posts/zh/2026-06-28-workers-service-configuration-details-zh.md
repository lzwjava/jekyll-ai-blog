---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 工人服务配置详情
translated: true
type: note
---

这是一个 Cloudflare **Workers** 服务（不是 Pages——尽管面包屑导航显示的是 `/workers/services/` 路径，但它实际上是 Workers）。该服务名为 `sec-edgar-gpt`，从你的 GitHub 仓库部署而来。以下是各部分含义：

## 变量和机密（Variables and secrets）

注入到 Worker 中的运行时配置。**变量（Variables）** 是明文（例如 `API_BASE_URL`），**机密（Secrets）** 是加密且仅可写入的（例如 `OPENAI_API_KEY`、SEC EDGAR 认证）。在处理器中通过 `env.MY_VAR` 访问。当前未定义任何变量或机密。

## 触发事件（Trigger events）

Worker 在 HTTP 之外被调用的方式：

- **Cron 触发器（Cron triggers）** — 计划执行（`*/5 * * * *`），运行你的 `scheduled()` 处理器
- **队列/消息（Queue/messaging）** — 从 Cloudflare Queues 消费消息

## 可观测性（Observability）

调试遥测，当前全部**禁用**：

- **Logs** — `console.log` 在控制台中的持久化（否则为临时输出）
- **Traces** — 分布式追踪跨度
- **Exports** — 将日志发送到外部接收端（Datadog 等）
- **Sampling** — 捕获一部分请求以控制成本/流量
- **Tail Worker** — 一个独立的 Worker，以编程方式接收此 Worker 的日志/事件

对于基于 GPT 的服务，建议开启 **Logs**——成本低且对调试 API 故障很有用。

## 运行时（Runtime）

- **放置（Placement）** — `Default` 在离用户最近的边缘运行。`Smart` 放置会就近将执行位置移至后端/源站附近，以减少延迟（当需要多次往返 SEC EDGAR 或 LLM 的 API 时很有用）。
- **兼容性日期（Compatibility date）**（`Jun 27, 2026`）— 将 Workers 运行时行为锁定在该日期的语义上，避免未来运行时变更对你造成影响。
- **兼容性标志（Compatibility flags）** — 选择性启用特定的运行时功能（例如 `nodejs_compat` 用于 Node 内置模块）。

## 构建（Build）

来自 Git 的 CI/CD：

- **构建命令（Build command）: 无**，**部署命令（Deploy command）: `npx wrangler deploy`** — 推送到 `main` 分支时，Cloudflare 会运行 wrangler 将其部署
- **版本命令（Version command）: `npx wrangler versions upload`** — 上传非生产版本但不将其提升为正式版本（用于预览/灰度发布）
- **监视路径（Watch paths）: `*`** — 任何文件变更都会触发构建
- **分支控制（Branch control）** — `main` 为生产分支；其他分支会获得预览部署
- **构建缓存（Build cache）: 已启用** — 缓存构建之间的依赖以加快速度
- **API 令牌（API token）** — 构建管道用于代表你进行部署的作用域令牌

## 常规（General）

名称和删除按钮（不可逆——会清除版本、部署和配置）。

---

**Pages 与 Workers 说明：** 页面标题显示“Workers & Pages”，因为两者已统一。真正的 *Pages* 项目以静态资源构建为核心，包含 `_worker.js` 或 Functions 目录，并有“构建输出目录”设置。你的项目是纯 Worker——使用 `wrangler deploy`、兼容性标志和 Cron 触发器——因此请将其视为 Worker。`nodejs_compat` 标志是值得检查的一项，如果你需要拉取 SEC 文件并使用 Node 流/缓冲区的话。
