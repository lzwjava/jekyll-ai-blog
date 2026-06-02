---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: Docker Compose 快速安装方法
translated: true
type: note
---

### 在 Ubuntu 上快速下载/安装 Docker Compose 的替代方法

假设您希望快速获取最新的 Docker Compose 二进制文件（根据官方文档，截至 2025 年 10 月为 v2.37.3），而无需经过完整的 GitHub 发布页面流程（例如手动 curl 和 sha256 验证），这里提供几种可靠且更快速的选项。这些方法利用 Ubuntu 的包管理器或 Docker 的软件源实现近乎即时的安装。我将优先考虑速度和简单性——大多数方法耗时不超过 1 分钟。

#### 1. **通过 Ubuntu APT（对大多数用户最快）**
   如果您已安装 Docker（包含 `docker-compose-plugin`），只需使用子命令——无需单独下载。这是现代集成方式，可避免二进制文件管理。

   - **检查是否已可用**：
     ```
     docker compose version
     ```
     如果显示 v2.x 版本，则已完成——这是通过 Docker 安装的最新版本。

   - **需要时安装/更新**（若缺少插件则添加）：
     ```
     sudo apt update
     sudo apt install docker-compose-plugin
     ```
     - **为何快速？** 无需访问 GitHub；使用本地软件源。通过 `apt upgrade` 自动更新。
     - **用法**：以 `docker compose up` 运行（注意是空格而非连字符）。
     - **专业提示**：如果尚未安装 Docker，请先添加 Docker 软件源：
       ```
       sudo apt update
       sudo apt install ca-certificates curl
       sudo install -m 0755 -d /etc/apt/keyrings
       sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
       sudo chmod a+r /etc/apt/keyrings/docker.asc
       echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
       sudo apt update
       sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
       ```

#### 2. **从 GitHub 单行 Curl（比完整发布略快）**
   跳过浏览发布页面——curl 直接获取最新的 Linux x86_64 二进制文件并安装。比手动选择资源更快，但仍使用 GitHub。

   ```
   VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4) && sudo curl -L "https://github.com/docker/compose/releases/download/${VERSION}/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose && docker-compose --version
   ```
   - **为何快速？** API 在几秒内获取版本；单条命令处理下载和安装。
   - **验证**：末尾的 `--version` 确认安装。
   - **注意**：如需特定版本 v2.39.4，将 `${VERSION}` 替换为 `v2.39.4`。

#### 3. **通过 Snap（Ubuntu 的通用包管理器）**
   Snap 预装在 Ubuntu 24.04 上，可从 Canonical 商店即时拉取最新版本。

   ```
   sudo snap install docker
   ```
   - **为何快速？** 无需设置软件源；并行下载且自动更新。包含 Compose 插件。
   - **用法**：与 APT 方法相同（`docker compose`）。
   - **检查版本**：`docker compose version`。

#### 4. **通过 Pip（因您已安装 Python 3.13.4）**
   如果您偏好基于 Python 的方式（传统 v1 风格，但 pip 提供 v2 封装器），可快速安装且无需系统依赖。

   ```
   sudo pip3 install docker-compose
   ```
   - **为何快速？** Pip 缓存并快速解析依赖；不涉及 GitHub。
   - **限制**：这更多用于 v1 兼容性——对于官方 v2 插件，请使用 APT。
   - **验证**：`docker-compose --version`（带连字符）。

这些方法都比 GitHub 界面更快，因为它们最小化点击或使用 API/缓存。对于 Ubuntu，我首选推荐 APT 或 Snap——它们无缝集成并处理更新。如果您对 "docker compose down" 有其他含义（例如命令本身），请澄清！

[官方 Docker Compose 安装指南](https://docs.docker.com/compose/install/linux/)
[Docker 发布页面](https://github.com/docker/compose/releases)
