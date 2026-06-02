---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 配置Docker守护进程代理设置
translated: true
type: note
---

### 配置 Docker 守护进程的代理设置

可以通过配置 Docker 守护进程使用 HTTP/HTTPS 代理，使在企业防火墙后执行拉取镜像或构建容器等操作成为可能。这需要通过编辑（或创建）`/etc/docker/daemon.json` 文件来实现。请注意，此配置适用于守护进程本身（例如用于 `docker pull` 或 `docker build`），而不适用于单个容器（容器将使用环境变量或 Docker 构建参数）。

#### 前提条件

- 您需要在 Linux 系统上拥有 root 或 sudo 权限（这是 Docker 守护进程配置的主要操作系统；在 Windows/Mac 上使用 Docker Desktop 时，请改用 GUI 设置）。
- Docker 已安装并正在运行。
- 了解您的代理服务器详细信息（例如，用于 HTTP/HTTPS 代理的 `http://proxy.company.com:8080`，以及任何 no-proxy 例外）。

#### 分步配置

1. **定位或创建守护进程配置文件**：
   - 打开终端并导航至 `/etc/docker/`（如果目录不存在，则创建它：`sudo mkdir -p /etc/docker`）。
   - 使用文本编辑器编辑 `daemon.json` 文件（例如 `sudo nano /etc/docker/daemon.json` 或 `sudo vim /etc/docker/daemon.json`）。
   - 如果文件不存在，请创建它。如果是新文件，从一个空的 JSON 对象 `{}` 开始。

2. **添加代理配置**：
   - 向 JSON 文件添加一个 `"proxies"` 部分。以下是一个基本示例：

     ```json
     {
       "proxies": {
         "http-proxy": "http://proxy.company.com:8080",
         "https-proxy": "http://proxy.company.com:8080",
         "no-proxy": "localhost,127.0.0.1,*.company.com,10.0.0.0/8"
       }
     }
     ```

     - **说明**：
       - `"http-proxy"`：HTTP 代理的 URL（用于非 HTTPS 请求）。
       - `"https-proxy"`：HTTPS 代理的 URL（通常与 HTTP 代理相同）。
       - `"no-proxy"`：应绕过代理的主机/域/IP 范围列表，以逗号分隔（例如，本地地址或内部域）。这可以防止无限循环。
       - 如果需要身份验证，请使用格式 `http://username:password@proxy.company.com:8080`。
       - 对于 SOCKS 代理，请使用 `"http-proxy": "socks5://proxy.company.com:1080"`。

     - 如果 `daemon.json` 已有现有内容（例如其他设置，如 `"log-driver": "json-file"`），请将 `"proxies"` 部分合并到其中，不要重复键。确保 JSON 语法有效（如果需要，使用 `jsonlint` 等工具进行验证）。

3. **保存并重启 Docker 守护进程**：
   - 保存文件。
   - 重启 Docker 服务以应用更改：

     ```
     sudo systemctl restart docker
     ```

     - 在旧系统或非 systemd 系统上，使用 `sudo service docker restart`。
   - 验证守护进程是否正在运行：

     ```
     sudo systemctl status docker
     ```

     - 如果有问题，请检查日志：`sudo journalctl -u docker.service`。

4. **验证配置**：
   - 通过拉取镜像进行测试（现在应通过您的代理路由）：

     ```
     docker pull hello-world
     ```

   - 通过检查守护进程配置来确认代理设置是否已应用：

     ```
     docker info | grep -i proxy
     ```

     - 您应该看到类似以下的输出：

       ```
       HTTP Proxy: http://proxy.company.com:8080
       HTTPS Proxy: http://proxy.company.com:8080
       No Proxy: localhost,127.0.0.1,*.company.com,10.0.0.0/8
       ```

   - 如果您在构建上下文中使用 Docker，请使用以下命令进行测试：

     ```
     docker build -t test-proxy .
     ```

     （假设使用一个拉取基础镜像的简单 Dockerfile。）

#### 补充说明

- **安全性**：避免在共享系统的 `daemon.json` 中硬编码凭据。如果可能，请使用环境变量，或使用 `docker config` 等工具进行更高级的设置。
- **常见问题**：
  - **语法错误**：无效的 JSON 将阻止守护进程启动。请使用 `cat /etc/docker/daemon.json` 和 JSON 验证器仔细检查。
  - **防火墙/SELinux**：确保您的代理可访问，并且没有安全模块阻止它。
  - **Docker 版本**：此方法适用于 Docker 20.10+（早期版本使用不同的环境变量，如 `HTTP_PROXY`）。使用 `docker --version` 检查您的版本，并在需要时升级。
  - **特定于注册表的代理**：对于私有注册表，您可能需要在 `daemon.json` 中的 `"registry-mirrors"` 或不安全注册表下进行额外配置。
- **对于容器**：如果您需要在*运行中*的容器内部（而不是守护进程）设置代理，请在 Dockerfile 中设置环境变量（例如 `ENV http_proxy=http://proxy.company.com:8080`）或通过 `docker run -e http_proxy=...` 设置。
- **Docker Desktop (Windows/Mac)**：转到 Settings > Resources > Proxies，并在那里启用/配置——无需编辑 JSON。

有关更多详细信息，请参阅官方 Docker 文档：[配置 Docker 守护进程](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file)。如果您遇到错误，请分享确切的输出以进行故障排除！
