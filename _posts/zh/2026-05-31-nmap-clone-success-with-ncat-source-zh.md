---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Ncat源码成功克隆Nmap
translated: true
type: note
---

使用凭据管理器通过 HTTPS 克隆成功。结果如下：

```
仓库：https://github.com/nmap/nmap.git
位置：/Users/lzwjava/projects/nmap/
大小：84 MB（浅克隆 --depth 1）
ncat 目录：/Users/lzwjava/projects/nmap/ncat/
```

ncat 源码位于 `/Users/lzwjava/projects/nmap/ncat/` — 你已获得包含 ncat 的完整 nmap 源码树。仓库通过 HTTPS 干净克隆（公开仓库无需认证，凭据管理器作为后备可用）。

关键 ncat 文件：
- `ncat/ncat_main.c` — 入口点
- `ncat/ncat_core.c` — 核心连接逻辑
- `ncat/ncat_ssl.c` — SSL/TLS 支持
- `ncat/ncat_proxy.c` — 代理模式
- `ncat/http.c` — HTTP CONNECT 支持

需要我从源码构建 ncat，还是深入研究某个特定部分？