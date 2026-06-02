---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: 在Ubuntu上安装LibreChat
translated: true
type: note
---

### 在 Ubuntu 24.04 LTS 上安装 LibreChat

LibreChat 是一款开源 AI 聊天平台，支持通过网页界面调用多种 AI 模型（如 OpenAI、Gemini、Ollama）。推荐使用 Docker Compose 进行安装，这种方式简单易行，能自动处理 MongoDB 和 MeiliSearch 等依赖项，且在 Ubuntu 系统上运行稳定。您的系统（Ubuntu 24.04.2 LTS 搭配 Python 3.13.4）已满足要求，但需要先安装 Docker 和 Git。

#### 环境准备
1. **更新系统**：
   ```
   sudo apt update && sudo apt upgrade -y
   ```

2. **安装 Git**（如未安装）：
   ```
   sudo apt install git -y
   ```

3. **安装 Docker 与 Docker Compose**：
   - 安装 Docker：
     ```
     sudo apt install docker.io -y
     sudo systemctl start docker
     sudo systemctl enable docker
     sudo usermod -aG docker $USER
     ```
     注销并重新登录（或执行 `newgrp docker`）使用户组变更生效。
   - 安装 Docker Compose（最新版本）：
     ```
     sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
     sudo chmod +x /usr/local/bin/docker-compose
     ```
     可通过 `docker-compose --version` 验证安装。

#### 安装步骤
1. **克隆 LibreChat 代码库**：
   ```
   cd ~/projects  # 或您偏好的目录
   git clone https://github.com/danny-avila/LibreChat.git
   cd LibreChat
   ```

2. **复制并配置环境文件**：
   - 复制示例文件：
     ```
     cp .env.example .env
     ```
   - 使用文本编辑器修改 `.env`（如 `nano .env`）。需更新的关键设置：
     - 设置 MongoDB 主密钥：生成强密码并配置 `MONGODB_URI=mongodb://mongodb:27017/LibreChat?authSource=admin` 与 `MONGODB_MASTER_KEY=此处填入生成的密钥`。
     - MeiliSearch 配置：设置 `MEILI_MASTER_KEY=此处填入生成的密钥`（生成强密钥）。
     - 按需添加 AI API 密钥（如 `OPENAI_API_KEY=您的_openai_密钥`）。对于 Ollama 等本地模型，初始无需密钥。
     - 保存并退出。完整配置选项请参阅文档。

3. **通过 Docker Compose 启动 LibreChat**：
   ```
   docker-compose up -d
   ```
   - 该命令将拉取镜像、启动服务（LibreChat 应用、MongoDB、MeiliSearch）并在后台运行。
   - 等待服务完全启动（可通过 `docker-compose logs -f` 查看状态）。

4. **访问 LibreChat**：
   - 打开浏览器访问 `http://localhost:3080`。
   - 在登录页面创建账户。
   - 选择 AI 模型（需在设置中配置端点）即可开始对话。

#### 安装后提示
- **停止/更新**：执行 `docker-compose down` 停止服务，通过 `git pull` 和 `docker-compose up -d --build` 更新。
- **数据持久化**：MongoDB 数据将自动创建存储卷（位于 `./data/mongodb`）。
- **故障排除**：
  - 端口冲突时可编辑 `docker-compose.yml` 修改 `3080:3080`。
  - 无图形界面/服务器访问需使用服务器 IP（如 `http://您的服务器IP:3080`）并确保防火墙放行 3080 端口（`sudo ufw allow 3080`）。
  - 使用本地 LLM 时需单独安装 Ollama 并在 `.env` 中配置端点。
- **备选方案：NPM 方式**（无需 Docker）：可手动安装 Node.js 18+、Yarn、MongoDB 和 MeiliSearch，然后运行 `yarn install` 及 `yarn run frontend` + `yarn run backend`。但强烈推荐 Docker 以简化流程。

按照以上步骤可快速完成部署。若遇到错误，请提供输出信息以获取进一步帮助！

[LibreChat 官方文档](https://docs.librechat.ai/install/installation/docker_compose.html)
[Ubuntu Docker 指南](https://docs.librechat.ai/install/installation/docker_ubuntu.html)
[It's FOSS 教程](https://itsfoss.com/librechat-linux/)
