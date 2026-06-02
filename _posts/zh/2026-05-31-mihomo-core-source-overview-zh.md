---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mihomo 核心源码概述
translated: true
type: note
---

完成。源代码在 ~/projects/mihomo — 这才是正主：

```
~/projects/mihomo/
├── 836 个 Go 文件，122K 行代码
├── main.go（入口）
├── go.mod（模块：github.com/metacubex/mihomo，go 1.20）
├── adapter/       — 出站适配器（Shadowsocks、VMess、Trojan 等）
├── common/        — 工具、池、实用函数
├── component/     — DNS、TLS、认证
├── config/        — 配置解析、规则提供者
├── constant/      — 枚举、常量
├── dns/           — DNS 解析器
├── listener/      — 入站监听器（mixed、redir、TUN、TUIC、Hysteria2）
├── rules/         — 路由规则
├── transport/     — 底层传输
└── tunnel/        — 核心隧道逻辑
```

注意：`main` 分支已被一个无关的 Python 库替换，因此我们改为从 `v1.19.25` 标签克隆。Go 源代码存在于发布标签中。
