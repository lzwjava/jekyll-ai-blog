---
audio: false
generated: true
image: false
lang: en
layout: post
title: Change Open WebUI Port
translated: false
type: note
---

To change the port when running Open WebUI using the `open-webui serve` command (typically after installing via pip), use the `--port` flag followed by your desired port number. The default port is 8080.

### Steps:
1. Ensure Open WebUI is installed:
   ```
   pip install open-webui
   ```

2. Run the server on a different port (e.g., 3000):
   ```
   open-webui serve --port 3000
   ```

   - This will make the WebUI accessible at `http://localhost:3000` (or your server's IP address with the new port).
   - Note: The `PORT` environment variable is ignored when using the `serve` command; you must use the `--port` flag instead.

If you're using Docker instead of direct installation:
- Set the `PORT` environment variable, e.g., `docker run -e PORT=3000 ...`.
- Map the port externally with `-p <host_port>:3000` (adjust as needed).

For full installation and configuration details, refer to the official documentation.

[Environment Variable Configuration | Open WebUI](https://docs.openwebui.com/getting-started/env-configuration/)
[Quick Start | Open WebUI](https://docs.openwebui.com/getting-started/quick-start/)
