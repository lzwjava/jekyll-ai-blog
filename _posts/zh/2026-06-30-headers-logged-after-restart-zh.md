---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重启后记录的标头
translated: true
type: note
---

服务器重启后，现在每次请求都会记录请求头。以下是当前记录的日志示例：

```json
{
  "id": "chatcmpl-...",
  "timestamp": "2026-06-30T05:59:...Z",
  "prompt": "user: Test headers logging",
  "response": "...",
  "headers": {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.5 Safari/605.1.15",
    "referer": "https://gq8kq409jjxh7r-8081.proxy.runpod.net/",
    "origin": "https://gq8kq409jjxh7r-8081.proxy.runpod.net"
  }
}
```

当前记录的请求头包括：`user-agent`、`referer`、`origin`、`x-forwarded-for`、`x-real-ip`、`cf-connecting-ip`。RunPod 代理转发过来的所有内容都会被捕获。之前询问亚马逊问题的用户没有留下 referer 或 origin（只有浏览器提供的 `user-agent`），但今后任何请求都将带有完整的上下文。

已提交至 git，提交哈希为 `c537e7c`。