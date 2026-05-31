---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mihomo Core Source Overview
translated: false
type: note
---

Done. Source code is at ~/projects/mihomo — the real deal:

```
~/projects/mihomo/
├── 836 Go files, 122K lines of code
├── main.go (entrypoint)
├── go.mod (module: github.com/metacubex/mihomo, go 1.20)
├── adapter/       — outbound adapters (Shadowsocks, VMess, Trojan, etc.)
├── common/        — utilities, pool, utils
├── component/     — DNS, TLS, authentication
├── config/        — config parsing, rule providers
├── constant/      — enums, constants
├── dns/           — DNS resolver
├── listener/      — inbound listeners (mixed, redir, TUN, TUIC, Hysteria2)
├── rules/         — routing rules
├── transport/     — underlying transports
└── tunnel/        — core tunnel logic
```

Note: the `main` branch was replaced with an unrelated Python lib, so we cloned from the `v1.19.25` tag instead. The Go source lives in the release tags.