---
audio: false
generated: true
lang: en
layout: post
title: Java VPN Proxy Client with Netty
translated: false
type: note
---

To build a Clash VPN proxy client in Java using Netty or Spring Boot, we need a robust framework to handle networking, YAML configuration parsing, and proxy protocols like SOCKS, HTTP, and Shadowsocks. Netty is ideal for high-performance networking, while Spring Boot can simplify configuration and dependency management. Below, I’ll outline the core logic, main libraries, and provide a sample implementation focusing on Netty for the networking layer, as it’s better suited for low-level proxy operations. The client will support popular Clash YAML configurations (e.g., for proxies, rules, and DNS).

### Main Logic

1. **Configuration Parsing**:
   - Parse Clash-compatible YAML configuration files (e.g., `config.yaml`) containing proxy servers, rules, and DNS settings.
   - Support common proxy types: HTTP, SOCKS5, Shadowsocks, etc.
   - Map YAML fields to Java objects for easy access.

2. **Proxy Server Setup**:
   - Initialize a Netty server to listen for incoming client connections (e.g., on a local port like 7890).
   - Handle SOCKS5/HTTP proxy protocols to accept client requests.

3. **Routing and Rule Handling**:
   - Implement rule-based routing (e.g., domain, IP, or geo-based) as defined in the YAML config.
   - Route client requests to the appropriate upstream proxy server or direct connection.

4. **Connection Management**:
   - Use Netty’s event-driven model to manage client-to-proxy and proxy-to-destination connections.
   - Support connection pooling and keep-alive for efficiency.

5. **DNS Resolution**:
   - Handle DNS queries as specified in the config (e.g., use upstream DNS or a local resolver).
   - Support DNS over HTTPS (DoH) or other secure protocols if configured.

6. **Protocol Handling**:
   - Implement protocol-specific logic for Shadowsocks (e.g., AEAD encryption), SOCKS5, and HTTP.
   - Use pluggable protocol handlers to support extensibility.

7. **Error Handling and Logging**:
   - Gracefully handle connection failures, invalid configurations, or unsupported protocols.
   - Provide detailed logs for debugging.

### Main Libraries

- **Netty**: For high-performance networking and event-driven I/O. Handles client connections, proxy forwarding, and protocol encoding/decoding.
- **SnakeYAML**: To parse Clash-compatible YAML configuration files.
- **Bouncy Castle**: For cryptographic operations (e.g., Shadowsocks AEAD encryption).
- **SLF4J**: For logging.
- **Apache Commons**: For utility functions (e.g., configuration validation).
- **Jackson (optional)**: If you prefer JSON-like handling for YAML or additional config formats.
- **DNSJava (optional)**: For custom DNS resolution if needed.

### Core Implementation

Below is a simplified Netty-based implementation of a Clash-like VPN proxy client. It focuses on:

- Parsing a Clash YAML config.
- Setting up a SOCKS5 proxy server.
- Forwarding requests to an upstream proxy or destination.
- Basic rule-based routing.

```x-java-source
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

    // Configuration class to hold parsed YAML data
    static class ProxyConfig {
        List<Map<String, String>> proxies;
        List<String> rules;

        public ProxyConfig(Map<String, Object> config) {
            this.proxies = (List<Map<String, String>>) config.get("proxies");
            this.rules = (List<String>) config.get("rules");
        }
    }

    // Load Clash YAML configuration
    public void loadConfig(String configPath) throws Exception {
        Yaml yaml = new Yaml();
        try (FileReader reader = new FileReader(configPath)) {
            config = yaml.load(reader);
            logger.info("Loaded configuration from {}", configPath);
        }
    }

    // Start the proxy server
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
                            // Add SOCKS5 protocol handlers
                            pipeline.addLast(new Socks5ServerEncoder());
                            pipeline.addLast(new Socks5InitialRequestDecoder());
                            pipeline.addLast(new Socks5InitialRequestHandler());
                            pipeline.addLast(new Socks5CommandRequestDecoder());
                            pipeline.addLast(new ProxyHandler(new ProxyConfig(config)));
                        }
                    });

            ChannelFuture future = bootstrap.bind(DEFAULT_PORT).sync();
            logger.info("Proxy server started on port {}", DEFAULT_PORT);
            future.channel().closeFuture().sync();
        } finally {
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }

    // Handle SOCKS5 command requests and route traffic
    static class ProxyHandler extends SimpleChannelInboundHandler<Socks5CommandRequest> {
        private final ProxyConfig config;

        public ProxyHandler(ProxyConfig config) {
            this.config = config;
        }

        @Override
        protected void channelRead0(ChannelHandlerContext ctx, Socks5CommandRequest request) {
            String destination = request.dstAddr() + ":" + request.dstPort();
            logger.info("Handling request for {}", destination);

            // Simple rule-based routing (extend with actual rule parsing)
            String selectedProxy = selectProxy(destination);
            if (selectedProxy != null) {
                logger.info("Routing to proxy: {}", selectedProxy);
                // Implement proxy forwarding logic here
                ctx.write(new DefaultSocks5CommandResponse(
                        Socks5CommandStatus.SUCCESS, request.dstAddrType(),
                        request.dstAddr(), request.dstPort()));
            } else {
                logger.warn("No matching proxy found for {}", destination);
                ctx.write(new DefaultSocks5CommandResponse(
                        Socks5CommandStatus.FAILURE, request.dstAddrType(),
                        request.dstAddr(), request.dstPort()));
            }
        }

        private String selectProxy(String destination) {
            // Implement rule-based proxy selection
            for (String rule : config.rules) {
                // Example: Match domain or IP rules
                if (destination.matches(rule)) {
                    return config.proxies.get(0).get("name"); // Simplified
                }
            }
            return null; // Direct connection or fallback
        }
    }

    // Handle SOCKS5 initial request
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

### Sample YAML Configuration

Here’s an example `config.yaml` compatible with the above code:

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

### Explanation of Core Logic

- **YAML Parsing**: The `loadConfig` method uses SnakeYAML to parse the Clash configuration into a `ProxyConfig` object, which holds proxy definitions and routing rules.
- **Netty Server**: The `start` method sets up a Netty server listening on port 7890, handling SOCKS5 protocol requests using Netty’s built-in SOCKS5 codecs.
- **Request Handling**: The `ProxyHandler` processes SOCKS5 command requests, applies routing rules, and selects an upstream proxy or direct connection.
- **Routing**: The `selectProxy` method (simplified) matches destination addresses against rules to choose the appropriate proxy.
- **Extensibility**: The code is modular, allowing easy addition of new protocols (e.g., Shadowsocks) by extending the `ProxyHandler`.

### Next Steps

1. **Protocol Support**: Add handlers for Shadowsocks (using Bouncy Castle for encryption) and HTTP proxies.
2. **Advanced Routing**: Implement full Clash rule parsing (e.g., GEOIP, DOMAIN-SUFFIX) using regex or a rule engine.
3. **DNS Handling**: Integrate DNSJava or a custom resolver for Clash’s DNS settings.
4. **Connection Pooling**: Use Netty’s `ChannelPool` for efficient upstream connections.
5. **Spring Boot (Optional)**: If you prefer Spring Boot, use it for configuration management and REST endpoints for monitoring, but keep Netty for the core proxy logic.

### Dependencies (Maven)

Add these to your `pom.xml`:

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

This provides a foundation for a Clash-like VPN proxy client. You can extend it by adding support for more protocols, advanced routing, and DNS features based on your needs. Let me know if you want to dive deeper into any specific part!
