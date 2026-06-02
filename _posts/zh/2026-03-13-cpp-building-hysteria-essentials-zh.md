---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 C++ 基础中构建 Hysteria
translated: true
type: note
---

我会搜索有关 Hysteria 的信息以及如何用 C++ 构建类似项目。现在让我搜索实现 Hysteria 在 C++ 中所需的 C++ QUIC 库。让我搜索 C++ 中 HTTP/3 和协议混淆所需的额外支持库。现在让我搜索有关 C++ 的 BLAKE2 库和连接管理工具的更多信息。现在我拥有全面的信息，可以提供有关用 C++ 构建 Hysteria 的详细答案。

---

**问题：** 如果我用 C++ 构建 Hysteria（<https://github.com/apernet/hysteria）？需要哪些库？>

**答案：**

用 C++ 构建 Hysteria 的复杂度远高于 Clash-core，因为 Hysteria 由定制的 QUIC 协议驱动，该协议旨在在不可靠和丢包网络上提供无与伦比的性能，同时协议伪装成标准的 HTTP/3 流量，使审查者难以检测和屏蔽。Hysteria 支持 SOCKS5、HTTP Proxy、TCP/UDP 转发、Linux TProxy 和 TUN 模式，并内置支持自定义认证、流量统计和访问控制。

## 核心 QUIC 传输库

这是基础层。您需要一个健壮的 QUIC 实现：

**1. MsQuic（生产环境推荐）** - MsQuic 是 Microsoft 对 IETF QUIC 协议的实现，用 C 编写，并设计为通用 QUIC 库，带有 C++ API 包装类，针对最大吞吐量和最小延迟进行了优化，支持异步 IO 和接收侧缩放 (RSS)。MsQuic 正式支持 Microsoft Windows、Linux 和 Xbox 平台，并对 macOS 和 Android 提供实验性支持。

**2. ngtcp2** - ngtcp2 是 IETF QUIC 协议的 C 实现，可以与多个 TLS 后端配对，包括 wolfSSL、OpenSSL、LibreSSL、GnuTLS 和 BoringSSL。这更灵活以进行自定义，但需要更多集成工作。

**3. mvfst (Facebook 的实现)** - 一个针对性能优化的 C++ QUIC 实现，虽然不如 MsQuic 那样经过生产验证。

## HTTP/3 协议映射

由于 Hysteria 伪装成 HTTP/3：

**nghttp3** - nghttp3 是 RFC 9114 HTTP/3 over QUIC 和 RFC 9204 QPACK 头部压缩的 C 实现，不依赖于任何特定的 QUIC 传输实现。此层位于您的 QUIC 传输之上，处理 HTTP/3 帧和语义。

## 密码学和 TLS 库

针对定制 QUIC 协议和 Salamander 混淆：

**1. wolfSSL** - wolfSSL 是一个轻量级 SSL/TLS 库，支持 TLS 1.3 和 DTLS 1.3，比 OpenSSL 小高达 20 倍，提供渐进式密码套件，包括 ChaCha20、Curve25519 和 BLAKE2b/BLAKE2s。wolfSSL 通过 blake2.h 头文件提供 BLAKE2b 实现，包含 wc_InitBlake2b、wc_Blake2bUpdate 和 wc_Blake2bFinal 等函数。

**2. OpenSSL 3.5.0+** - 如果使用 ngtcp2，则需要，用于集成 QUIC 支持 API。

**3. Crypto++ Library** - 提供全面的密码算法，包括 BLAKE2s、BLAKE2b、ChaCha20Poly1305、AES 和其他认证加密方案。

## 协议特定要求

针对 Hysteria 的 Salamander 混淆层：

Hysteria 协议支持一个可选的混淆层称为“Salamander”，它通过计算用户提供的预共享密钥附加随机生成的 8 字节 salt 的 BLAKE2b-256 哈希来封装所有 QUIC 数据包。这需要：

- BLAKE2b-256 哈希实现（由 wolfSSL 或 Crypto++ 提供）
- 随机数生成（来自您的密码库）
- 数据包封装/解封装逻辑

## 配置和实用工具

**YAML 解析器** - 与 Clash-core 相同：yaml-cpp 或 RapidYAML 用于配置文件

**JSON 库** - 用于 RESTful API 响应（推荐 nlohmann/json）

**压缩库** - 如果支持压缩，则使用 zlib 或 brotli

## 推荐架构栈

```
┌─────────────────────────────┐
│   应用层                    │
│ (SOCKS5, HTTP Proxy, TUN)   │
├─────────────────────────────┤
│   Hysteria 协议层            │
│ (Salamander 混淆)           │
├─────────────────────────────┤
│   HTTP/3 映射 (nghttp3)     │
├─────────────────────────────┤
│   QUIC 传输 (MsQuic)        │
├─────────────────────────────┤
│   TLS/密码学 (wolfSSL)      │
├─────────────────────────────┤
│   UDP/网络 (Boost.Asio)     │
└─────────────────────────────┘
```

## 与 Clash-core 的关键挑战

1. **QUIC 自定义** - Hysteria 修改了 QUIC 协议，需要更深入的理解和潜在的自定义 QUIC 实现
2. **数据包混淆** - 比 Clash 更复杂的协议级修改
3. **性能关键** - QUIC 优化对于宣传的性能优势至关重要
4. **跨平台 UDP** - 需要仔细处理 UDP 以优化丢包网络
5. **复杂的构建依赖** - 多个相互关联的库，具有特定版本要求

## 构建复杂度

用 C++ 构建 Hysteria 的挑战远高于 Clash-core。考虑从以下开始：

- MsQuic 用于 QUIC 传输（生产就绪，文档完善）
- nghttp3 用于 HTTP/3 兼容性
- wolfSSL 用于密码学（包含 BLAKE2b）
- Boost.Asio 用于 UDP 网络

主要实现工作将集中在 Hysteria 协议层和针对丢包网络的网络特定优化。

**参考资料：**

- [Hysteria Protocol Documentation](https://github.com/apernet/hysteria/blob/master/PROTOCOL.md)
- [MsQuic GitHub](https://github.com/microsoft/msquic)
- [ngtcp2 GitHub](https://github.com/ngtcp2/ngtcp2)
- [nghttp3 GitHub](https://github.com/ngtcp2/nghttp3)
- [wolfSSL GitHub](https://github.com/wolfSSL/wolfssl)
- [Crypto++ Library GitHub](https://github.com/weidai11/cryptopp)
