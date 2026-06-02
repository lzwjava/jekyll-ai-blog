---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: 无需Docker Compose的LibreChat安装指南
translated: true
type: note
---

是的，你可以不使用 Docker Compose 来设置 LibreChat，只需使用单独的 `docker run` 命令，甚至可以采用非 Docker 方法（手动安装 Node.js、Yarn、MongoDB 和 MeiliSearch）。这样可以避免下载 `docker-compose` 二进制文件本身（它很小，约 20-30MB，但我猜你指的是 LibreChat 服务总共需要拉取约 70MB+ 的镜像）。然而，核心的 Docker 镜像（例如应用、MongoDB、MeiliSearch）在拉取后总共仍有约 500MB-1GB——Docker Compose 只是 Docker 之上的编排工具，并非主要的带宽消耗者。在缓慢的 4G/5G 网络上拉取镜像仍然是瓶颈，但你可以缓解这个问题。

下面我将列出几种方案，优先介绍节省带宽的技巧。如果移动数据非常有限，可以考虑暂时连接到 WiFi 网络，或在另一台机器上使用预下载的设置（例如，通过 `docker save`/`docker load` 导出/导入镜像）。

### 任何基于 Docker 的设置节省带宽的技巧

- **在更快的连接上预拉取镜像**：在另一台网络更好的设备上，运行 `docker pull node:20-alpine`（用于应用）、`docker pull mongo:7`（数据库）和 `docker pull getmeili/meilisearch:v1.10`（搜索）。然后将它们保存为文件：

  ```
  docker save -o librechat-app.tar node:20-alpine
  docker save -o mongo.tar mongo:7
  docker save -o meili.tar getmeili/meilisearch:v1.10
  ```

  通过 USB/驱动器传输 .tar 文件（总共约 500-800MB 压缩后），然后在你的 Ubuntu 机器上运行：`docker load -i librechat-app.tar` 等。无需在线拉取。
- **使用更轻量的替代方案**：为了测试，可以暂时跳过 MeiliSearch（搜索功能是可选的；在配置中禁用它）。MongoDB 镜像约 400MB——改用本地 MongoDB 安装（见下面的非 Docker 部分）可以节省约 400MB。
- **监控使用情况**：使用 `docker pull --quiet` 或类似 `watch docker images` 的工具来跟踪。
- **代理或缓存**：如果你有 Docker Hub 镜像或代理，可以在 `/etc/docker/daemon.json` 中配置以加速拉取。

### 方案 1：纯 Docker（无 Compose）——等同于 Compose 设置

你可以使用 `docker run` 和 `docker network` 来复制 `docker-compose.yml` 的行为。这会下载相同的镜像，但让你控制每个步骤。总下载量仍约为 700MB+（应用构建 + 数据库）。

1. **创建 Docker 网络**（隔离服务）：

   ```
   docker network create librechat-network
   ```

2. **运行 MongoDB**（将 `your_mongo_key` 替换为强密码）：

   ```
   docker run -d --name mongodb --network librechat-network \
     -e MONGO_INITDB_ROOT_USERNAME=librechat \
     -e MONGO_INITDB_ROOT_PASSWORD=your_mongo_key \
     -v $(pwd)/data/mongodb:/data/db \
     mongo:7
   ```

   - 创建 `./data/mongodb` 用于持久化。

3. **运行 MeiliSearch**（将 `your_meili_key` 替换为强密码）：

   ```
   docker run -d --name meilisearch --network librechat-network \
     -e MEILI_MASTER_KEY=your_meili_key \
     -p 7700:7700 \
     -v $(pwd)/data/meili:/meili_data \
     getmeili/meilisearch:v1.10
   ```

   - 如果带宽紧张，可以跳过；稍后在应用配置中禁用。

4. **克隆并构建/运行 LibreChat 应用**：
   - 如果尚未完成，克隆仓库：`git clone https://github.com/danny-avila/LibreChat.git && cd LibreChat`（仓库下载约 50MB）。
   - 构建镜像（这会拉取 Node.js 基础镜像约 200MB 并构建应用层）：

     ```
     docker build -t librechat-app .
     ```

   - 运行它（连接到数据库，使用环境变量——像我之前的回复中一样创建一个 `.env` 文件）：

     ```
     docker run -d --name librechat --network librechat-network -p 3080:3080 \
       --env-file .env \
       -v $(pwd):/app \
       librechat-app
     ```

     - 在 `.env` 中，设置 `MONGODB_URI=mongodb://librechat:your_mongo_key@mongodb:27017/LibreChat` 和 `MEILI_HOST=http://meilisearch:7700` 等。

5. **访问**：`http://localhost:3080`。日志：`docker logs -f librechat`。

- **停止/清理**：`docker stop mongodb meilisearch librechat && docker rm them`。
- **优点/缺点**：与 Compose 相同，但更手动。镜像拉取/构建仍然消耗大量数据。

### 方案 2：非 Docker 安装（手动，无镜像拉取）——推荐用于低带宽情况

在 Ubuntu 上原生安装依赖项。这避免了所有 Docker 开销（容器约 0MB；仅通过 apt/yarn 下载包，总共约 200-300MB）。间接使用你系统的 Python/Node 设置。

#### 先决条件（一次性安装）

```
sudo apt update
sudo apt install nodejs npm mongodb-org redis meilisearch git curl build-essential python3-pip -y  # MongoDB 官方包；MeiliSearch 约 50MB 二进制文件
sudo systemctl start mongod redis meilisearch
sudo systemctl enable mongod redis meilisearch
```

- Node.js：如果不是 v20+，通过 nvm 安装：`curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash`，然后 `nvm install 20`。
- Yarn：`npm install -g yarn`。
- MongoDB 配置：编辑 `/etc/mongod.conf` 绑定到 localhost，然后重启。

#### 安装步骤

1. **克隆仓库**：

   ```
   cd ~/projects
   git clone https://github.com/danny-avila/LibreChat.git
   cd LibreChat
   ```

2. **安装依赖项**：

   ```
   yarn install  # 约 100-200MB 的包下载
   ```

3. **配置 `.env`**（从 `.env.example` 复制）：
   - `cp .env.example .env && nano .env`
   - 关键更改：
     - Mongo：`MONGODB_URI=mongodb://localhost:27017/LibreChat`（如果需要，通过 `mongo` shell 创建数据库用户）。
     - Meili：`MEILI_HOST=http://localhost:7700` 和 `MEILI_MASTER_KEY=your_key`。
     - 如果跳过 Meili，禁用搜索：`SEARCH=false`。
     - 根据需要添加 AI 密钥。

4. **构建并运行**：
   - 在一个终端中：`yarn run backend`（在端口 3090 启动 API）。
   - 在另一个终端中：`yarn run frontend`（在端口 3080 启动 UI）。
   - 或者在生产环境中使用 PM2：`yarn global add pm2 && pm2 start yarn --name backend -- run backend` 等。

5. **访问**：`http://localhost:3080`。创建账户并配置。

- **数据**：MongoDB 存储在 `/var/lib/mongodb`，Meili 存储在 `/var/lib/meilisearch`。
- **故障排除**：
  - Mongo 认证：运行 `mongo` 并创建用户：`use LibreChat; db.createUser({user: 'librechat', pwd: 'yourpass', roles: ['readWrite']})`。
  - 端口/防火墙：`sudo ufw allow 3080,3090,7700`。
  - 更新：`git pull && yarn install && restart services`。
- **优点**：带宽消耗更轻（无容器），直接使用系统资源。缺点：设置更繁琐，可能存在依赖冲突（例如，与你的 Python 3.13，但 Node 是独立的）。

如果移动数据极其有限，非 Docker 方法是最佳选择——分阶段进行，使用 `du -sh` 监控目录。对于错误，请分享日志（例如来自 `yarn run backend`）。官方非 Docker 指南：<https://docs.librechat.ai/install/installation/manual_install.html。如果你需要> Ollama 集成以使用本地 AI（节省 API 成本），请通过他们的脚本单独安装（约 100MB）。如果需要调整，请告诉我！
