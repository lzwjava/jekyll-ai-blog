---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: Docker注册表连接超时故障排查
translated: true
type: note
---

您遇到的错误 `Error response from daemon: Get "https://registry-1.docker.io/v2/": net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)` 表明 Docker 客户端因超时无法连接到 Docker Hub 仓库。这可能是由网络问题、认证问题或配置错误引起的。既然您正在尝试基于网页的登录，让我们逐步排查并解决这个问题。

### 问题解决步骤

1. **验证网络连接**
   - 确保您的互联网连接稳定。
   - 通过运行以下命令测试与 Docker Hub 的连接性：

     ```bash:disable-run
     ping registry-1.docker.io
     ```

     或

     ```bash
     curl -v https://registry-1.docker.io/v2/
     ```

     如果这些命令失败，您可能存在网络问题（例如，防火墙、代理或 DNS 问题）。

2. **检查基于网页的认证**
   - 消息表明您正在使用一次性设备确认码 (`LVFK-KCQX`)。请确保您：
     - 按下了 `ENTER` 键以打开浏览器，或手动访问了 `https://login.docker.com/activate`。
     - 在浏览器中正确输入了该确认码。
     - 在超时期限内在浏览器中完成了认证过程。
   - 如果浏览器没有自动打开，请手动访问该 URL 并输入确认码。
   - 如果认证失败或超时，请尝试重新启动该过程：

     ```bash
     docker login
     ```

3. **处理超时问题**
   - 超时错误表明 Docker 客户端无法连接到仓库。通过设置 `DOCKER_CLIENT_TIMEOUT` 环境变量来增加超时时间：

     ```bash
     export DOCKER_CLIENT_TIMEOUT=120
     export COMPOSE_HTTP_TIMEOUT=120
     docker login
     ```

     这将超时时间延长至 120 秒。

4. **检查代理或防火墙问题**
   - 如果您在代理后面，请配置 Docker 使用它。编辑或创建 `~/.docker/config.json` 并添加：

     ```json
     {
       "proxies": {
         "default": {
           "httpProxy": "http://<proxy-host>:<proxy-port>",
           "httpsProxy": "https://<proxy-host>:<proxy-port>",
           "noProxy": "localhost,127.0.0.1"
         }
       }
     }
     ```

     将 `<proxy-host>` 和 `<proxy-port>` 替换为您的代理详细信息。
   - 如果有防火墙阻止访问，请确保允许 `registry-1.docker.io` 和 `login.docker.com`。

5. **使用凭据助手（可选但推荐）**
   - 关于 `~/.docker/config.json` 中未加密凭据的警告建议设置一个凭据助手。安装一个凭据助手，如 `docker-credential-pass` 或 `docker-credential-secretservice`：
     - 对于使用 `pass` 的 Linux 系统：

       ```bash
       sudo apt-get install pass
       curl -fsSL https://github.com/docker/docker-credential-helpers/releases/download/v0.7.0/docker-credential-pass-v0.7.0-amd64.tar.gz | tar -xz
       sudo mv docker-credential-pass /usr/local/bin/
       ```

       初始化 `pass`：

       ```bash
       gpg2 --gen-key
       pass init <your-gpg-key-id>
       ```

       更新 `~/.docker/config.json` 以使用该助手：

       ```json
       {
         "credsStore": "pass"
       }
       ```

     - 配置凭据助手后重试登录。

6. **回退到命令行登录**
   - 如果基于网页的登录持续失败，请尝试使用您的 Docker Hub 用户名和密码进行命令行登录：

     ```bash
     docker login -u <your-username>
     ```

     在提示时输入您的密码或个人访问令牌 (PAT)。您可以从 Docker Hub 账户设置生成 PAT。

7. **检查 Docker 守护进程状态**
   - 确保 Docker 守护进程正在运行：

     ```bash
     sudo systemctl status docker
     ```

     如果它没有运行，请启动它：

     ```bash
     sudo systemctl start docker
     ```

8. **清除 Docker 配置（最后手段）**
   - 如果问题仍然存在，请清除 Docker 配置文件并重试：

     ```bash
     mv ~/.docker/config.json ~/.docker/config.json.bak
     docker login
     ```

### 补充说明

- **Docker Hub 状态**：通过访问 `https://status.docker.com/` 检查 Docker Hub 是否遇到服务中断。
- **DNS 问题**：如果 `registry-1.docker.io` 无法解析，请尝试在您的网络设置中使用公共 DNS，如 Google (`8.8.8.8`) 或 Cloudflare (`1.1.1.1`)。
- **Docker 版本**：确保您的 Docker 客户端是最新的：

  ```bash
  docker --version
  ```

  如果需要，请按照您操作系统的说明更新 Docker。

### 参考

- [Docker 凭据存储文档](https://docs.docker.com/go/credential-store/)
- [Docker 登录文档](https://docs.docker.com/engine/reference/commandline/login/)
- [Docker Hub 状态](https://status.docker.com/)
