---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 近视逆转应用设置摘要
translated: true
type: note
---

完成。以下是我发现的内容以及我设置的内容：

**openclaw** — 一个 Node.js Telegram/WhatsApp 机器人代理框架（`v2026.5.12`），全局安装在 `/home/lzw/.npm-global/lib/node_modules/openclaw/`。配置文件位于 `~/.openclaw/openclaw.json`。它一直存在 Telegram API 连接问题（`api.telegram.org` 的 DNS 超时——看起来是代理/网络封锁情况）。与 Hermes 无关。

**myopia-reversal-app** — 位于 `/home/lzw/.openclaw/workspace/myopia-reversal-app/`。一个单页 Web 应用（原生 HTML/CSS/JS），用于计算用于主动近视逆转的降低近用处方（通常比完全矫正低 -1.50D）。功能：单位切换（度 vs 屈光度）、中英文双语、深色模式、恢复提示。使用 Vite 作为开发依赖，但在 Mar 14 提交中只有 `index.html` + 内联 JS。

**nginx** — 已配置并重新加载：
- `http://localhost/myopia/` → 提供该应用
- 现有的 `/movies/` 和 `/todo/` 路由保持不变
- `nginx -t` 通过，已重新加载，返回 200