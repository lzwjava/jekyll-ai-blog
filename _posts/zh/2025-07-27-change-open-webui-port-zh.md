---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修改OpenWebUI端口
translated: true
type: note
---

在使用 `open-webui serve` 命令运行 Open WebUI 时（通常通过 pip 安装后），如需更改端口，请使用 `--port` 标志后接所需端口号。默认端口为 8080。

### 操作步骤：
1. 确保已安装 Open WebUI：
   ```
   pip install open-webui
   ```

2. 在指定端口运行服务（例如 3000）：
   ```
   open-webui serve --port 3000
   ```

   - 这将使 WebUI 可通过 `http://localhost:3000`（或您的服务器 IP 地址加新端口）访问
   - 注意：使用 `serve` 命令时 `PORT` 环境变量将被忽略，必须使用 `--port` 标志

若使用 Docker 而非直接安装：
- 设置 `PORT` 环境变量，例如 `docker run -e PORT=3000 ...`
- 通过 `-p <主机端口>:3000` 进行外部端口映射（按需调整）

完整安装和配置详情请参阅官方文档。

[环境变量配置 | Open WebUI](https://docs.openwebui.com/getting-started/env-configuration/)
[快速开始 | Open WebUI](https://docs.openwebui.com/getting-started/quick-start/)
