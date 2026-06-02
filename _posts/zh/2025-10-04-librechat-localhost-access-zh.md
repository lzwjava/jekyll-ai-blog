---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 解决LibreChat本地访问问题
translated: true
type: note
---

### 解决 LibreChat 在 localhost:3080 的访问问题

根据日志显示，Docker 镜像已成功拉取（尽管最初出现超时和重试），并启动了 6 个组件：默认网络、`vectordb`、`chat-mongodb`、`chat-meilisearch`、`rag_api` 和 `LibreChat`。但 `api` 服务（通常在端口 3080 提供后端服务）未出现在已启动的容器列表中——这很可能是无法访问网站的原因。`LibreChat` 容器可能是前端，它依赖于 `api` 后端。

UID/GID 警告提示可能存在权限问题，导致 `api` 容器无法正常启动。以下是诊断和修复问题的分步指南。

#### 1. **验证运行中的容器和端口**
   运行以下命令查看所有活动容器、状态及端口映射：
   ```
   docker ps
   ```
   - 查找 `api` 容器（可能命名为 `librechat_api` 或类似名称）。如果缺失或已退出，即为问题所在。
   - 确认端口 `3080` 是否已映射（例如 `0.0.0.0:3080->3080/tcp`）。若未映射，则服务未暴露该端口。
   - 如果无容器显示端口 3080，请继续下一步。

#### 2. **检查容器日志**
   检查启动错误日志，特别是 `api` 和 `LibreChat` 服务：
   ```
   docker logs LibreChat
   docker logs api  # 如果命名不同，使用 docker logs librechat_api
   docker logs rag_api  # 检查依赖问题
   ```
   - 常见错误：权限被拒绝（因 UID/GID 导致）、MongoDB/Meilisearch 连接失败或绑定问题（例如未监听 0.0.0.0）。
   - 如果日志显示服务器已启动但仅绑定到容器内的 localhost，请在 `.env` 文件中添加 `HOST=0.0.0.0`。

#### 3. **设置 UID 和 GID 修复权限警告**
   您的 `.env` 文件（从 `.env.example` 复制）中这些变量可能被注释。未设置的变量可能因文件权限不匹配导致容器静默失败。
   - 编辑 `.env`：
     ```
     UID=1000  # 运行 `id -u` 获取用户 ID
     GID=1000  # 运行 `id -g` 获取组 ID
     ```
   - 保存后重启：
     ```
     docker compose down
     docker compose up -d
     ```
   这确保卷（如 config/logs）由您的用户拥有。

#### 4. **测试连接性**
   - 检查端口 3080 是否在本地监听：
     ```
     curl -v http://localhost:3080
     ```
     - 如果超时或连接被拒绝，表示服务未运行/未暴露。
   - 如果 `docker ps` 显示端口已映射但 curl 失败，请检查防火墙（例如 `sudo ufw status`）或尝试 `http://127.0.0.1:3080`。

#### 5. **如需其他修复**
   - **镜像拉取问题**：首次尝试时出现 `ghcr.io/v2/librechat/librechat/manifests/latest` 的 "denied" 错误。如果再次拉取失败，请向 GitHub 容器注册表认证：
     ```
     echo $YOUR_GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
     ```
     （在 github.com/settings/tokens 创建具有 `read:packages` 范围的个人访问令牌。）
   - **使用推荐的 Compose 文件**：默认的 `docker-compose.yml` 用于本地构建，可能不稳定。切换到 `deploy-compose.yml` 以使用稳定的远程镜像：
     - 重命名或备份当前的 `docker-compose.yml`。
     - 改用 `deploy-compose.yml`：`docker compose -f deploy-compose.yml up -d`。
     - 确保 `.env` 中设置 `HOST=0.0.0.0` 和 `NODE_ENV=production`。
   - **完全重启并清理**：如果问题依旧，清理环境：
     ```
     docker compose down -v  # 同时删除卷
     docker system prune -f
     docker compose up -d
     ```
   - **依赖项**：确认 MongoDB 和 Meilisearch 运行正常（`docker logs chat-mongodb` 等）。`api` 依赖这些服务。

完成以上步骤后，重新尝试访问 http://localhost:3080。如果日志显示特定错误（例如 Mongo 连接问题），请分享错误信息以获取更有针对性的帮助。一旦 UID/GID 和依赖项配置正确，此设置对大多数用户有效。

[本地 Docker 构建无法在 localhost:3080 提供服务](https://github.com/danny-avila/LibreChat/discussions/3425)
[LibreChat Docker 文档](https://www.librechat.ai/docs/local/docker)
[环境文件配置（UID/GID）](https://www.librechat.ai/docs/configuration/dotenv)
