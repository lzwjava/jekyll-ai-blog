---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SOCKS5代理测试与结果
translated: true
type: note
---

```
测试结果
============

1. macOS nc -X 5：已损坏
   - SOCKS5 握手失败："banner line contains invalid characters"
   - 无法使用

2. ncat 与 connect 的吞吐量对比（git fetch pytorch depth=50，各运行 3 次）：
   ncat：    9.6秒，6.1秒，11.8秒
   connect：13.1秒，7.9秒，11.3秒
   → 在网络波动范围内结果相同

3. SSH 握手延迟（各运行 3 次）：
   ncat：    2.5秒，2.6秒，2.5秒
   connect：2.3秒，2.8秒，2.3秒
   → 结果相同

结论
=======
瓶颈在于你的 SOCKS5 代理（mihomo）和 GitHub 服务器，而非中继工具。ncat 和 connect 速度相当。

配置已更新为使用 connect——它是一个更简洁的 100KB 工具，而 ncat 依赖于 nmap 的 nsock 引擎。

~/.ssh/config 现在：
  ProxyCommand connect -S localhost:7891 -5 %h %p

对于大型模型仓库传输，真正的加速方案仍是你已在使用的方法——通过 HTTPS 远程仓库（ghfast.top 镜像）完全绕过 SSH。
```
