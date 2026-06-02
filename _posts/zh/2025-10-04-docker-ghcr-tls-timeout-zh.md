---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复Docker GHCR TLS连接超时错误
translated: true
type: note
---

您遇到的错误 `Get "https://ghcr.io/v2/": net/http: TLS handshake timeout` 通常表示 Docker 从 GitHub 容器注册表（GHCR）拉取镜像时出现网络问题。以下是排查和解决此问题的步骤：

---

### 1. **检查网络连接**
- 确保您的设备具有稳定的互联网连接。
- 尝试在浏览器中访问 `https://ghcr.io` 以确认能够正常访问该网站。

---

### 2. **检查 Docker 守护进程状态**
- 重启 Docker 守护进程：
  ```bash
  sudo systemctl restart docker
  ```
- 验证 Docker 是否正在运行：
  ```bash
  sudo systemctl status docker
  ```

---

### 3. **配置 Docker DNS**
- 如果您处于企业网络或代理之后，Docker 可能需要自定义 DNS 设置。
- 编辑或创建 `/etc/docker/daemon.json` 文件：
  ```json
  {
    "dns": ["8.8.8.8", "1.1.1.1"]
  }
  ```
- 重启 Docker：
  ```bash
  sudo systemctl restart docker
  ```

---

### 4. **检查代理设置**
- 如果您使用代理，请配置 Docker 使用代理：
  ```bash
  mkdir -p ~/.docker
  echo '{
    "proxies": {
      "default": {
        "httpProxy": "http://your-proxy-address:port",
        "httpsProxy": "http://your-proxy-address:port",
        "noProxy": "localhost,127.0.0.1"
      }
    }
  }' > ~/.docker/config.json
  ```
- 将 `your-proxy-address:port` 替换为您的实际代理地址和端口。

---

### 5. **手动重试拉取镜像**
- 尝试手动拉取镜像以确认问题是否持续存在：
  ```bash
  docker pull ghcr.io/librechat/librechat:latest
  ```
- 如果成功，请重新运行 `docker-compose up -d`。

---

### 6. **检查防火墙/网络限制**
- 确保您的防火墙或网络没有阻止访问 `ghcr.io`。
- 临时禁用防火墙进行测试：
  ```bash
  sudo ufw disable
  ```
  （测试完成后如需可重新启用。）

---

### 7. **更新 Docker 和 Docker-Compose**
- 确保您使用的是最新版本：
  ```bash
  sudo apt update && sudo apt upgrade docker-ce docker-compose-plugin
  ```

---

### 8. **设置 UID/GID 环境变量**
- 关于 `UID` 和 `GID` 的警告并非关键错误，但您可以在 `.env` 文件或 `docker-compose.yml` 中设置它们以消除警告：
  ```bash
  echo "UID=$(id -u)" >> .env
  echo "GID=$(id -g)" >> .env
  ```

---

### 9. **使用其他注册表镜像（可选）**
- 如果 GHCR 持续无法访问，可以尝试使用镜像（但不建议用于生产环境）：
  ```json
  {
    "registry-mirrors": ["https://mirror.example.com"]
  }
  ```
  将此内容添加到 `/etc/docker/daemon.json` 并重启 Docker。

---

### 10. **检查时间同步**
- 确保系统时间已同步：
  ```bash
  sudo apt install ntp
  sudo systemctl restart ntp
  ```

---

### 命令摘要表

| 步骤 | 命令/操作 |
|------|-----------|
| 重启 Docker | `sudo systemctl restart docker` |
| 检查 Docker 状态 | `sudo systemctl status docker` |
| 配置 DNS | 编辑 `/etc/docker/daemon.json` |
| 手动拉取镜像 | `docker pull ghcr.io/librechat/librechat:latest` |
| 设置 UID/GID | `echo "UID=$(id -u)" >> .env` |

---

如果尝试上述步骤后问题仍然存在，请提供以下命令的输出：
```bash
docker info
```
以及运行上述命令时看到的任何错误信息。这将有助于进一步诊断问题！
