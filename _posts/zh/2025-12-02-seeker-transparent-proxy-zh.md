---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Seeker：透明代理工具
translated: true
type: note
---

问题：GitHub 仓库 <https://github.com/gfreezy/seeker> 是做什么的？

回答：
GitHub 仓库 [gfreezy/seeker](https://github.com/gfreezy/seeker) 是一个主要用 Go 编写的开源工具，它使用 TUN 虚拟网络接口实现透明代理。它能够在 macOS 和 Linux 系统上通过 Shadowsocks、SOCKS5 或 HTTP 等代理无缝路由网络流量（TCP、UDP 和 ICMP/ping）。该项目模拟 Surge 的增强模式用于本地流量拦截，以及网关模式用于代理局域网（LAN）上的设备。

### 主要功能

- **透明代理**: 通过 TUN 拦截和路由流量，无需单独配置应用程序。
- **代理支持**: 优先支持 SOCKS5，然后是 Shadowsocks，最后是 HTTP（注意：HTTP 仅支持 TCP CONNECT，不支持 UDP）。
- **规则引擎**: 使用与 Clash 兼容的规则（例如 DOMAIN、DOMAIN-SUFFIX、IP-CIDR），支持 PROXY、DIRECT、REJECT 或 PROBE 等动作。
- **DNS 处理**: 自动启动本地 DNS 服务器 (127.0.0.1)，并在退出时恢复；支持 Fake-IP 解析以处理 ICMP ping。
- **远程配置**: 从订阅 URL（Base64 编码）或加密的 YAML 文件（使用 ChaCha20-IETF）加载配置。
- **优化**: 基于阈值的服务器切换、故障保护以及连接/读写超时。
- **网关模式**: 通过将 DNS 设置为 0.0.0.0:53 并调整设备网关来代理整个局域网流量。

### 安装

从 [发布页面](https://github.com/gfreezy/seeker/releases) 下载 macOS 或 Linux 的预编译二进制文件，然后使其可执行：

```
chmod +x seeker-osx  # macOS
chmod +x seeker-linux  # Linux
```

从源代码构建：

```
git clone https://github.com/gfreezy/seeker.git
cd seeker
OPENSSL_STATIC=yes cargo build --release
```

二进制文件将位于 `target/release/seeker`。

### 使用示例

使用本地 YAML 配置运行（需要 sudo 来设置 TUN）：

```
sudo seeker --config path/to/config.yml
```

对于远程加密配置：

```
sudo seeker --config-url https://example.com/encrypted-config.txt --key mypassword
```

生成加密配置：

```
seeker --config config.yml --encrypt --key mypassword > encrypted-config.txt
```

一个示例配置可在 [此处](https://github.com/gfreezy/seeker/blob/master/sample_config.yml) 获取，支持原生服务器格式或 Clash 风格的 `proxies`。

### 警告

- 避免 TUN IP 与您的网络冲突；TUN 名称不能重复。
- 在 SOCKS5/HTTP 模式下，将直连域添加到配置中以防止循环。
- 在 macOS 上，请在“系统偏好设置”>“安全与隐私”中允许运行未签名二进制文件。
- Ubuntu 用户可能需要解决 DNS 问题（例如，如果使用 dnsmasq，则禁用 systemd-resolved）。
- 根据 Apache-2.0 或 MIT 许可证授权。

此工具对于需要轻量级、基于规则的代理设置（类似于 Surge 或 Clash 等商业应用）的用户非常有用，尤其是在受审查的网络环境中。

*[GitHub - gfreezy/seeker](https://github.com/gfreezy/seeker)*
