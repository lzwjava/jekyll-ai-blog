---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 直播平台AI集成策略
translated: true
type: note
---

是的——这个项目其实非常适合做这件事。我看了代码，有几个因素对你有利：

**为什么这个项目很适合**

- **真实的领域数据作为基础**：直播带有 Markdown 公告/详情（`noticeArea`、`EditDetailView`）、聊天记录（LeanCloud 实时）、视频、用户列表。这就是天然的 RAG 语料库——不需要合成数据。
- **已具备流式渲染 UI**：你已经内置了 `marked` + `highlight.js` + `markdown.vue`/`markdown-area.vue`，这正是逐 token 渲染 LLM 输出（含代码块）所需要的东西。
- **已有聊天界面**：`LiveView.vue` 带有标签页（聊天 / 公告 / 切换线路）。AI 助手只是多一个标签页，而不是一个新的应用。
- **干净的 API 接缝**：所有请求都通过 `/api` 的 axios 实例 + Vite 代理，所以增加一个 AI 服务（`/ai`）可以沿用现有模式，无需改动已部署的后端。

**两个演示概念**

1. **RAG ——“直播助手”标签页**
   - 数据摄取：公告、直播详情、历史聊天记录、视频描述 → 分块 → 嵌入 → 向量存储。
   - 观众问“这期直播讲了 X 吗？”→ 答案流式返回，并附带**引用**（“来源：第12期公告 / 聊天记录 14:32”）。引用是让 RAG 演示更有可信度的关键。
2. **Agent —— 工具调用型助手**
   - 工具封装你现有的 API：`fetchLive`、`fetchVideos`、`fetchUsers`、`saveLiveData`（发布公告）、搜索直播。
   - 演示时刻：*“总结这场直播，写一条公告发出去”* → Agent 规划 → 调用工具 → 流式输出结果。显示**工具调用追踪面板**（第 1 步：检索公告… 第 2 步：查询聊天记录… 第 3 步：发布）——可见的多步推理才是“Agent”区别于“chatbot”的关键。

**建议架构**

- 保持 `live-server` 不动。构建一个轻量 AI 服务（Node + Hono，或使用 Workers AI + Vectorize 的 Cloudflare Worker），对外提供 `/chat`（SSE 流式）和 `/ingest`。
- 在 `vite.config.js` 中紧挨着 `/api` 添加一个 `/ai` 代理条目。
- 前端：新增 `AssistantView` 组件 + 一个轻量的 SSE 读取器；复用 `markdown.vue` 进行渲染。

**阶段规划**

1. 代理 + 流式聊天接口 + 带引用的助手标签页（最快做出可演示的东西）
2. 通过现有 API 拉取真实直播内容的摄取脚本
3. 带工具和追踪 UI 的 Agent 循环
4. 推荐问题、答案评估、细节打磨

在继续之前有一个问题：目标是做作品集/演讲演示，还是给去直播做真实产品功能？另外，你能控制 `live-server` 吗（能否直接在那里加接口，还是必须用独立服务）？如果你需要，我现在就可以搭好 Phase 1（`/ai` 代理 + 助手标签页 + SSE 流式）。