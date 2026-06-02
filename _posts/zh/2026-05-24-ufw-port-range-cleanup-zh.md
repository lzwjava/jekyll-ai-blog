---
audio: false
generated: true
image: false
lang: zh
layout: post
title: UFW端口范围清理
translated: true
type: note
---

Done. UFW 现已清理完成：

  ✓ 13000-14000/tcp 已移除（IPv4 + IPv6）
  ✓ 13000-14000/udp 已移除（IPv4 + IPv6）
  ✓ 所有必要规则保留（22、80、443）

最终防火墙状态：

  [1] 22/tcp    ALLOW   SSH
  [2] 22/udp    ALLOW   （SSH 发现）
  [3] 443/udp   ALLOW   Hysteria2
  [4] 80/tcp    ALLOW   ACME 验证
  [5-8]         相同规则，IPv6

默认策略：入站拒绝，出站允许。攻击面最小化。
