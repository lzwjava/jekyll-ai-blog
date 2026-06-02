---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 理解CA证书捆绑包
translated: true
type: note
---

### 什么是 cacert.pem？

`cacert.pem`（或类似命名的文件如 `ca-bundle.crt`、`ca-bundle.pem` 或 `ca-certificates.pem`）指的是一个包含一个或多个采用 PEM 格式的证书颁发机构（CA）根证书的文件。PEM 代表隐私增强邮件，这是一种基于文本的编码标准（使用 Base64），它将证书数据包装在类似 `-----BEGIN CERTIFICATE-----` 和 `-----END CERTIFICATE-----` 的标头之间。

- **用途**：这些文件是来自主要证书颁发机构（例如 Let's Encrypt、DigiCert、GlobalSign）的可信根证书的集合。它们允许软件（如 Web 浏览器、服务器或工具）在安全连接（HTTPS）期间验证网站或服务器出示的 SSL/TLS 证书的真实性。
- **在您的示例中**：粘贴的内容是一个过时的 `ca-bundle.crt` 文件（来自 2012 年 10 月），从 Mozilla 的 Firefox 浏览器中提取。它包括诸如 "GTE CyberTrust Global Root" 和 "Thawte Server CA" 之类的根证书，这些证书在当时是受信任的，但此后已过期或被替换。现代的 CA 证书包会定期更新（例如，通过操作系统更新或软件包）。

许多系统和工具使用类似的文件：
- 在 Linux 上：通常位于 `/etc/ssl/certs/ca-certificates.crt`（Debian/Ubuntu）或 `/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem`（Red Hat）。
- 在 macOS 上：是系统钥匙串的一部分。
- 在 Windows 上：存储在证书存储区中。

这些证书为何可信的证据：CA 证书由受信任的实体签名，而像这样的证书包确保了安全的网页浏览。没有它们，SSL 验证将失败，从而存在中间人攻击的风险。有关更新信息，Mozilla 在 https://wiki.mozilla.org/CA 发布当前数据。

### 为什么我们需要它？

CA 证书包对于 SSL/TLS 加密（用于 HTTPS、安全电子邮件等）至关重要，因为它们：
- **验证真实性**：当您连接到像 https://example.com 这样的站点时，服务器会发送其证书。您的客户端（浏览器、curl 等）使用 CA 证书包来检查该证书是否由受信任的根证书签名。如果不是，它会发出警告或阻止连接。
- **防止攻击**：如果没有验证，任何人都可以伪造证书，从而导致网络钓鱼或数据窃听等漏洞。
- **实现安全通信**：它们确保证书在端到端加密中的可信度，这对于电子商务、银行和任何在线服务都至关重要。
- **历史背景**：在 20 世纪 90 年代初，SSL 被开发出来，CA 证书包成为标准（例如，受 IETF 标准如 RFC 5280 针对 X.509 证书的信任）。

如果您的系统缺少最新的证书包，安全站点可能会显示错误（例如，"证书不受信任"）。大多数操作系统会自动维护和更新这些证书包。

### 如何使用它？

具体用法取决于工具或软件。以下是一些常见示例：

#### 1. **在 Curl（命令行工具）中**
   - Curl 默认使用 CA 证书包（来自您系统的存储），但您可以指定一个自定义文件进行验证。
   - 示例：下载一个自定义证书包并将其用于 HTTPS 请求。
     ```
     wget https://curl.se/ca/cacert.pem  # 从 curl 网站获取更新的 CA 证书包
     curl --cacert cacert.pem https://api.github.com  # 针对此证书包进行验证
     ```
     - 如果没有 `--cacert`，curl 可能会在 Linux 上从 `/etc/ssl/certs/ca-certificates.crt` 加载。

#### 2. **在 Apache/Nginx（Web 服务器）中**
   - 配置用于客户端证书认证或 SSL 验证。
   - 在 Apache 的 `httpd.conf` 或虚拟主机中：
     ```
     SSLCACertificateFile /path/to/ca-bundle.crt
     ```
     - 这告诉 Apache 使用该证书包来信任客户端证书或验证上游连接。

#### 3. **在 PHP 或其他语言中**
   - 对于 PHP 中的 cURL：
     ```
     $ch = curl_init();
     curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);  // 启用验证
     curl_setopt($ch, CURLOPT_CAINFO, '/path/to/cacert.pem');  // 指定证书包
     // 发起请求...
     ```
   - Node.js 或 Python（requests 库）有类似的选项来设置自定义 CA 路径。

#### 4. **浏览器使用**
   - 浏览器（Chrome、Firefox）包含内置的 CA 证书包，通常不需要手动配置。如果需要（例如，用于自签名的开发站点），您可以通过设置添加自定义 CA。

#### 5. **通用提示**
   - **保持更新**：CA 证书会过期或被吊销。请从诸如 https://mkcert.dev（用于开发）等来源或您的操作系统包管理器（例如，在 Ubuntu 上使用 `sudo apt-get update ca-certificates`）下载最新的证书包。
   - **安全说明**：仅使用受信任的证书包，以避免接受无效证书。对于测试，您可以使用 OpenSSL 创建自签名证书（例如，`openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365`）。
   - **检查有效性**：使用 `openssl x509 -in cacert.pem -text -noout` 来检查证书的详细信息。

如果这是针对特定应用程序，请提供更多详细信息以获得量身定制的建议！如果您看到错误（例如，"SSL 证书验证失败"），这可能意味着您的证书包已过时或缺失。
