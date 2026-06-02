---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: Configuring Liberty HTTP Timeouts and Keep-Alive
translated: false
type: note
---

### Configuring Keep-Alive Settings

WebSphere Liberty Profile handles HTTP keep-alive connections through the `<httpEndpoint>` element in `server.xml`. This element controls persistent connections to reduce latency and overhead.

- **keepAlive**: Enables or disables keep-alive. Set to `true` (default) to allow multiple requests over a single connection.
- **keepAliveTimeout**: Defines how long (in seconds) the server waits before closing an idle keep-alive connection. Default is 30 seconds.

To configure, add or modify the `<httpEndpoint>` element under the `<server>` root in `server.xml`. Example:

```xml
<server>
    <!-- Other configurations -->
    <httpEndpoint id="defaultHttpEndpoint" host="*"
        keepAlive="true"
        keepAliveTimeout="60"/>
</server>
```

Restart the server for changes to take effect. TCP-level keep-alives can be adjusted via `<tcpOptions>` if needed, but HTTP keep-alive is more common for web traffic.

### Configuring Timeout Settings

Timeouts in Liberty's `server.xml` primarily relate to connection timeouts under `<httpEndpoint>`, controlling how long the server waits for operations. These apply to HTTP communication.

- **connectionTimeout**: Maximum time (in seconds) to establish a new connection. Default is 60 seconds.
- **readTimeout**: Maximum time (in seconds) to wait for incoming data during a request. Default is 60 seconds.
- **writeTimeout**: Maximum time (in seconds) to wait for outgoing data to be sent. Default is 60 seconds.

Session-specific timeouts (e.g., for web app sessions) are configured in `web.xml` or via `<sessionManager>` in `server.xml`, not directly in `<httpEndpoint>`.

Example `server.xml` configuration:

```xml
<server>
    <!-- Other configurations -->
    <httpEndpoint id="defaultHttpEndpoint" host="*"
        connectionTimeout="30"
        readTimeout="120"
        writeTimeout="120"/>
</server>
```

Adjust values based on your application's requirements, such as higher timeouts for slow networks or long-running requests. Monitor logs for timeout-related errors and restart the server after changes. For more details, refer to the [IBM Liberty documentation on HTTP endpoints](https://www.ibm.com/docs/en/was-liberty/23.0.0?topic=configuration-http-endpoint-running-liberty).
