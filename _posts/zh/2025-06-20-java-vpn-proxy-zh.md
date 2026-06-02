---
audio: false
generated: true
lang: zh
layout: post
title: 基于Netty的Java VPN代理客户端
translated: true
type: note
---

要使用 Netty 或 Spring Boot 构建基于 Java 的 Clash VPN 代理客户端，我们需要一个健壮的框架来处理网络通信、YAML 配置解析以及 SOCKS、HTTP 和 Shadowsocks 等代理协议。Netty 适用于高性能网络通信，而 Spring Boot 可以简化配置和依赖管理。下面我将概述核心逻辑、主要依赖库，并提供一个基于 Netty 网络层的示例实现（因其更擅长底层代理操作）。该客户端将支持主流 Clash YAML 配置（如代理服务器、规则和 DNS 设置）。

### 核心逻辑
1. **配置解析**：
   - 解析兼容 Clash 的 YAML 配置文件（如 `config.yaml`），包含代理服务器、规则和 DNS 设置
   - 支持常见代理类型：HTTP、SOCKS5、Shadowsocks 等
   - 将 YAML 字段映射到 Java 对象以便访问

2. **代理服务器搭建**：
   - 初始化 Netty 服务端监听客户端连接（如本地端口 7890）
   - 处理 SOCKS5/HTTP 代理协议接收客户端请求

3. **路由与规则处理**：
   - 实现基于 YAML 配置的规则路由（如域名、IP 或地理路由）
   - 将客户端请求路由至对应上游代理服务器或直连

4. **连接管理**：
   - 利用 Netty 事件驱动模型管理客户端-代理和代理-目标连接
   - 支持连接池和长连接提升效率

5. **DNS 解析**：
   - 按配置处理 DNS 查询（如使用上游 DNS 或本地解析器）
   - 支持 DNS over HTTPS (DoH) 等安全协议

6. **协议处理**：
   - 实现 Shadowsocks（如 AEAD 加密）、SOCKS5 和 HTTP 的协议逻辑
   - 通过可插拔协议处理器支持扩展

7. **错误处理与日志**：
   - 优雅处理连接失败、无效配置或不支持协议
   - 提供详细调试日志

### 主要依赖库
- **Netty**：用于高性能网络通信和事件驱动 I/O，处理客户端连接、代理转发和协议编解码
- **SnakeYAML**：解析 Clash 兼容的 YAML 配置文件
- **Bouncy Castle**：用于加密操作（如 Shadowsocks AEAD 加密）
- **SLF4J**：日志记录
- **Apache Commons**：工具函数（如配置验证）
- **Jackson（可选）**：用于 YAML 的类 JSON 处理或附加配置格式
- **DNSJava（可选）**：用于自定义 DNS 解析

### 核心实现
以下是简化的 Netty 实现示例，重点包含：
- 解析 Clash YAML 配置
- 搭建 SOCKS5 代理服务器
- 将请求转发至上游代理或目标地址
- 基于规则的基础路由

```java
import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.socksx.v5.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.yaml.snakeyaml.Yaml;

import java.io.FileReader;
import java.util.List;
import java.util.Map;

public class ClashProxyClient {
    private static final Logger logger = LoggerFactory.getLogger(ClashProxyClient.class);
    private static final int DEFAULT_PORT = 7890;
    private Map<String, Object> config;

    // 配置类用于保存解析的 YAML 数据
    static class ProxyConfig {
        List<Map<String, String>> proxies;
        List<String> rules;

        public ProxyConfig(Map<String, Object> config) {
            this.proxies = (List<Map<String, String>>) config.get("proxies");
            this.rules = (List<String>) config.get("rules");
        }
    }

    // 加载 Clash YAML 配置
    public void loadConfig(String configPath) throws Exception {
        Yaml yaml = new Yaml();
        try (FileReader reader = new FileReader(configPath)) {
            config = yaml.load(reader);
            logger.info("已从 {} 加载配置", configPath);
        }
    }

    // 启动代理服务器
    public void start() throws Exception {
        EventLoopGroup bossGroup = new NioEventLoopGroup(1);
        EventLoopGroup workerGroup = new NioEventLoopGroup();
        try {
            ServerBootstrap bootstrap = new ServerBootstrap();
            bootstrap.group(bossGroup, workerGroup)
                    .channel(NioServerSocketChannel.class)
                    .childHandler(new ChannelInitializer<Channel>() {
                        @Override
                        protected void initChannel(Channel ch) {
                            ChannelPipeline pipeline = ch.pipeline();
                            // 添加 SOCKS5 协议处理器
                            pipeline.addLast(new Socks5ServerEncoder());
                            pipeline.addLast(new Socks5InitialRequestDecoder());
                            pipeline.addLast(new Socks5InitialRequestHandler());
                            pipeline.addLast(new Socks5CommandRequestDecoder());
                            pipeline.addLast(new ProxyHandler(new ProxyConfig(config)));
                        }
                    });

            ChannelFuture future = bootstrap.bind(DEFAULT_PORT).sync();
            logger.info("代理服务器已启动，端口 {}", DEFAULT_PORT);
            future.channel().closeFuture().sync();
        } finally {
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }

    // 处理 SOCKS5 命令请求并路由流量
    static class ProxyHandler extends SimpleChannelInboundHandler<Socks5CommandRequest> {
        private final ProxyConfig config;

        public ProxyHandler(ProxyConfig config) {
            this.config = config;
        }

        @Override
        protected void channelRead0(ChannelHandlerContext ctx, Socks5CommandRequest request) {
            String destination = request.dstAddr() + ":" + request.dstPort();
            logger.info("正在处理对 {} 的请求", destination);

            // 简化的基于规则路由（需扩展实际规则解析）
            String selectedProxy = selectProxy(destination);
            if (selectedProxy != null) {
                logger.info("路由至代理: {}", selectedProxy);
                // 在此实现代理转发逻辑
                ctx.write(new DefaultSocks5CommandResponse(
                        Socks5CommandStatus.SUCCESS, request.dstAddrType(),
                        request.dstAddr(), request.dstPort()));
            } else {
                logger.warn("未找到匹配 {} 的代理", destination);
                ctx.write(new DefaultSocks5CommandResponse(
                        Socks5CommandStatus.FAILURE, request.dstAddrType(),
                        request.dstAddr(), request.dstPort()));
            }
        }

        private String selectProxy(String destination) {
            // 实现基于规则的代理选择
            for (String rule : config.rules) {
                // 示例：匹配域名或 IP 规则
                if (destination.matches(rule)) {
                    return config.proxies.get(0).get("name"); // 简化实现
                }
            }
            return null; // 直连或回退
        }
    }

    // 处理 SOCKS5 初始请求
    static class Socks5InitialRequestHandler extends SimpleChannelInboundHandler<Socks5InitialRequest> {
        @Override
        protected void channelRead0(ChannelHandlerContext ctx, Socks5InitialRequest msg) {
            ctx.write(new DefaultSocks5InitialResponse(Socks5AuthMethod.NO_AUTH));
        }
    }

    public static void main(String[] args) throws Exception {
        ClashProxyClient client = new ClashProxyClient();
        client.loadConfig("config.yaml");
        client.start();
    }
}
```

### 示例 YAML 配置
以下是与上述代码兼容的 `config.yaml` 示例：

```yaml
proxies:
  - name: proxy1
    type: socks5
    server: 192.168.1.100
    port: 1080
  - name: proxy2
    type: http
    server: 192.168.1.101
    port: 8080
rules:
  - DOMAIN,example.com,proxy1
  - IP-CIDR,192.168.0.0/16,DIRECT
```

### 核心逻辑说明
- **YAML 解析**：`loadConfig` 方法使用 SnakeYAML 将 Clash 配置解析为 `ProxyConfig` 对象，其中包含代理定义和路由规则
- **Netty 服务端**：`start` 方法搭建监听 7890 端口的 Netty 服务端，使用 Netty 内置 SOCKS5 编解码器处理协议请求
- **请求处理**：`ProxyHandler` 处理 SOCKS5 命令请求，应用路由规则并选择上游代理或直连
- **路由机制**：`selectProxy` 方法（简化版）根据目标地址匹配规则选择对应代理
- **扩展性**：采用模块化设计，可通过扩展 `ProxyHandler` 轻松添加新协议（如 Shadowsocks）

### 后续开发
1. **协议支持**：为 Shadowsocks（使用 Bouncy Castle 加密）和 HTTP 代理添加处理器
2. **高级路由**：通过正则表达式或规则引擎实现完整 Clash 规则解析（如 GEOIP、DOMAIN-SUFFIX）
3. **DNS 处理**：集成 DNSJava 或自定义解析器以实现 Clash DNS 设置
4. **连接池**：使用 Netty 的 `ChannelPool` 优化上游连接效率
5. **Spring Boot（可选）**：如需 Spring Boot，可将其用于配置管理和监控 REST 接口，但核心代理逻辑仍用 Netty

### 依赖配置（Maven）
在 `pom.xml` 中添加：

```xml
<dependencies>
    <dependency>
        <groupId>io.netty</groupId>
        <artifactId>netty-all</artifactId>
        <version>4.1.111.Final</version>
    </dependency>
    <dependency>
        <groupId>org.yaml</groupId>
        <artifactId>snakeyaml</artifactId>
        <version>2.3</version>
    </dependency>
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-api</artifactId>
        <version>2.0.16</version>
    </dependency>
    <dependency>
        <groupId>org.bouncycastle</groupId>
        <artifactId>bcprov-jdk18on</artifactId>
        <version>1.78.1</version>
    </dependency>
</dependencies>
```

这为 Clash 风格的 VPN 代理客户端提供了基础框架。您可以根据需求扩展更多协议支持、高级路由和 DNS 功能。如需深入了解特定部分，欢迎进一步探讨！
