---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 元内核代理引擎Mihomo
translated: true
type: note
---

什么是 mihomo？
    
    mihomo（Meta Kernel）是 Clash 的一个分支——一个基于规则的网络代理/隧道工具，使用 Go 语言编写。它是许多代理客户端（Clash Verge、ClashX Meta、Stash 等）的底层引擎。你现在正在查看的源码位于 ~/projects/mihomo/。
    
    它的功能：作为本地代理服务器，拦截你的网络流量，应用路由规则，并通过各种代理协议（Shadowsocks、VMess、VLESS、Trojan、Hysteria2、TUIC、WireGuard 等）或直连转发连接。
    
    
    
    项目架构
    
    
    main.go              — 命令行入口：参数解析、配置加载、信号处理
    config/              — YAML 配置解析器（RawConfig -> Config 结构体）
    hub/                 — RESTful API 服务器（代理、规则、DNS、连接的控制器）
    hub/executor/        — 应用解析后的配置：启动监听器、加载代理、应用规则
    adapter/
      inbound/           — 入站连接适配器（HTTP、SOCKS 等）
      outbound/          — 出站代理适配器（ss、vmess、vless、hysteria2 等）
      outboundgroup/     — 代理组（select、url-test、fallback、load-balance、relay）
      provider/          — 代理提供者（HTTP/文件订阅源）
    listener/            — TCP/UDP 监听器（mixed-port、tun、redir、tproxy）
    tunnel/              — 核心数据包路由引擎——匹配规则、选择代理、发起连接
    dns/                 — 完整 DNS 服务器（DoH、DoT、DoQ、fake-ip、redir-host）
    rules/               — 规则实现（DOMAIN、IP-CIDR、GEOIP、RULE-SET、MATCH）
    transport/           — 协议传输层（vmess websocket、vless vision、xhttp 等）
    component/           — 共享组件（geoip、geodata、fakeip 池、进程查找器）
    
    
    数据流：
    1. main.go 读取 config.yaml，调用 hub.Parse()，进而调用 config.Parse()
    2. config/config.go 将 YAML 反序列化为 RawConfig，然后构建 Config（创建代理对象、规则对象、DNS 解析器）
    3. hub/executor 应用配置：启动监听器、创建代理组、加载规则提供者
    4. 当有连接进入时，tunnel/tunnel.go 将其与规则匹配，选择代理/出站，并建立连接
    
    
    
    你的配置（~/.config/mihomo/config.yaml）——工作原理
    
    入站端口：
    - port 7890 — HTTP 代理
    - socks-port 7891 — SOCKS5 代理
    - mixed-port 7892 — 合并的 HTTP+SOCKS5（使用这个即可，其他两个是多余的）
    
    代理（2 个节点）：
    - My SS 1 — Shadowsocks（chacha20-ietf-poly1305）位于 5.223.42.176:19400
    - My Hysteria2 2 — Hysteria2 位于 h2.lzwjava.shop:443（基于 UDP，速度快）
    
    代理组：
    - Proxy — 手动选择组，包含两个节点
    
    DNS（fake-ip 模式）：
    - 监听 0.0.0.0:53
    - 使用中国 DoH（doh.pub、alidns）作为域名服务器
    - Fake-IP 池：198.18.0.1/16 — 向应用返回虚假 IP，然后拦截真实连接
    - 从 fake-ip 中过滤掉本地/局域网域名
    
    规则（流量如何路由）：
    1. 特定域名（linkedin、deepseek、claude、openai 等）→ Proxy
    2. RULE-SET,Global → Proxy（大量被屏蔽/代理的站点）
    3. RULE-SET,China → DIRECT（中国站点直连）
    4. RULE-SET,ChinaIP → DIRECT
    5. 私有 IP（10.x、172.16.x、192.168.x）→ DIRECT
    6. GEOIP,CN → DIRECT（任何中国 IP 直连）
    7. MATCH,Proxy — 其余所有流量 → Proxy
    
    
    
    问题与建议
    
    你的配置中存在的问题：
    
    1. 定义了三个端口——只需一个即可。port、socks-port 和 mixed-port 功能重叠。仅使用 mixed-port: 7892，删除另外两个。mixed-port 同时处理 HTTP 和 SOCKS5。
    
    2. external-controller 未设置 secret。API 在 0.0.0.0:9090 完全开放——局域网内任何人都可以切换你的代理节点、读取连接等。添加 secret: "something-random"。
    
    3. experimental.ignore-resolve-fail: true — 在 Meta mihomo 中已弃用/忽略。不会造成损害，但也不起任何作用。
    
    4. *cfw- 键** 是 Clash for Windows 专用——在 mihomo 中无意义。死配置。
    
    5. 代理上未设置 ip-version——你的 Hysteria2 使用 UDP；明确设置 ip-version: dual 或 ipv4-prefer 可避免 IPv6 解析延迟。
    
    6. DNS 监听：0.0.0.0:53——绑定到 53 端口在 macOS 上需要 root 权限。以 root 运行 mihomo，使用更高端口（例如 1053），或使用 TUN 模式（自动劫持 DNS）。
    
    7. 无后备 DNS / 无 nameserver-policy——你的 DNS 设置可用，但可以更智能。中国域名应使用中国 DNS，国外域名应使用国外 DNS（通过代理）。考虑添加：
       yaml
       nameserver-policy:
         "geosite:cn,private": [223.5.5.5, 119.29.29.29]
         "geosite:geolocation-!cn": [8.8.8.8, 1.1.1.1]
       
    
    8. 未启用 tcp-concurrent: true——开启后，mihomo 可同时竞争 IPv4/IPv6 连接，加快拨号速度。
    
    9. 规则排序可更紧凑——RULE-SET,ChinaIP 之后加 GEOIP,CN 是多余的，因为 ChinaIP 已捕获中国 IP。无害，但增加额外处理。