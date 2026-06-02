---
audio: false
generated: true
lang: zh
layout: post
title: 修复Clash VPN混合内容错误
translated: true
type: note
---

您遇到的错误信息表明 **Clash VPN 应用存在混合内容问题**，具体表现为当页面 `https://clash.razord.top/` 尝试从非安全的 `http://127.0.0.1:9090/` 端点（例如 `http://127.0.0.1:9090/version`）加载资源时。现代浏览器会阻止此类请求，因为它们违反了安全策略，即试图在安全的 HTTPS 页面上加载不安全的 HTTP 内容。此外，由于访问控制限制，还存在 CORS（跨源资源共享）错误。以下是解决此问题的分步指南。

---

### 问题原因
- **混合内容错误**：网页通过 HTTPS 提供服务，但它试图从 `http://127.0.0.1:9090` 获取资源（如版本检查），这是不安全的。浏览器会阻止这些请求，以防止潜在的安全漏洞，例如中间人攻击。
- **CORS 错误**：由于 CORS 策略，浏览器阻止了对 `http://127.0.0.1:9090` 的请求，该策略限制跨源请求，除非服务器明确允许。
- **Clash 上下文**：Clash（或 Clash for Windows）是一个代理应用，可能使用本地服务器（`127.0.0.1:9090`）作为其仪表板或 API。如果此本地服务器不支持 HTTPS 或配置不正确，当通过 HTTPS 网页访问时，就会触发这些错误。

---

### 解决步骤

#### 1. **验证 Clash 核心配置**
   - **检查 Clash 核心是否运行**：确保 Clash 核心（后端服务）正在您的机器上运行并监听 `127.0.0.1:9090`。您可以通过以下方式验证：
     - 打开终端或命令提示符。
     - 运行 `curl http://127.0.0.1:9090/version` 检查端点是否响应并返回 Clash 版本。
     - 如果没有响应，请确保 Clash 服务处于活动状态。重启 Clash for Windows 或 Clash 核心进程。
   - **为 Clash 核心启用 HTTPS**（如果可能）：
     - 某些版本的 Clash（例如 Clash Premium 或 Clash Meta）支持为本地 API 启用 HTTPS。请查阅 Clash 文档或配置文件（通常是 `config.yaml`），寻找为外部控制器（API 端点）启用 HTTPS 的选项。
     - 在配置文件中查找诸如 `external-controller` 或 `external-ui` 的设置。例如：
       ```yaml
       external-controller: 127.0.0.1:9090
       external-ui: <ui路径>
       ```
       如果支持 HTTPS，您可能需要为本地服务器配置证书。这是一个高级操作，可能需要生成自签名证书（请参阅下面的第 4 步）。

#### 2. **通过 HTTP 访问仪表板（临时解决方法）**
   - 如果 Clash 仪表板可以通过 HTTP 访问（例如，使用 `http://clash.razord.top/` 而不是 HTTPS），请尝试在不使用 HTTPS 的情况下加载它，以避免混合内容问题：
     - 打开浏览器并导航至 `http://clash.razord.top/`。
     - 注意：这不推荐用于生产环境，因为 HTTP 不安全。仅用于测试或仅在本地访问仪表板时使用。
   - 如果仪表板要求使用 HTTPS，请继续执行后续步骤以解决根本原因。

#### 3. **将 URL 更新为 HTTPS**
   - 错误信息表明 Clash 仪表板正尝试从 `http://127.0.0.1:9090` 获取资源。如果您可以访问 Clash 仪表板的源代码或配置：
     - 检查前端代码（例如 `index-5e90ca00.js` 或 `vendor-827b5617.js`）中是否有硬编码的 `http://127.0.0.1:9090` 引用。
     - 如果 Clash 核心支持 HTTPS，请将这些引用更新为 `https://127.0.0.1:9090`，或者使用相对 URL（例如 `/version`），让浏览器使用与页面相同的协议。
     - 如果您无法访问源代码，则可能需要配置反向代理（请参阅第 4 步）。

#### 4. **设置带 HTTPS 的反向代理**
   - 为了解决混合内容问题，您可以设置一个反向代理（例如使用 Nginx 或 Caddy），通过 HTTPS 提供 Clash 核心 API（`http://127.0.0.1:9090`）服务。这使得仪表板能够安全地与核心通信。
   - **Nginx 步骤**：
     1. 在您的系统上安装 Nginx（如果尚未安装）。
     2. 为 `127.0.0.1` 生成自签名 SSL 证书：
        ```bash
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout localhost.key -out localhost.crt -subj "/CN=localhost"
        ```
     3. 配置 Nginx 将通过 HTTPS 的请求代理到 `http://127.0.0.1:9090`。创建一个配置文件（例如 `/etc/nginx/sites-available/clash`）：
        ```nginx
        server {
            listen 443 ssl;
            server_name localhost;

            ssl_certificate /path/to/localhost.crt;
            ssl_certificate_key /path/to/localhost.key;

            location / {
                proxy_pass http://127.0.0.1:9090;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }
        }
        ```
     4. 启用配置并重启 Nginx：
        ```bash
        sudo ln -s /etc/nginx/sites-available/clash /etc/nginx/sites-enabled/
        sudo nginx -t
        sudo systemctl restart nginx
        ```
     5. 更新 Clash 仪表板，使其 API 请求使用 `https://localhost:443` 而不是 `http://127.0.0.1:9090`。
     6. 在浏览器中，当提示时接受自签名证书。

   - **使用 Caddy 的替代方案**：Caddy 配置更简单且自动处理 HTTPS：
     1. 安装 Caddy。
     2. 创建一个 `Caddyfile`：
        ```caddy
        localhost:443 {
            reverse_proxy http://127.0.0.1:9090
        }
        ```
     3. 运行 Caddy：`caddy run`。
     4. 更新 Clash 仪表板以使用 `https://localhost:443`。

#### 5. **绕过 CORS 限制（高级）**
   - CORS 错误（`XMLHttpRequest cannot load http://127.0.0.1:9090/version due to access control checks`）表明 Clash 核心服务器未发送适当的 CORS 头。如果您控制 Clash 核心：
     - 修改 Clash 核心配置以包含 CORS 头，例如：
       ```yaml
       external-controller: 127.0.0.1:9090
       allow-cors: true
       ```
       （请查阅 Clash 文档了解确切语法，因为这取决于 Clash 版本。）
     - 或者，第 4 步中的反向代理设置可以通过添加如下头信息来处理 CORS：
       ```nginx
       add_header Access-Control-Allow-Origin "https://clash.razord.top";
       add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
       add_header Access-Control-Allow-Headers "*";
       ```
   - 如果您不控制核心，可以使用浏览器扩展临时绕过 CORS（例如 Chrome 的 "CORS Unblock"），但出于安全原因不推荐这样做。

#### 6. **更新 Clash 或切换到兼容版本**
   - 确保您使用的是最新版本的 Clash for Windows 或 Clash Verge，因为旧版本可能存在错误或缺少对外部控制器的 HTTPS 支持。
   - 查看 Clash GitHub 仓库（`github.com/Dreamacro/clash` 或 `github.com/Fndroid/clash_for_windows_pkg`）以获取更新或报告与混合内容或 CORS 相关的问题。
   - 考虑切换到 **Clash Verge** 或 **Clash Meta**，它们可能对 HTTPS 和现代浏览器安全策略有更好的支持。[](https://clashverge.net/en/tutorial-en/)

#### 7. **在浏览器中允许不安全内容（不推荐）**
   - 作为最后的手段，您可以在浏览器中为 `https://clash.razord.top/` 允许不安全内容：
     - **Chrome**：
       1. 点击地址栏中的锁形图标。
       2. 转到"网站设置" > "不安全内容" > 设置为"允许"。
     - **Firefox**：
       1. 点击锁形图标并转到"连接设置"。
       2. 临时禁用"阻止危险和欺骗性内容"。
     - **警告**：这会绕过安全保护，应仅用于受信任网络上的本地测试。
   - 或者，使用 `--disable-web-security` 标志启动 Chrome（仅用于开发）：
     ```bash
     google-chrome --disable-web-security --user-data-dir="/tmp/chrome_dev"
     ```

#### 8. **检查冲突的扩展或防火墙**
   - 浏览器扩展（例如广告拦截器、隐私工具）或防火墙设置可能会干扰 Clash 的本地服务器。临时禁用扩展或检查防火墙以确保 `127.0.0.1:9090` 可访问。[](https://vpncentral.com/reddit-blocked-by-network-security/)
   - 在 Windows 上，确保 Clash 应用具有防火墙权限：
     - 转到 设置 > 网络和 Internet > Windows 防火墙 > 允许应用通过防火墙。
     - 添加或启用 Clash for Windows。

#### 9. **联系 Clash 支持或社区**
   - 如果上述步骤未能解决问题，请在 Clash for Windows GitHub issues 页面（`github.com/Fndroid/clash_for_windows_pkg/issues`）或 Clash 社区论坛报告此问题。提供您的设置详情，包括：
     - Clash 版本。
     - 操作系统。
     - 配置文件（隐去敏感信息）。
     - 浏览器及版本。
   - 在社区中查看类似问题，因为此错误可能特定于某些 Clash 版本或配置。[](https://superuser.com/questions/1769163/could-not-switch-to-this-profile-proxy-0-filed-ws-opts-headershost-invalid-c)

---

### 推荐方法
最安全、最稳健的解决方案是**设置带 HTTPS 的反向代理**（第 4 步），以确保所有请求都通过 HTTPS 提供服务，从而同时解决混合内容和 CORS 问题。如果您无法修改 Clash 核心或仪表板，使用较新版本的 Clash（例如 Clash Verge）或临时通过 HTTP 访问仪表板（第 2 步）可能是更快的解决方法。

---

### 补充说明
- 如果您使用的是自定义 Clash 仪表板或第三方服务（如 `clash.razord.top`），请确保它与您的 Clash 核心版本兼容。
- 在进行更改之前，始终备份您的 Clash 配置（`config.yaml`）。
- 如果问题仍然存在，您可以尝试切换到其他代理客户端，如 v2rayN 或 OpenVPN，它们可能对本地 API 有更好的 HTTPS 支持。[](https://stackoverflow.com/questions/67822697/how-to-route-internet-traffic-via-clash-for-windows-ping-from-python-code-is)

如果您在具体步骤（例如设置 Nginx 或调试 Clash 配置）上需要帮助，请告诉我！
