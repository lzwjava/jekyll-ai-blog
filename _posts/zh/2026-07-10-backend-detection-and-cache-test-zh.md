---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 后端检测与缓存测试
translated: true
type: note
---

后端检测测试
  模型: tencent/hy3-preview
  代理: HTTP_PROXY=http://127.0.0.1:7890 (端口 7890 可访问)

[1/3] 发送流式请求以检测后端...

  响应 ID:  gen-1783677403-Ki1BBI5Ijd0hQgrOz3XX
  id 检测: unknown (id='gen-1783677403-Ki1BBI5Ijd0hQgrOz3XX')
  delta 键:   ['content', 'role']
  delta 检测: unknown (delta 键: ['content', 'role'])
  TTFT:         4.319s
  总时间:   4.319s
  完整文本:    'Hello! It is a'

[2/3] 检查服务器头信息...
  服务器:        cloudflare
  X-Powered-By:  未报告

[3/3] 前缀缓存测试（两次请求共享相同前缀）...
  共享前缀: 13000 字符，约 2000 tokens

  请求 A（冷启动）... TTFT=7.703s, 总时间=7.703s
  请求 B（相同前缀，不同后缀）... TTFT=2.674s, 总时间=2.674s
  -> 可能缓存命中（TTFT 降至冷启动的 34.7%）

总结:
  后端:       unknown (id='gen-1783677403-Ki1BBI5Ijd0hQgrOz3XX') / unknown (delta 键: ['content', 'role'])
  服务器:        cloudflare
  TTFT（冷启动）:   4.319s