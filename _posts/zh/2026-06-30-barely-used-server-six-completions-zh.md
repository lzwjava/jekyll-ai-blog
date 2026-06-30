---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 几乎未用的服务器，六次完成
translated: true
type: note
---

服务器正在运行，但几乎未被使用。以下是英文摘要：

**服务器**：SEC-EDGAR-GPT — 124M nanoGPT（`/workspace/model/server.py`）监听端口8888。于今天UTC时间05:59启动（约7小时前重启）。

**实际完成的请求（重启后共6次）**：

1. `05:28:33` — "10-K文件中披露了哪些风险因素？" → 1000 tokens，耗时21.3秒。来自浏览器（通过code-server，你的测试）。
2. `05:51:23` — "亚马逊SEC文件中的法律诉讼内容？" → 200 tokens，耗时1.3秒。iPhone通过微信浏览器访问你的8888 URL。
3. `06:00:31` — "测试标头日志记录" → 1000 tokens，耗时21秒。来自浏览器（通过code-server，你的测试）。
4. `06:42:12` — 再次询问相同亚马逊问题 → 200 tokens，耗时1.3秒。iPhone微信，CF IP 69.63.219.52。
5. `11:53:35` — "微软收入细分" → 200 tokens，耗时1.28秒。Mac Safari访问8888 URL，CF IP 69.63.219.52。
6. `11:53:43` — 再次询问亚马逊问题 → 200 tokens，耗时1.32秒。同一Safari会话。

**这说明**：
- 06:42通过8888 URL来自iPhone+微信浏览器的请求——有人点击了你分享的链接（可能是微信/朋友圈）。他们问了一个问题后就离开了。
- 11:53来自CF IP 69.63.219.52的Safari请求，可能是你在其他网络测试，或是同一运营商NAT下的其他人。
- 其他所有请求都是你通过code-server浏览器（8081 localhost）进行的测试。

**背景噪音**（均为404，无真实用户）：
- Runpod内部IP（100.64.1.x）轮询`/robots.txt`、`/sitemap.xml`、`/favicon.ico`、`/apple-touch-icon.png`
- 部分请求访问`/api/status?token=z9cgjolmphbkms0ui0je`——监控脚本寻找不存在的API状态端点

**结论**：使用量极低。只有你加上可能一位来自微信的好奇用户。无持续流量。