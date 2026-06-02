---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Java Proxy Like Clash Guide
translated: false
type: note
---

Question: How to use Java to write a proxy application like Clash, the famous proxy program especially in mainland China? What libraries should we use, what's the architecture, preferring the latest/advanced ones?

Answer:

Building a full-featured proxy client like **Clash** (or modern forks such as ClashMeta / mihomo) in pure Java is challenging and not very common. Clash itself is written in Go and most popular clients (FlClash, Clash Verge, etc.) are wrappers or use other languages. There are almost no mature, actively maintained, full Clash-compatible proxy clients written purely in Java as of 2026.

However, you can build a **powerful local proxy client / transparent proxy tool** in Java that supports multiple protocols (especially SOCKS5 + HTTP(S) inbound, and various outbounds like Shadowsocks, VMess, Trojan, Hysteria2, etc.). Below is a realistic modern approach using the latest/advanced libraries.

### Recommended Modern Stack (2025–2026 style)

- **Language / Runtime**: Java 21+ (or 23) + Virtual Threads (Project Loom) for excellent concurrency with low overhead
- **Core networking framework** — **Netty** (latest 4.1.x or 5 if stable)
  - Almost all high-performance Java proxies are built on Netty
  - Handles TCP/UDP, SSL/TLS, HTTP/2, very efficient event-loop model
- **HTTP client for outbounds** — **java.net.http.HttpClient** (JDK built-in, Java 11+) or **OkHttp 5.x**
  - OkHttp is still very popular for advanced use-cases (better connection pooling, HTTP/3 experimental in some forks)
- **SOCKS5** — Implement manually using Netty (most flexible) or use older **sockslib** (fengyouchao/sockslib — last major update ~2016 but still works)
  - Newer alternative: **jargyle** (Java SOCKS5 server/client API, more modern than sockslib)
- **Shadowsocks** — Use **shadowsocks-netty** or implement AEAD ciphers yourself (chacha20-ietf-poly1305, aes-256-gcm, etc.)
- **VMess / VLESS / Trojan / Reality** — Usually need to port the protocols or embed **Xray-core** / **sing-box** via JNI/JNA — very hard
  - Most practical: implement **only** Shadowsocks + SOCKS5/HTTP inbound + few outbounds
- **TLS** — **Netty** built-in OpenSSL/Conscrypt or JDK SSLEngine
- **Rule engine (like Clash YAML routing)** — Use **Picocli** or **Quarkus** CLI + **Jackson/YAML** parser + custom rule matcher (or embed **Drools** for complex rules, but heavy)
- **Transparent proxy / TUN mode** (very hard in Java)
  - Use **tun2socks** approach + **gVisor** / **lwip** stack in Java (almost impossible)
  - More realistic: only **system proxy** (PAC + HTTP/SOCKS outbound) or **per-app proxy** via local SOCKS/HTTP server
- **Configuration & GUI** (optional)
  - **Quarkus** or **Spring Boot 3.x** (with virtual threads) for backend server
  - Frontend: **JavaFX** (modern with Gluon) or Electron wrapper + Java backend

### Recommended Architecture (2025 style – similar to sing-box / mihomo spirit)

```
[Apps / Browser / curl]
       ↓
[System Proxy / PAC]  →  Local SOCKS5/HTTP Server (inbound)
                             │
                ┌────────────┼────────────┐
                │            │            │
         Routing Engine   DNS Hijack     Fake-IP
       (YAML / Domain / GeoIP / Process)   (optional)
                │
      ┌─────────┼─────────┬─────────┐
      │         │         │         │
  Direct   Shadowsocks   VMess    Hysteria2 / TUIC
   (outbound)  (outbound)  etc.
      │         │         │
      └─────────┼─────────┘
                ↓
          Remote Server(s)
```

Key components in code:

1. **Inbound server** (SOCKS5 + HTTP)
   - Netty ServerBootstrap → two ports or one with protocol detection
   - SOCKS5 handshake (Netty has codec examples)
   - HTTP CONNECT for HTTPS

2. **Rule-based dispatcher**
   - Parse Clash-like YAML config
   - Use domain trie / GeoIP database (MaxMind GeoLite2)
   - Process name matching (hard — needs JNA + native calls)

3. **Outbound connectors**
   - Direct: just forward socket
   - Shadowsocks: Netty pipeline with SS codec
   - VMess/Trojan: implement protocol or use external core

4. **Connection management**
   - Use Netty `ChannelPool` or OkHttp for HTTP outbounds
   - Virtual threads for each connection (very cheap)

### Quick Start Skeleton (Netty + Java 21)

```java
import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.nio.NioServerSocketChannel;

public class SimpleProxy {
    public static void main(String[] args) throws Exception {
        EventLoopGroup boss = new NioEventLoopGroup(1);
        EventLoopGroup worker = new NioEventLoopGroup(); // virtual threads possible in Netty 5

        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(boss, worker)
             .channel(NioServerSocketChannel.class)
             .childHandler(new ChannelInitializer<Channel>() {
                 @Override
                 protected void initChannel(Channel ch) {
                     // Add SOCKS5 / HTTP codec here
                     ch.pipeline().addLast(new YourSocks5OrHttpHandler());
                 }
             });

            ChannelFuture f = b.bind(1080).sync();
            f.channel().closeFuture().sync();
        } finally {
            boss.shutdownGracefully();
            worker.shutdownGracefully();
        }
    }
}
```

### Realistic Advice in 2026

- If you want **full Clash compatibility** (120+ protocols, TUN, fake-ip, rule-providers, clash meta API): **not practical in pure Java**. Use Go (mihomo) or Rust (sing-box) instead.
- If you want **Java learning project** or **only Shadowsocks + SOCKS5/HTTP**: very doable and educational — use **Netty** + **Jackson** + **Picocli**.
- If you must have Clash-like features in Java ecosystem: consider **JNI/JNA bridge** to mihomo/lib or call sing-box binary as subprocess (like many Clash GUI clients do).

Most advanced Java proxy projects today are either simple HTTP proxies or enterprise reverse proxies — not client-side censorship circumvention tools like Clash.

References:

- [Netty project](https://netty.io)
- [sockslib GitHub](https://github.com/fengyouchao/sockslib)
- [OkHttp](https://square.github.io/okhttp/)
- [jargyle (Java SOCKS5)](https://github.com/jh3nd3rs0n/jargyle)
