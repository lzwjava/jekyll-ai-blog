---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 远程Mihomo设置已完成
translated: true
type: note
---

完成 ✅ mihomo 已完全配置并在 `lzw@192.168.1.46` 上运行。

## 摘要

| 项目 | 状态 |
|------|------|
| **二进制文件** | `/usr/local/bin/mihomo` v1.19.32（适用于 AMD Athlon X4 850 的兼容构建） |
| **配置** | 已将笔记本电脑的 `~/.config/mihomo/` → `/etc/mihomo/`（config.yaml、Rules/、geoip.metadb） |
| **systemd 服务** | `/etc/systemd/system/mihomo.service` — `active`（活动）+ `enabled`（启用）（开机自启） |
| **代理** | 端到端工作正常（已通过 `https://www.gstatic.com/generate_204` 测试 `204 OK`） |

## 监听端口（与你的笔记本电脑相同）

- `7890` — HTTP 代理
- `7891` — SOCKS5 代理
- `7892` — 混合 HTTP+SOCKS 代理
- `9090` — RESTful API（外部控制器）
- `53` — DNS（⚠️ 已跳过，systemd-resolved 占用了该端口——与你的笔记本电脑相同的非致命行为）

## 重要说明

1. **节点选择已修正** — 配置的第一个节点 "My SS 1"（`5.223.42.176:19400`）在两台机器上均已失效。我已将远程的 `Proxy` 组切换到 **"My Hysteria2 2"**（与你的笔记本电脑当前选择一致），并验证其工作正常（204 OK）。该选择已持久化到 `cache.db` 中。

2. **安全注意事项**（与你的笔记本电脑相同，仅供参考）— `external-controller: 0.0.0.0:9090` **没有密钥/认证**，且 `allow-lan: true`。局域网内的任何人都可以控制 mihomo 或将其用作代理。如果此机器暴露在家庭局域网之外，请考虑在配置中添加 `secret`。

3. 以后管理它：
   ```bash
   systemctl status mihomo      # 检查状态
   systemctl restart mihomo     # 重启
   mihomo -d /etc/mihomo -t     # 测试配置有效性
   ```

需要我为安全添加 API `secret`，或调整其他内容吗？