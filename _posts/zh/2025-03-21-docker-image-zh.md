---
audio: false
generated: true
lang: zh
layout: post
title: 构建与部署Docker镜像
translated: true
type: note
---

以下是构建 Spring Boot 应用为 Docker 镜像并部署到服务器的分步指南：

### 前置条件
1. 本地安装 **Java**（如 JDK 17 或兼容版本）
2. 安装 **Maven** 或 **Gradle**（根据 Spring Boot 项目配置选择）
3. 本地机器和服务器均安装 **Docker**
4. 准备好可容器化的 **Spring Boot 项目**
5. 拥有服务器访问权限（如 SSH）且已安装 Docker

---

### 步骤 1：准备 Spring Boot 应用
确保 Spring Boot 应用在本地正常运行。使用以下命令测试：
```bash
mvn spring-boot:run  # Maven 用户
# 或
gradle bootRun       # Gradle 用户
```

确认应用构建成功：
```bash
mvn clean package    # Maven
# 或
gradle build         # Gradle
```
此操作将生成 `.jar` 文件（如 `target/myapp-1.0.0.jar`）

---

### 步骤 2：创建 Dockerfile
在项目根目录（`.jar` 文件所在位置）创建名为 `Dockerfile` 的文件，内容如下：

```dockerfile
# 使用官方 OpenJDK 运行时作为基础镜像
FROM openjdk:17-jdk-slim

# 设置容器内工作目录
WORKDIR /app

# 将 Spring Boot JAR 文件复制到容器中
COPY target/myapp-1.0.0.jar app.jar

# 暴露 Spring Boot 应用运行端口（默认为 8080）
EXPOSE 8080

# 运行 JAR 文件
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**注意：**
- 将 `myapp-1.0.0.jar` 替换为实际 JAR 文件名
- 若应用使用其他 Java 版本，请调整基础镜像（如 `openjdk:17-jdk-slim`）

---

### 步骤 3：构建 Docker 镜像
在包含 `Dockerfile` 的目录中执行：
```bash
docker build -t myapp:latest .
```
- `-t myapp:latest` 为镜像打标签
- `.` 指定当前目录为构建上下文

验证镜像创建：
```bash
docker images
```

---

### 步骤 4：本地测试 Docker 镜像
本地运行容器进行验证：
```bash
docker run -p 8080:8080 myapp:latest
```
- `-p 8080:8080` 将本机 8080 端口映射到容器 8080 端口
- 可通过浏览器或 `curl` 测试（如 `curl http://localhost:8080`）

停止容器：
- 使用 `Ctrl+C`
- 或通过 `docker ps` 查找容器 ID 后执行：
```bash
docker stop <容器ID>
```

---

### 步骤 5：推送镜像到 Docker 仓库（可选）
若需部署到服务器，需将镜像推送到 Docker Hub（或私有仓库）。跳过此步骤则需手动传输镜像。

1. 登录 Docker Hub：
   ```bash
   docker login
   ```
2. 为镜像打标签：
   ```bash
   docker tag myapp:latest 你的用户名/myapp:latest
   ```
3. 推送镜像：
   ```bash
   docker push 你的用户名/myapp:latest
   ```

---

### 步骤 6：部署到服务器
#### 方案 1：使用仓库部署
1. SSH 登录服务器：
   ```bash
   ssh 用户@服务器IP
   ```
2. 拉取镜像：
   ```bash
   docker pull 你的用户名/myapp:latest
   ```
3. 运行容器：
   ```bash
   docker run -d -p 8080:8080 你的用户名/myapp:latest
   ```
   - `-d` 表示后台运行模式

#### 方案 2：手动传输
若未使用仓库：
1. 本地将镜像保存为 `.tar` 文件：
   ```bash
   docker save -o myapp.tar myapp:latest
   ```
2. 传输到服务器（如通过 SCP）：
   ```bash
   scp myapp.tar 用户@服务器IP:/目标路径
   ```
3. SSH 登录服务器：
   ```bash
   ssh 用户@服务器IP
   ```
4. 加载镜像：
   ```bash
   docker load -i myapp.tar
   ```
5. 运行容器：
   ```bash
   docker run -d -p 8080:8080 myapp:latest
   ```

---

### 步骤 7：验证部署
检查容器运行状态：
```bash
docker ps
```

测试应用：
- 在服务器上测试：`curl http://localhost:8080`
- 外部访问：使用服务器 IP（如 `http://服务器IP:8080`），确保防火墙已开放端口

---

### 可选增强功能
- **环境变量**：向应用传递配置：
  ```bash
  docker run -d -p 8080:8080 -e "SPRING_PROFILES_ACTIVE=prod" myapp:latest
  ```
- **Docker Compose**：多容器部署时使用 `docker-compose.yml` 文件
- **重启策略**：添加 `--restart unless-stopped` 确保服务器重启时容器自动重启

如有具体问题需要协助，请随时告知！

---

根据您提供的错误输出，有几个问题导致 `docker build` 命令执行失败。让我们逐步分析和解决这些问题。

---

### 已识别问题
1. **缺少 `docker-buildx` 插件**
   错误：`fork/exec /Users/lzwjava/.docker/cli-plugins/docker-buildx: no such file or directory`
   表明 Docker 尝试使用 `buildx` 插件（现代构建工具），但未正确安装或配置

2. **旧版构建器弃用警告**
   警告：`DEPRECATED: The legacy builder is deprecated...`
   Docker 推荐切换到 BuildKit（`buildx`），但当前回退到已失败的旧版构建器

3. **Docker 守护进程未运行**
   错误：`Cannot connect to the Docker daemon at unix:///Users/lzwjava/.docker/run/docker.sock. Is the docker daemon running?`
   Docker 守护进程（管理容器的后台服务）未在系统中运行

4. **文件访问错误**
   错误：`Can't add file ... to tar: io: read/write on closed pipe` 和 `Can't close tar writer...`
   由于守护进程未运行导致构建失败引发的次要问题

5. **检测到代理设置**
   系统正在使用代理（`HTTP_PROXY` 和 `HTTPS_PROXY`），若未正确配置可能影响 Docker 运行

---

### 分步修复方案

#### 1. 验证 Docker 守护进程运行状态
核心问题是 Docker 守护进程未运行。修复方法：

- **macOS 系统**（假设使用 Docker Desktop）：
  1. 从应用程序文件夹或 Spotlight 打开 Docker Desktop
  2. 确保程序运行（菜单栏 Docker 鲸鱼图标应显示绿色）
  3. 若无法启动：
     - 退出 Docker Desktop 后重新启动
     - 检查更新：Docker Desktop > Check for Updates
     - 若仍失败，从 [docker.com](https://www.docker.com/products/docker-desktop/) 重新安装

- **终端验证**：
  执行：
  ```bash
  docker info
  ```
  若守护进程正常运行，将显示系统信息；否则会出现相同连接错误

- **手动重启守护进程**（如需要）：
  ```bash
  sudo launchctl stop com.docker.docker
  sudo launchctl start com.docker.docker
  ```

守护进程正常运行后，继续后续步骤

---

#### 2. 安装 `buildx` 插件（可选但推荐）
由于旧版构建器已弃用，建议设置 `buildx`：

1. **安装 `buildx`**：
   - 手动下载二进制文件或按 Docker 说明操作：
     ```bash
     mkdir -p ~/.docker/cli-plugins
     curl -SL https://github.com/docker/buildx/releases/download/v0.13.0/buildx-v0.13.0.darwin-amd64 -o ~/.docker/cli-plugins/docker-buildx
     chmod +x ~/.docker/cli-plugins/docker-buildx
     ```
     （请根据您的操作系统/架构查看[最新版本](https://github.com/docker/buildx/releases)，如 M1/M2 Mac 使用 `darwin-arm64`）

2. **验证安装**：
   ```bash
   docker buildx version
   ```

3. **设置 BuildKit 为默认**（可选）：
   在 `~/.docker/config.json` 中添加：
   ```json
   {
     "features": { "buildkit": true }
   }
   ```

也可暂时跳过此步骤继续使用旧版构建器（见第4步）

---

#### 3. 处理代理设置
代理设置（`http://127.0.0.1:7890`）可能影响 Docker 拉取镜像。配置方法：

1. **通过 Docker Desktop**：
   - 打开 Docker Desktop > Settings > Resources > Proxies
   - 启用 "Manual proxy configuration" 并填写：
     - HTTP Proxy: `http://127.0.0.1:7890`
     - HTTPS Proxy: `http://127.0.0.1:7890`
   - 应用设置并重启

2. **通过 CLI**（若不使用 Desktop）：
   创建或编辑 `~/.docker/config.json`：
   ```json
   {
     "proxies": {
       "default": {
         "httpProxy": "http://127.0.0.1:7890",
         "httpsProxy": "http://127.0.0.1:7890"
       }
     }
   }
   ```
   编辑后重启 Docker

---

#### 4. 重新尝试构建
现在守护进程已运行且代理已配置，重新执行构建：

```bash
docker build -t myapp:latest .
```

- 若已安装 `buildx`，将默认使用 BuildKit
- 若跳过 `buildx` 安装，可添加 `--progress=plain` 强制使用旧版构建器：
  ```bash
  docker build --progress=plain -t myapp:latest .
  ```

---

#### 5. 排查 `.git/hooks` 错误（如仍存在）
`.git/hooks/pre-rebase.sample` 错误表明 Docker 尝试将非必要文件包含在构建上下文中。通过 `.dockerignore` 文件排除：

1. 在 `Dockerfile` 同级目录创建 `.dockerignore`：
   ```
   .git
   .gitignore
   *.md
   target/*
   !target/*.jar
   ```
2. 此配置告知 Docker 忽略 `.git` 文件夹和 `target/` 目录中除 JAR 文件外的所有内容

3. 重新构建：
   ```bash
   docker build -t myapp:latest .
   ```

---

### 最终验证
- 检查镜像：
  ```bash
  docker images
  ```
- 本地运行：
  ```bash
  docker run -p 8080:8080 myapp:latest
  ```
- 使用 `curl http://localhost:8080` 测试

---

### 后续步骤
镜像构建成功后，请按照我之前回复中的部署步骤操作（如推送到仓库或传输到服务器）。若遇到其他问题请随时告知！
