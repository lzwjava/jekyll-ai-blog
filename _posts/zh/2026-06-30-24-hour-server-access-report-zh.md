---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 24小时服务器访问报告
translated: true
type: note
---

已通过SSH连接并检查了所有内容。以下是完整情况：

---

**服务器运行中** 自6月29日04:51 UTC（约24小时），PID 3312，已加载原生nanoGPT检查点。stdout管道至`/workspace/fastapi.log`——日志已被保存。

**发布以来的访问统计（过去约24小时）：**

| 指标 | 计数 |
|---|---|
| **首页访问**（GET /） | 83 |
| **聊天补全**（POST /v1/chat/completions） | **54** |
| 传统补全（POST /v1/completions） | 1 |
| 健康检查（GET /health） | 1 |
| 404 垃圾请求（favicons、apple-touch-icons等） | ~80 |
| 400 错误请求（客户端格式错误） | 2 |

**唯一"用户"组**（RunPod内部IP）访问了聊天端点——这些是经过代理映射的，因此每个组大约对应一个真实用户：

- **100.64.1.99** — 12次补全（最活跃用户）
- **100.64.1.98** — 9次补全
- **100.64.1.97** — 9次补全
- **100.64.1.101** — 8次补全
- **100.64.1.96** — 7次补全
- **100.64.1.100** — 7次补全
- 此外还有127.0.0.1（我自己的本地测试）和100.64.1.33（各1次）

因此大约有 **6个真实用户** 主动尝试了该模型。对于一个公司微信群加内部分享来说，这差不多——人们点击、尝试几个提示词、探索一下。

**另外值得注意的是：**

- 有人从5个不同的代理IP对`/api/status?token=z9cgjolmphbkms0ui0je`爬取了8次——在寻找管理端点。
- 2个请求返回了400 Bad Request——可能是某个API客户端发送了格式错误的JSON。
- 一位Safari用户访问了`/README.md`，referer显示为RunPod代理域名——有人在阅读文档。

**日志保留：**

- `/workspace/fastapi.log` — 15KB，包含自服务器启动以来的所有请求。正在保留。
- `/var/log/nginx/access.log` — 很小（仅15条记录），nginx的logrotate已配置，但nginx不是主要入口。
- **fastapi.log没有日志轮转** — 24小时后15KB尚可，但对于面向生产的实时服务器，你需要logrotate或基于重启的拆分。

需要我添加日志轮转或首页的简单访问计数器吗？
