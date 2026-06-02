---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WhatsApp代理设置要点回顾
translated: true
type: note
---

老板，以下是总结：

---

## WhatsApp 设置——要点回顾

**已完成部分：** 插件已安装，二维码成功扫描，WhatsApp 已链接并连接。

**遇到的主要困难：**

1. **代理必须启用** —— 服务器的直连网络无法维持 WhatsApp WebSocket 连接（408 超时）。在 systemd 服务中设置标准的 `HTTP_PROXY`/`HTTPS_PROXY` 环境变量对 Baileys WebSocket 不起作用。

2. **proxychains4 才是真正解决方案** —— 它在 libc 层面拦截所有 TCP 连接，强制所有流量（包括 Node 的 WebSocket）通过 mihomo 代理。必须使用 `socks5 127.0.0.1 7891`（SOCKS 端口，而非 HTTP 7890 端口）。

3. **Gateway 同样需要 proxychains** —— 必须更新 systemd 服务，用 `proxychains4` 包装网关进程，否则重启后 WhatsApp 会断开连接。

4. **二维码中继速度过慢** —— 等我将二维码转发至网页聊天界面再由您查看时，二维码已刷新多次。最终只能通过 SSH 直接扫码——这是唯一可靠的方法。

**配置变更记录：**

- 安装了 `@openclaw/whatsapp` 插件
- 新增 `channels.whatsapp` 配置，设置 `dmPolicy: "pairing"`
- 更新 systemd 服务，以 `proxychains4` 包装进程
- 代理配置：`/etc/proxychains4.conf` → `socks5 127.0.0.1 7891`

已记录供后续参考。🦞
