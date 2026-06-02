---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 博客访问实时Telegram通知
translated: true
type: note
---

是的，你可以搭建一个系统来近乎实时地分析 Cloudflare 日志或流量，并为每次博客访问发送 Telegram 通知。但仅凭标准分析日志无法直接实现：Cloudflare 的分析数据多为聚合数据（如每日/每周摘要），即便是其日志推送功能（导出日志）也会每 1-5 分钟批量处理数据，因此不适合用于即时单次访问提醒。即时日志功能虽支持实时流式传输，但需要企业版套餐且需通过自定义处理（例如通过 WebSocket 和脚本）来触发 Telegram 消息——这对大多数用户而言过于复杂。

最实用且实时的方案是使用 **Cloudflare Workers** 拦截发往你博客的每个请求。该方案会在每次访问时运行无服务器代码，允许你记录事件并通过 Telegram API 立即发送消息。对于低流量网站（每日不超过 10 万次请求）可免费使用，但高流量博客可能触及限制或产生费用——此外你会被通知淹没，建议设置过滤条件（例如仅针对独立 IP 或特定页面）。

### 快速配置步骤

1. **创建 Telegram 机器人**：
   - 在 Telegram 中联系 @BotFather，使用 `/newbot` 创建机器人，并保存机器人令牌（例如 `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`）。
   - 与你的机器人开启对话，然后联系 @userinfobot 获取聊天 ID（例如 `123456789`）。
   - 通过 curl 测试消息发送：

     ```
     curl -X POST "https://api.telegram.org/bot<你的机器人令牌>/sendMessage" \
     -H "Content-Type: application/json" \
     -d '{"chat_id":"<你的聊天ID>","text":"测试访问！"}'
     ```

2. **创建 Cloudflare Worker**：
   - 登录 Cloudflare 仪表板 > Workers 与 Pages > 创建应用 > 创建 Worker。
   - 命名（如 `blog-visit-notifier`）并部署默认模板。

3. **添加通知代码**：
   - 编辑 Worker 代码以拦截请求并发送至 Telegram。基础示例（需替换占位符）：

     ```javascript
     export default {
       async fetch(request, env) {
         // 可选：记录或过滤访问（例如仅针对博客首页）
         const url = new URL(request.url);
         if (url.pathname !== '/') {  // 按需调整路径
           return fetch(request);  // 跳过非博客页面
         }

         // 发送 Telegram 消息（异步执行避免阻塞）
         const message = `新访问来自 ${url.origin}！IP：${request.headers.get('cf-connecting-ip')}，用户代理：${request.headers.get('user-agent')}`;
         await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({
             chat_id: env.TELEGRAM_CHAT_ID,
             text: message,
             parse_mode: 'HTML'  // 如需格式化可启用
           })
         }).catch(err => console.error('Telegram 发送失败：', err));

         // 将原始请求代理到你的博客
         return fetch(request);
       }
     };
     ```

     - 此代码会在每次匹配请求时运行，记录基础访问者信息并通过 Telegram 发送，且不会延迟页面加载。

4. **配置环境变量**：
   - 在 Worker 设置 > 变量 > 添加：
     - `TELEGRAM_BOT_TOKEN`：你的机器人令牌
     - `TELEGRAM_CHAT_ID`：你的聊天 ID
   - 保存后重新部署。

5. **将 Worker 路由至博客**：
   - 在 Workers 设置 > 触发器 > 添加路由
   - 设置为你的博客域名/路径（例如 `yourblog.com/*`）
   - 这能确保 Worker 在每次访问到达源服务器前执行。

6. **测试与监控**：
   - 访问你的博客——Telegram 应立即收到提示
   - 在仪表板检查 Worker 日志中的错误。若触及速率限制（如 Telegram 的 30 条/秒），可通过 KV 存储添加去抖机制。

### 备用方案（若 Worker 不适用）

- **批量日志分析**：使用日志推送将 HTTP 请求日志导出至 AWS S3 或 Google Pub/Sub 等服务，再通过 Zapier 或 n8n 等工具转发至 Telegram（例如每小时汇总访问）。但非实时方案。
- **集成工具**：Albato 或 n8n 等工具可连接 Cloudflare 网络钩子至 Telegram，但无法实现单次访问通知。
- **限制说明**：免费版 Worker 每次请求限 10ms CPU 时间——当前场景足够，需要时请升级方案。高流量网站需配置节流机制。

此方案能将 Cloudflare 流量转化为可操作的即时提醒。如需代码调整或错误排查，请提供更多细节！

[Cloudflare Workers 文档](https://developers.cloudflare.com/workers/)
[Telegram 机器人 API](https://core.telegram.org/bots/api)
[Cloudflare 即时日志](https://developers.cloudflare.com/logs/instant-logs/)
