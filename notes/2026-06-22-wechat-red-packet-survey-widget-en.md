---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Red Packet Survey Widget
translated: false
type: note
---

Here's a red packet style survey widget — single pick, one question, WeChat-inspired UX:This is a demo/mockup version of the red packet survey. For the real WeChat group flow, a few notes:

**To actually deploy this:** You'd need a backend to persist votes (Cloudflare Worker + KV, or a simple Supabase table) and generate a real red packet link via WeChat Pay API. The ¥0.01 red packet would be sent separately after they submit — WeChat doesn't natively gate red packet claims behind a form.

**Simpler real-world approach:** Post the red packet first (让大家抢), then immediately post a Typeform/Wenjuanxing poll link in the same message. People who grabbed the packet are more likely to fill it out — social reciprocity works.

**Copy for the group message:**
> 🧧 发个小红包答谢大家，同时做个小调研～
> 请问你访问过 lzwjava.github.io 吗？
> 【经常访问 / 访问过 / 没访问过】
> 选一个回复就行，帮我判断要不要把 markdown 改成可视化 HTML 格式 🙏
