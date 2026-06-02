---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building Hysteria in C++ Essentials
translated: false
type: note
---

I'll search for information about Hysteria and how to build a similar project in C++.Now let me search for C++ QUIC libraries that would be essential for implementing Hysteria in C++.Let me search for additional supporting libraries needed for HTTP/3 and protocol obfuscation in C++.Let me search for more information about BLAKE2 libraries and connection management tools for C++.Now I have comprehensive information to provide a detailed answer about building Hysteria in C++.

---

**Question:** What if I use C++ to build Hysteria (https://github.com/apernet/hysteria)? What libraries will be needed?

**Answer:**

Building Hysteria in C++ is significantly more complex than Clash-core because Hysteria is powered by a customized QUIC protocol designed to deliver unparalleled performance over unreliable and lossy networks, with the protocol masquerading as standard HTTP/3 traffic making it very difficult for censors to detect and block. Hysteria supports SOCKS5, HTTP Proxy, TCP/UDP forwarding, Linux TProxy, and TUN modes with built-in support for custom authentication, traffic statistics, and access control.

## Core QUIC Transport Libraries

This is the foundation layer. You'll need a robust QUIC implementation:

**1. MsQuic (Recommended for Production)** - MsQuic is Microsoft's implementation of the IETF QUIC protocol, written in C and designed as a general purpose QUIC library with C++ API wrapper classes, optimized for maximal throughput and minimal latency with asynchronous IO and receive side scaling (RSS) support. MsQuic is officially supported on Microsoft Windows, Linux, and Xbox platforms with additional experimental support for macOS and Android.

**2. ngtcp2** - ngtcp2 is a C implementation of the IETF QUIC protocol that can be paired with multiple TLS backends including wolfSSL, OpenSSL, LibreSSL, GnuTLS, and BoringSSL. This is more flexible for customization but requires more integration work.

**3. mvfst (Facebook's Implementation)** - A C++ QUIC implementation optimized for performance, though less production-proven than MsQuic.

## HTTP/3 Protocol Mapping

Since Hysteria masquerades as HTTP/3:

**nghttp3** - nghttp3 is an implementation of RFC 9114 HTTP/3 mapping over QUIC and RFC 9204 QPACK header compression in C that does not depend on any particular QUIC transport implementation. This layer sits above your QUIC transport and handles HTTP/3 framing and semantics.

## Cryptography & TLS Libraries

For the customized QUIC protocol and Salamander obfuscation:

**1. wolfSSL** - wolfSSL is a lightweight SSL/TLS library with support for TLS 1.3 and DTLS 1.3, up to 20 times smaller than OpenSSL, offering progressive ciphers including ChaCha20, Curve25519, and BLAKE2b/BLAKE2s. wolfSSL provides BLAKE2b implementation through the blake2.h header with functions like wc_InitBlake2b, wc_Blake2bUpdate, and wc_Blake2bFinal.

**2. OpenSSL 3.5.0+** - Required if using ngtcp2, with QUIC support APIs for integration.

**3. Crypto++ Library** - Provides comprehensive cryptographic algorithms including BLAKE2s, BLAKE2b, ChaCha20Poly1305, AES, and other authenticated encryption schemes.

## Protocol-Specific Requirements

For Hysteria's Salamander Obfuscation Layer:

The Hysteria protocol supports an optional obfuscation layer called "Salamander" that encapsulates all QUIC packets by calculating a BLAKE2b-256 hash of a randomly generated 8-byte salt appended to a user-provided pre-shared key. This requires:

- BLAKE2b-256 hash implementation (provided by wolfSSL or Crypto++)
- Random number generation (from your crypto library)
- Packet encapsulation/decapsulation logic

## Configuration & Utilities

**YAML Parser** - Same as Clash-core: yaml-cpp or RapidYAML for configuration files

**JSON Library** - For RESTful API responses (nlohmann/json recommended)

**Compression Library** - zlib or brotli if supporting compression

## Recommended Architecture Stack

```
┌─────────────────────────────┐
│   Application Layer         │
│ (SOCKS5, HTTP Proxy, TUN)   │
├─────────────────────────────┤
│   Hysteria Protocol Layer   │
│ (Salamander Obfuscation)    │
├─────────────────────────────┤
│   HTTP/3 Mapping (nghttp3)  │
├─────────────────────────────┤
│   QUIC Transport (MsQuic)   │
├─────────────────────────────┤
│   TLS/Crypto (wolfSSL)      │
├─────────────────────────────┤
│   UDP/Networking (Boost.Asio)│
└─────────────────────────────┘
```

## Key Challenges vs. Clash-core

1. **QUIC Customization** - Hysteria modifies the QUIC protocol, requiring deeper understanding and potential custom QUIC implementation
2. **Packet Obfuscation** - More complex protocol-level modifications than Clash
3. **Performance Critical** - QUIC optimization is crucial for the advertised performance benefits
4. **Cross-platform UDP** - Requires careful handling of UDP for lossy network optimization
5. **Complex Build Dependencies** - Multiple interrelated libraries with specific version requirements

## Build Complexity

Building Hysteria in C++ would be significantly more challenging than Clash-core. Consider starting with:
- MsQuic for QUIC transport (production-ready, well-documented)
- nghttp3 for HTTP/3 compatibility
- wolfSSL for cryptography (includes BLAKE2b)
- Boost.Asio for UDP networking

The main implementation effort would be in the Hysteria protocol layer and the network-specific optimizations for lossy networks.

**References:**

- [Hysteria Protocol Documentation](https://github.com/apernet/hysteria/blob/master/PROTOCOL.md)
- [MsQuic GitHub](https://github.com/microsoft/msquic)
- [ngtcp2 GitHub](https://github.com/ngtcp2/ngtcp2)
- [nghttp3 GitHub](https://github.com/ngtcp2/nghttp3)
- [wolfSSL GitHub](https://github.com/wolfSSL/wolfssl)
- [Crypto++ Library GitHub](https://github.com/weidai11/cryptopp)
