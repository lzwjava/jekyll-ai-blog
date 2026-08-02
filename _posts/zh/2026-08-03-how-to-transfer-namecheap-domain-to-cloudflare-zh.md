---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何将Namecheap域名转移到Cloudflare
translated: true
type: note
---

问题：如何将域名从 Namecheap 转移到 Cloudflare（注册商转移，不仅仅是 DNS）？

答案：

分为两个阶段：（1）先将 DNS 迁移到 Cloudflare；（2）再进行注册转移。Cloudflare 要求域名**在 Cloudflare 上处于活跃状态**后才会接受授权码——你不能先进行注册转移。

**阶段 1 — DNS 切换**
```
1. cloudflare.com → 添加站点 → 输入域名 → 选择免费计划
2. 检查自动扫描的 DNS 记录，修正或添加缺失的记录（MX、TXT/SPF 等）
3. Namecheap 控制面板 → 域名列表 → 管理 → 名称服务器 → 自定义 DNS
   → 设置 Cloudflare 提供的两个名称服务器（例如 <NS1>.cloudflare.com、<NS2>.cloudflare.com）
4. 如果在 Namecheap 启用了 DNSSEC，请先禁用（删除 DS 记录）——不匹配的
   DS 记录会在名称服务器指向 Cloudflare 后导致解析中断
5. 等待 Cloudflare 控制面板显示域名状态为“活跃”（通常几分钟，最长 24 小时）
```

**阶段 2 — 注册商转移**（仅在域名状态为“活跃”后进行）
```
1. 域名在当前注册商处必须已注册超过 60 天、已解锁、且无待续费
2. Namecheap → 域名列表 → 管理 → 共享与转移 → 解锁域名
3. 同一页面 → 请求/显示授权码（EPP 码），发送至注册人邮箱
4. Cloudflare 控制面板 → 域名注册 → 转移域名 → 输入域名
5. 粘贴授权码 → 确认/验证 WHOIS 联系信息 → 支付（Cloudflare 按
   成本价收费，无加价——通常仅为 ICANN 和注册局费用，约 $9-15/年，视 TLD 而定）
6. Namecheap 会发送一封转移确认邮件 → 点击批准（切勿忽略，
   若不操作，注册局层面约 5 天后自动批准，但不要依赖此机制）
7. 转移在几小时到 5 天内完成
```

容易踩坑的地方：
- WHOIS 隐私有时需要根据注册商临时关闭（Namecheap 通常没问题，但请检查）。
- 如果跳过阶段 1，Cloudflare 的“输入授权码”字段实际上会被禁用，直到域名状态变为“活跃”。
- 在转移完全完成前，请将 Namecheap 的名称服务器作为备用记录在记事本中——如果转移中途失败，你不希望同时失去 DNS 控制权。

参考资料：
- [将域名转移到 Cloudflare — Cloudflare Registrar 文档](https://developers.cloudflare.com/registrar/get-started/transfer-domain-to-cloudflare/)
- [如何转移域名 — Cloudflare 学习中心](https://www.cloudflare.com/learning/dns/how-to-transfer-a-domain-name/)
- [Namecheap 到 Cloudflare 域名转移教程](https://syahnurnizam.com/articles/2025/07/how-to-transfer-your-domain-name-from-namecheap-to-cloudflare/)