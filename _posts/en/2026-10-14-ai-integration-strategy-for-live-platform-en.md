---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Integration Strategy for Live Platform
translated: false
type: note
---

Yes — this project is actually a strong vehicle for it. I looked through the code, and it has several things working in your favor:

**Why this project fits**

- **Real domain data to ground on**: lives with markdown announcements/details (`noticeArea`, `EditDetailView`), chat transcripts (LeanCloud realtime), videos, user lists. That's a natural RAG corpus — no synthetic data needed.
- **Streaming-ready UI**: you already ship `marked` + `highlight.js` + `markdown.vue`/`markdown-area.vue`, which is exactly what you need to render token-by-token LLM output with code blocks.
- **A chat surface already exists**: `LiveView.vue` has tabs (聊天 / 公告 / 切换线路). An AI assistant is one more tab, not a new app.
- **Clean API seam**: everything goes through the `/api` axios instance + Vite proxy, so adding an AI service (`/ai`) follows the existing pattern without touching the deployed backend.

**Two demo concepts**

1. **RAG — "直播助手" tab**
   - Ingest: announcements, live details, past chat logs, video descriptions → chunk → embed → vector store.
   - Viewer asks "这期直播讲了 X 吗？" → answer streams in with **citations** ("来源：第12期公告 / 聊天记录 14:32"). Citations are what make a RAG demo credible.
2. **Agent — tool-using assistant**
   - Tools wrap your existing API: `fetchLive`, `fetchVideos`, `fetchUsers`, `saveLiveData` (post announcement), search lives.
   - Demo moment: *"总结这场直播，写一条公告发出去"* → agent plans → calls tools → streams result. Show a **tool-call trace panel** (step 1: 检索公告… step 2: 查询聊天记录… step 3: 发布) — visible multi-step reasoning is what sells "agent" vs "chatbot".

**Suggested architecture**

- Keep `live-server` untouched. Build a small AI service (Node + Hono, or a Cloudflare Worker with Workers AI + Vectorize) that exposes `/chat` (SSE streaming) and `/ingest`.
- Add a `/ai` proxy entry in `vite.config.js` next to `/api`.
- Frontend: new `AssistantView` component + a small SSE reader; reuse `markdown.vue` for rendering.

**Phases**

1. Proxy + streaming chat endpoint + assistant tab with citations (fastest path to something demoable)
2. Ingestion script pulling real lives via your existing API
3. Agent loop with tools + trace UI
4. Suggested questions, answer evals, polish

One question before going further: what's the target — a portfolio/talk demo, or a real product feature for 去直播? And do you control `live-server` (can we add endpoints there, or strictly a separate service)? I can scaffold Phase 1 (the `/ai` proxy + assistant tab + SSE streaming) right now if you want.
