---
audio: false
generated: true
lang: en
layout: post
title: Building a Shadowsocks Client with Netty
translated: false
type: note
---

Building a Shadowsocks client like Clash or the original Shadowsocks client using Netty involves understanding the Shadowsocks protocol and leveraging Netty's asynchronous, event-driven network application framework. Here's a breakdown of the steps and key concepts involved:

**1. Understanding the Shadowsocks Protocol**

Before diving into Netty, you need to thoroughly understand the Shadowsocks protocol. At a high level, it involves:

* **Connection Establishment:** A client initiates a connection to a Shadowsocks server.
* **Authentication and Method Negotiation:** The client sends the chosen encryption method and password to the server for authentication.
* **Address Encoding:** The client sends the target address (IP address and port) of the actual destination server in a specific encoded format.
* **Data Forwarding:** After successful authentication and address encoding, all subsequent data exchanged between the client and the Shadowsocks server is encrypted/decrypted using the agreed-upon method.

**Key aspects of the protocol you'll need to implement:**

* **Method and Password Handling:** Storing and sending the chosen encryption method (e.g., `aes-256-cfb`, `chacha20-ietf-poly1305`) and the password.
* **Address Encoding:** Encoding the target address into a specific format (type byte, address, port). The type byte indicates whether the address is an IPv4 address (0x01), an IPv6 address (0x04), or a hostname (0x03).
* **Encryption and Decryption:** Implementing the chosen encryption and decryption algorithms. Libraries like `PyCryptodome` (Python) or `Bouncy Castle` (Java) can be helpful for this.
* **TCP Forwarding:** Establishing a local TCP server that listens for connections from applications and forwards the traffic through the Shadowsocks tunnel.

**2. Setting up a Netty Project**

First, you'll need to include the Netty dependency in your project (e.g., using Maven or Gradle for a Java project).

**3. Core Netty Components for a Proxy Client**

You'll primarily use the following Netty components:

* **`Bootstrap`:** Used to configure and start the client-side application.
* **`EventLoopGroup`:** Manages the event loops that handle I/O operations for the client. You'll typically use `NioEventLoopGroup` for non-blocking I/O.
* **`Channel`:** Represents a network connection.
* **`ChannelPipeline`:** A chain of `ChannelHandler`s that process inbound and outbound events and data.
* **`ChannelHandler`:** Interfaces that you implement to handle specific events and data transformations. You'll create custom handlers for the Shadowsocks protocol.
* **`ByteBuf`:** Netty's buffer for handling binary data.

**4. Implementing the Shadowsocks Protocol with Netty Handlers**

You'll need to create several custom `ChannelHandler`s within your `ChannelPipeline` to implement the Shadowsocks logic. Here's a possible structure:

* **Local Proxy Server Handler (`ChannelInboundHandlerAdapter`):**
    * This handler will run on a local server socket that your applications will connect to (e.g., `localhost:1080`).
    * When a new connection comes in from a local application, this handler will:
        * Establish a connection to the remote Shadowsocks server.
        * Forward the initial connection request (target address) to the Shadowsocks server after encoding it according to the protocol.
        * Manage the flow of data between the local application and the Shadowsocks server.

* **Shadowsocks Client Encoder (`ChannelOutboundHandlerAdapter`):**
    * This handler will be responsible for encoding the data being sent to the Shadowsocks server.
    * It will:
        * Encode the target address according to the Shadowsocks protocol (type, address, port).
        * Encrypt the data using the chosen encryption method.

* **Shadowsocks Client Decoder (`ChannelInboundHandlerAdapter`):**
    * This handler will be responsible for decoding the data received from the Shadowsocks server.
    * It will:
        * Decrypt the received data.

* **Remote Server Forwarding Handler (`ChannelInboundHandlerAdapter`):**
    * This handler will be invoked when data is received from the remote Shadowsocks server.
    * It will forward the decrypted data back to the original local application.

**5. Example Structure of the Netty Pipeline**

Here's a simplified example of how your `ChannelPipeline` might look for the connection to the Shadowsocks server:

```java
public class ShadowsocksClientInitializer extends ChannelInitializer<SocketChannel> {

    private final String serverAddress;
    private final int serverPort;
    private final String method;
    private final String password;

    public ShadowsocksClientInitializer(String serverAddress, int serverPort, String method, String password) {
        this.serverAddress = serverAddress;
        this.serverPort = serverPort;
        this.method = method;
        this.password = password;
    }

    @Override
    protected void initChannel(SocketChannel ch) throws Exception {
        ChannelPipeline pipeline = ch.pipeline();

        // Outbound handlers (data going to the Shadowsocks server)
        pipeline.addLast("encoder", new ShadowsocksClientEncoder(method, password));

        // Inbound handlers (data coming from the Shadowsocks server)
        pipeline.addLast("decoder", new ShadowsocksClientDecoder(method, password));
        pipeline.addLast("remoteForwarder", new RemoteServerForwardingHandler());
    }
}
```

And for the local proxy server:

```java
public class LocalProxyInitializer extends ChannelInitializer<SocketChannel> {

    private final String shadowsocksServerAddress;
    private final int shadowsocksServerPort;
    private final String method;
    private final String password;

    public LocalProxyInitializer(String shadowsocksServerAddress, int shadowsocksServerPort, String method, String password) {
        this.shadowsocksServerAddress = shadowsocksServerAddress;
        this.shadowsocksServerPort = shadowsocksServerPort;
        this.method = method;
        this.password = password;
    }

    @Override
    protected void initChannel(SocketChannel ch) throws Exception {
        ChannelPipeline pipeline = ch.pipeline();

        // Handler to initiate connection to the Shadowsocks server and forward data
        pipeline.addLast("localProxyHandler",
                new LocalProxyHandler(shadowsocksServerAddress, shadowsocksServerPort, method, password));
    }
}
```

**6. Key Implementation Details**

* **Encryption/Decryption Implementation:** You'll need to implement the chosen encryption and decryption algorithms within your `ShadowsocksClientEncoder` and `ShadowsocksClientDecoder`. This will likely involve using external libraries. Be careful with key derivation and initialization vectors if required by the chosen method.
* **Address Encoding in `LocalProxyHandler`:** When the `LocalProxyHandler` receives the initial connection request from the local application, it needs to extract the target address and port and encode them into the Shadowsocks format before sending them to the Shadowsocks server.
* **Connecting to the Shadowsocks Server in `LocalProxyHandler`:** The `LocalProxyHandler` will use a separate Netty `Bootstrap` to establish a connection to the configured Shadowsocks server.
* **Data Forwarding:** Once the connection to the Shadowsocks server is established, the handlers need to efficiently forward data between the local application's connection and the Shadowsocks server's connection. You'll likely need to manage the `Channel` objects for both connections.
* **Error Handling:** Implement proper error handling for network issues, protocol errors, and encryption/decryption failures.
* **Concurrency:** Netty handles concurrency efficiently with its event loop model. Ensure your handlers are designed to be thread-safe if you need to share state.

**7. Starting the Proxy Client**

You'll need to create a main class to start both the local proxy server (listening for local connections) and potentially handle configuration.

```java
public class ShadowsocksClient {

    private final int localPort;
    private final String serverAddress;
    private final int serverPort;
    private final String method;
    private final String password;

    public ShadowsocksClient(int localPort, String serverAddress, int serverPort, String method, String password) {
        this.localPort = localPort;
        this.serverAddress = serverAddress;
        this.serverPort = serverPort;
        this.method = method;
        this.password = password;
    }

    public void run() throws Exception {
        EventLoopGroup bossGroup = new NioEventLoopGroup();
        EventLoopGroup workerGroup = new NioEventLoopGroup();

        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(bossGroup, workerGroup)
             .channel(NioServerSocketChannel.class)
             .childHandler(new LocalProxyInitializer(serverAddress, serverPort, method, password))
             .option(ChannelOption.SO_BACKLOG, 128)
             .childOption(ChannelOption.SO_KEEPALIVE, true);

            ChannelFuture f = b.bind(localPort).sync();
            System.out.println("Shadowsocks client started on port: " + localPort);
            f.channel().closeFuture().sync();
        } finally {
            workerGroup.shutdownGracefully();
            bossGroup.shutdownGracefully();
        }
    }

    public static void main(String[] args) throws Exception {
        // Replace with your configuration
        int localPort = 1080;
        String serverAddress = "your_server_ip";
        int serverPort = 8388;
        String method = "aes-256-cfb";
        String password = "your_password";

        new ShadowsocksClient(localPort, serverAddress, serverPort, method, password).run();
    }
}
```

**8. Advanced Considerations (Like Clash)**

To build a client like Clash, you'd need to consider more advanced features:

* **Multiple Proxy Protocols:** Clash supports various proxy protocols (Shadowsocks, SOCKS5, HTTP). You'd need to add handlers for each protocol.
* **Rule-Based Routing:** Clash allows you to define rules to route traffic based on domain, IP address, GEOIP, etc. This would involve implementing a rule engine within your client.
* **Configuration Management:** Clash uses YAML configuration files. You'd need to implement a way to load and parse such configurations.
* **DNS Handling:** Clash often intercepts DNS requests and routes them through the proxy. You'd need to implement DNS interception and forwarding.
* **UDP Support:** Shadowsocks also supports UDP forwarding. You'd need to implement UDP handling using Netty's UDP capabilities.
* **Plugins and Extensions:** Clash has a plugin system. Implementing such a system would add significant complexity.

**In summary, building a basic Shadowsocks client with Netty involves:**

1.  Understanding the Shadowsocks protocol.
2.  Setting up a Netty project.
3.  Creating custom `ChannelHandler`s for encoding, decoding, and forwarding data.
4.  Implementing the encryption and decryption logic.
5.  Starting a local server to accept connections from applications.
6.  Connecting to the remote Shadowsocks server.

Building a more feature-rich client like Clash requires a much deeper understanding of networking, proxy protocols, and more complex software architecture. Start with a basic Shadowsocks implementation and gradually add features as needed. Remember to consult the official Shadowsocks documentation and Netty examples for more detailed information.
