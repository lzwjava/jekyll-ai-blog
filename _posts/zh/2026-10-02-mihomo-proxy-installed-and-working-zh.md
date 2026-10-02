---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 米霍莫代理已安装并正常工作
translated: true
type: note
---

完成！以下是操作详情：

1. **已下载并安装** `mihomo-linux-amd64-v1.19.32`（60MB，x86_64，静态链接）于 `192.168.1.34`
2. **已启动 mihomo**，使用你现有的配置位于 `~/.config/mihomo/config.yaml`
3. **所有端口均已开启**：
   - `7890` — HTTP proxy ✅
   - `7891` — SOCKS proxy ✅
   - `7892` — Mixed proxy ✅
   - `9090` — External controller ✅

代理正在运行——通过端口7890的HTTP测试返回了 `200`。日志显示它正在加载你的规则集并路由流量。
