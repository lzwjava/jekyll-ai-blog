---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 表单数据中的 HTTPS 测试证书
translated: true
type: note
---

Question: form-data GitHub npm 包的 test/fixture 目录中的 key.pem 和 cert.pem 是做什么用的？

Answer:

在 `form-data` npm 包的 GitHub 仓库 (https://github.com/form-data/form-data) 中，`test/fixture` 目录包含用于 integration tests 的 test fixture 文件。具体来说：

- **key.pem**: 这是自签名 SSL 证书的 private key 文件。它被加载并用于在 integration tests 中配置本地 HTTPS server。

- **cert.pem**: 这是自签名 SSL 证书文件 (public key)。它既用于 HTTPS server 配置，也作为 client 侧请求选项中的 Certificate Authority (CA)，以便在测试期间信任该自签名证书。

### 目的与用途

这些文件于 2015 年引入，旨在不依赖外部服务器的情况下实现本地 HTTPS 测试。来自相关 commit（afe1959 和 4d5ec50）的关键更改包括：

- **本地 HTTPS Server 设置**: 在 `static.js` 和 `common.js` 等 helper 文件中，使用 Node.js 的 `https` 模块创建 HTTPS server，配置如下：
  ```js
  const httpsServer = https.createServer({
    key: common.httpsServerKey,  // 从 'test/fixture/key.pem' 加载
    cert: common.httpsServerCert // 从 'test/fixture/cert.pem' 加载
  });
  ```
  该服务器监听一个端口（例如 9443）并响应请求以进行测试。

- **加载文件**: 在 `test/common.js` 中，使用以下代码读取文件：
  ```js
  const fs = require('fs');
  const path = require('path');
  common.httpsServerKey = fs.readFileSync(path.join(__dirname, '..', 'fixture', 'key.pem'));
  common.httpsServerCert = fs.readFileSync(path.join(__dirname, '..', 'fixture', 'cert.pem'));
  ```

- **Integration Test**: 在 `test/integration/test-submit-https.js` 中，`FormData` 实例被提交到本地 HTTPS server（例如 `localhost:9443`）。请求选项包含 `ca: common.httpsServerCert` 以处理自签名证书验证，从而避免拒绝错误。

这种设置允许在受控的本地环境中测试通过 HTTPS 提交 multipart/form-data。该证书在 2019 年进行了更新（commit e90a76a），可能是因为过期或其他维护原因。

请注意，`form-data` 库本身并不处理 HTTP/HTTPS 请求或 TLS 配置——它只负责构建 form-data streams。这些 fixtures 纯粹是为了仓库的 integration tests，以模拟与 HTTPS endpoint 交互的真实场景。

References:

- [https://github.com/form-data/form-data/commit/afe1959ec711f23e57038ab5cb20fedd86271f29](https://github.com/form-data/form-data/commit/afe1959ec711f23e57038ab5cb20fedd86271f29)
- [https://github.com/form-data/form-data/commit/4d5ec50e81109ad2addf3dbb56dc7c134df5ff87](https://github.com/form-data/form-data/commit/4d5ec50e81109ad2addf3dbb56dc7c134df5ff87)
