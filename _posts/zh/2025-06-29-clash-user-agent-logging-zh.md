---
audio: false
generated: true
lang: zh
layout: post
title: 记录Clash代理中的User-Agent信息
translated: true
type: note
---

看起来您指的是 **Clash**，这是一款基于规则的代理工具，您希望配置它以打印或记录其 HTTP 请求的 **User-Agent**。根据现有信息，Clash（或其核心，通常称为 `clash-core`）没有内置功能来直接、简单地打印传出请求的 User-Agent。不过，您可以通过利用 Clash 的配置选项、外部工具或调试方法来实现此目的。以下是一个分步指南，帮助您记录或检查通过 Clash 发出的请求的 User-Agent。

---

### 理解上下文
- **Clash** 是一款基于规则路由流量的代理工具，支持 HTTP、SOCKS5、Shadowsocks、V2Ray 等协议。它在网络层和应用层运行。
- **User-Agent** 是一个 HTTP 头，通常由发出请求的客户端应用程序（例如浏览器或 `curl` 等工具）设置，而不是由 Clash 本身设置。Clash 作为代理转发这些请求，除非明确配置，否则可能不会固有地记录或修改 User-Agent。
- 要打印 User-Agent，您需要：
  1.  配置 Clash 以记录 HTTP 头（包括 User-Agent）用于调试。
  2.  使用外部工具（例如代理调试器或网络嗅探器）来检查请求。
  3.  修改 Clash 配置以添加自定义头或使用脚本来记录它们。

由于 Clash 本身没有直接记录 User-Agent 头的配置，您可能需要将 Clash 与其他工具结合使用，或使用特定的配置方法。以下是实现此目的的方法。

---

### 方法 1：在 Clash 中启用详细日志记录并检查日志
Clash 可以在不同级别记录请求，但它本身并不原生记录像 User-Agent 这样的 HTTP 头，除非明确配置或与可以检查流量的工具一起使用。您可以启用详细日志记录并使用工具捕获 User-Agent。

#### 步骤：
1.  **将 Clash 日志级别设置为 Debug**：
    - 编辑您的 Clash 配置文件（`config.yaml`，通常位于 `~/.config/clash/config.yaml` 或使用 `-d` 标志指定的自定义目录）。
    - 将 `log-level` 设置为 `debug` 以捕获请求的详细信息：
      ```yaml
      log-level: debug
      ```
    - 保存配置并重启 Clash：
      ```bash
      clash -d ~/.config/clash
      ```
    - Clash 现在会将更详细的信息记录到 `STDOUT` 或指定的日志文件。但是，这可能不直接包含 User-Agent 头，因为 Clash 主要关注路由和连接细节。

2.  **检查日志**：
    - 检查终端或日志文件（如果已配置）中的日志输出。查找 HTTP 请求详情，但请注意 Clash 的默认日志记录可能不包含完整的 HTTP 头（如 User-Agent）。
    - 如果您没有看到 User-Agent 信息，请继续使用调试代理（见方法 2）或网络嗅探器（方法 3）。

3.  **可选：使用 Clash 仪表板**：
    - Clash 提供了一个基于 Web 的仪表板（例如 YACD `https://yacd.haishan.me/` 或官方仪表板 `https://clash.razord.top/`）来监控连接和日志。
    - 在您的 `config.yaml` 中配置 `external-controller` 和 `external-ui` 以启用仪表板：
      ```yaml
      external-controller: 127.0.0.1:9090
      external-ui: folder
      ```
    - 通过 `http://127.0.0.1:9090/ui` 访问仪表板，并检查 "Logs" 或 "Connections" 选项卡。这可能会显示连接详情，但不太可能直接显示 User-Agent。

#### 局限性：
- Clash 的调试日志侧重于路由和代理决策，而不是完整的 HTTP 头。要捕获 User-Agent，您需要拦截 HTTP 流量，这需要额外的工具。

---

### 方法 2：使用调试代理捕获 User-Agent
由于 Clash 本身不直接记录像 User-Agent 这样的 HTTP 头，您可以将 Clash 的流量通过一个调试代理（如 **mitmproxy**、**Charles Proxy** 或 **Fiddler**）进行路由。这些工具可以拦截并显示完整的 HTTP 请求，包括 User-Agent。

#### 步骤：
1.  **安装 mitmproxy**：
    - 安装 `mitmproxy`，一个流行的用于拦截 HTTP/HTTPS 流量的开源工具：
      ```bash
      sudo apt install mitmproxy  # On Debian/Ubuntu
      brew install mitmproxy      # On macOS
      ```
    - 或者，使用其他代理工具，如 Charles 或 Fiddler。

2.  **配置 Clash 将流量路由通过 mitmproxy**：
    - 默认情况下，Clash 充当 HTTP/SOCKS5 代理。您可以通过将 `mitmproxy` 设置为上游代理来将其链接到 `mitmproxy`。
    - 编辑您的 Clash `config.yaml`，包含一个指向 `mitmproxy` 的 HTTP 代理：
      ```yaml
      proxies:
        - name: mitmproxy
          type: http
          server: 127.0.0.1
          port: 8080  # Default mitmproxy port
      proxy-groups:
        - name: Proxy
          type: select
          proxies:
            - mitmproxy
      ```
    - 保存配置并重启 Clash。

3.  **启动 mitmproxy**：
    - 运行 `mitmproxy` 监听 8080 端口：
      ```bash
      mitmproxy
      ```
    - `mitmproxy` 将显示通过它的所有 HTTP 请求，包括 User-Agent 头。

4.  **发送测试请求**：
    - 使用配置为使用 Clash 作为代理的客户端（例如 `curl`、浏览器或其他工具）。
    - 使用 `curl` 的示例：
      ```bash
      curl --proxy http://127.0.0.1:7890 http://example.com
      ```
    - 在 `mitmproxy` 中，您将看到完整的 HTTP 请求，包括 User-Agent（例如 `curl/8.0.1` 或浏览器的 User-Agent）。

5.  **检查 User-Agent**：
    - 在 `mitmproxy` 界面中，浏览捕获的请求。User-Agent 头将在请求详情中可见。
    - 您也可以将日志保存到文件以供进一步分析：
      ```bash
      mitmproxy -w mitmproxy.log
      ```

#### 注意：
- 如果您使用 HTTPS，需要在客户端设备上安装并信任 `mitmproxy` 的 CA 证书以解密 HTTPS 流量。请按照 `http://mitm.clash/cert.crt` 或 `mitmproxy` 文档中的说明操作。
- 此方法需要链式代理（客户端 → Clash → mitmproxy → 目标），这可能会略微增加延迟，但允许完整检查头信息。

---

### 方法 3：使用网络嗅探器捕获 User-Agent
如果您不想使用链式代理，可以使用像 **Wireshark** 这样的网络嗅探器来捕获和检查通过 Clash 的 HTTP 流量。

#### 步骤：
1.  **安装 Wireshark**：
    - 从 [wireshark.org](https://www.wireshark.org/) 下载并安装 Wireshark。
    - 在 Linux 上：
      ```bash
      sudo apt install wireshark
      ```
    - 在 macOS 上：
      ```bash
      brew install wireshark
      ```

2.  **启动 Clash**：
    - 确保 Clash 正在运行，并使用您所需的配置（例如，HTTP 代理在 7890 端口）：
      ```bash
      clash -d ~/.config/clash
      ```

3.  **在 Wireshark 中捕获流量**：
    - 打开 Wireshark，选择 Clash 正在使用的网络接口（例如，`eth0`、`wlan0` 或用于本地流量的 `lo`）。
    - 应用过滤器以捕获 HTTP 流量：
      ```
      http
      ```
    - 或者，按 Clash HTTP 代理端口（例如 7890）过滤：
      ```
      tcp.port == 7890
      ```

4.  **发送测试请求**：
    - 使用配置为使用 Clash 作为代理的客户端：
      ```bash
      curl --proxy http://127.0.0.1:7890 http://example.com
      ```

5.  **检查 User-Agent**：
    - 在 Wireshark 中，查找 HTTP 请求（例如 `GET / HTTP/1.1`）。双击数据包以查看其详情。
    - 展开 "Hypertext Transfer Protocol" 部分以找到 `User-Agent` 头（例如 `User-Agent: curl/8.0.1`）。

#### 注意：
- 对于 HTTPS 流量，除非您拥有服务器的私钥或使用像 `mitmproxy` 这样的工具来解密流量，否则 Wireshark 无法解密 User-Agent。
- 此方法更复杂，需要熟悉网络数据包分析。

---

### 方法 4：修改 Clash 配置以注入或记录自定义头
Clash 支持在某些代理类型（例如 HTTP 或 VMess）的配置中使用自定义 HTTP 头。您可以配置 Clash 注入特定的 User-Agent 或使用脚本来记录头信息。然而，这对于记录所有请求的 User-Agent 来说不太直接。

#### 步骤：
1.  **添加自定义 User-Agent 头**：
    - 如果您想为测试强制使用特定的 User-Agent，可以修改 `config.yaml` 中的 `proxies` 部分以包含自定义头：
      ```yaml
      proxies:
        - name: my-http-proxy
          type: http
          server: proxy.example.com
          port: 8080
          header:
            User-Agent:
              - "MyCustomUserAgent/1.0"
      ```
    - 这会为通过此代理发送的请求设置一个自定义 User-Agent。但是，它会覆盖客户端原始的 User-Agent，如果您试图记录客户端的 User-Agent，这可能不是您想要的。

2.  **使用脚本规则记录头信息**：
    - Clash 支持使用 `expr` 或 `starlark` 等引擎的基于脚本的规则。您可以编写脚本来记录或处理头信息，包括 User-Agent。[](https://pkg.go.dev/github.com/yaling888/clash)
    - 示例配置：
      ```yaml
      script:
        engine: starlark
        code: |
          def match(req):
            print("User-Agent:", req.headers["User-Agent"])
            return "Proxy"  # Route to a proxy group
      ```
    - 这需要编写自定义脚本，属于高级用法，并且可能并非在所有 Clash 版本中都完全支持。请查阅 Clash 文档了解脚本支持情况。

3.  **使用 mitmproxy 或 Wireshark 验证**：
    - 注入自定义 User-Agent 后，使用方法 2 或方法 3 来确认 User-Agent 是否按预期发送。

#### 局限性：
- 注入自定义 User-Agent 会覆盖客户端的 User-Agent，因此这仅对测试特定 User-Agent 有用。
- 基于脚本的记录是实验性的，可能并非在所有 Clash 版本中都可用。

---

### 方法 5：使用 Clash 的 MITM 代理记录头信息
Clash 支持 **中间人 (MITM)** 代理模式，可以拦截和记录 HTTPS 流量，包括像 User-Agent 这样的头信息。

#### 步骤：
1.  **在 Clash 中启用 MITM**：
    - 编辑 `config.yaml` 以启用 MITM 代理：
      ```yaml
      mitm-port: 7894
      mitm:
        hosts:
          - "*.example.com"
      ```
    - 这配置 Clash 拦截指定域的 HTTPS 流量。

2.  **安装 Clash 的 CA 证书**：
    - Clash 为 MITM 生成一个 CA 证书。在浏览器中访问 `http://mitm.clash/cert.crt` 以下载并安装它。
    - 在您的客户端设备上信任该证书，以允许 Clash 解密 HTTPS 流量。

3.  **检查日志**：
    - 启用 MITM 后，Clash 可能会记录更详细的请求信息，包括头信息。检查终端或仪表板中的日志。
    - 如果头信息未被记录，请使用 `mitmproxy`（方法 2）来捕获解密的流量。

#### 注意：
- MITM 模式需要在所有客户端设备上信任 CA 证书，这对于所有用例可能不切实际。
- 此方法最适合 HTTPS 流量，但需要额外的设置。

---

### 推荐方法
- **首选方法**：使用 **方法 2 (mitmproxy)** 来捕获和记录请求的 User-Agent，这是最简单、最可靠的方法。它是开源的，得到广泛支持，并且专为 HTTP 调试而设计。
- **替代方法**：如果您熟悉网络数据包分析并且不想使用链式代理，请使用 **方法 3 (Wireshark)**。
- **对于高级用户**：如果您需要以编程方式在 Clash 内操作或记录头信息，可以尝试 **方法 4 (自定义头或脚本)**。

---

### 补充说明
- **Clash 文档**：请参阅官方 Clash 文档 (,) 以获取配置详情。GitHub 仓库 (`https://github.com/Dreamacro/clash`) 和 wiki (`https://en.clash.wiki`) 提供了详细指南。[](https://en.clash.wiki/)[](https://en.clash.wiki/configuration/getting-started.html)
- **客户端 User-Agent**：User-Agent 是由客户端（例如浏览器、`curl` 或应用程序）设置的，而不是 Clash。请确保您的客户端发送的是预期的 User-Agent。例如：
  - `curl` 默认使用 `curl/<version>`。
  - 浏览器使用它们自己的 User-Agent 字符串（例如 `Mozilla/5.0 ...`）。
- **测试**：始终使用简单的 HTTP 请求（例如 `curl --proxy http://127.0.0.1:7890 http://example.com`）进行测试以验证设置。
- **安全**：使用 MITM 或调试代理时，请确保您信任 CA 证书和工具，以避免安全风险。

如果您需要进一步的说明或对特定配置的帮助，请提供更多关于您设置的详细信息（例如 Clash 版本、操作系统或特定代理类型），我可以进一步调整说明！
