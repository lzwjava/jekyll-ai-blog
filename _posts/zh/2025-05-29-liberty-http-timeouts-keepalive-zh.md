---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: 配置Liberty HTTP超时与Keep-Alive设置
translated: true
type: note
---

### 配置 Keep-Alive 设置

WebSphere Liberty Profile 通过 `server.xml` 中的 `<httpEndpoint>` 元素处理 HTTP keep-alive 连接。该元素用于控制持久连接以降低延迟和开销。

- **keepAlive**：启用或禁用 keep-alive 功能。设置为 `true`（默认值）允许在单个连接上处理多个请求。
- **keepAliveTimeout**：定义服务器在关闭空闲 keep-alive 连接前的等待时间（以秒为单位）。默认值为 30 秒。

配置时，请在 `server.xml` 的 `<server>` 根节点下添加或修改 `<httpEndpoint>` 元素。示例：

```xml
<server>
    <!-- 其他配置 -->
    <httpEndpoint id="defaultHttpEndpoint" host="*"
        keepAlive="true"
        keepAliveTimeout="60"/>
</server>
```

修改后需重启服务器使配置生效。如需调整 TCP 层级的 keep-alive 设置，可通过 `<tcpOptions>` 进行配置，但 HTTP keep-alive 更常用于 Web 流量场景。

### 配置超时设置

Liberty 的 `server.xml` 中的超时设置主要涉及 `<httpEndpoint>` 下的连接超时参数，用于控制服务器等待操作完成的时间。这些设置适用于 HTTP 通信场景。

- **connectionTimeout**：建立新连接的最大等待时间（以秒为单位）。默认值为 60 秒。
- **readTimeout**：在请求过程中等待传入数据的最大时间（以秒为单位）。默认值为 60 秒。
- **writeTimeout**：等待传出数据发送完成的最大时间（以秒为单位）。默认值为 60 秒。

会话相关的超时设置（例如 Web 应用会话）需在 `web.xml` 或 `server.xml` 的 `<sessionManager>` 中配置，而非直接在 `<httpEndpoint>` 中设置。

`server.xml` 配置示例：

```xml
<server>
    <!-- 其他配置 -->
    <httpEndpoint id="defaultHttpEndpoint" host="*"
        connectionTimeout="30"
        readTimeout="120"
        writeTimeout="120"/>
</server>
```

请根据应用程序的实际需求调整参数值，例如在慢速网络或长时运行请求场景中可适当增加超时设置。建议监控日志中的超时相关错误，配置修改后需重启服务器。更多详细信息请参阅 [IBM Liberty 关于 HTTP 端点的官方文档](https://www.ibm.com/docs/en/was-liberty/23.0.0?topic=configuration-http-endpoint-running-liberty)。
