---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: Ubuntu系统安装Docker Compose
translated: true
type: note
---

根据您的系统信息，您正在 **x86_64** 架构上运行 **Ubuntu 24.04.2 LTS**。要从提供的 GitHub 发布版本 (v2.39.4) 下载适用于您系统的 **Docker Compose** 二进制文件，您应选择与 Linux x86_64 兼容的二进制文件。

### 推荐下载
您应下载 **docker-compose-linux-x86_64** 二进制文件。该文件在提供的资源列表中未明确列出，但在 Docker Compose 发布版本中，它是 Linux x86_64 系统的标准二进制文件。然而，根据列出的资源，与您系统最接近的匹配项是：

- **docker-compose-linux-aarch64** **不**适用，因为它适用于 ARM64 (aarch64) 架构，而您的系统是 x86_64。
- **darwin** 二进制文件（例如 `docker-compose-darwin-x86_64`）适用于 macOS，而非 Linux。
- 源代码选项（`Source code (zip)` 或 `Source code (tar.gz)`）需要手动编译，这通常是不必要的，因为通常有预编译的二进制文件可用。

由于 **docker-compose-linux-x86_64** 二进制文件在您提供的资源中未明确列出，但在 Docker Compose 发布版本中是标准文件，您很可能可以在 GitHub 发布页面的完整资源列表中找到它。如果不可用，您可以使用源代码或通过替代方法（例如，包管理器或 pip）安装 Docker Compose。

### 下载和安装步骤
1.  **确认二进制文件**：访问 v2.39.4 的 GitHub 发布页面以确认 `docker-compose-linux-x86_64` 的可用性。发布页面通常位于：
    [Docker Compose v2.39.4 Release](https://github.com/docker/compose/releases/tag/v2.39.4)

2.  **下载二进制文件**：
    如果 `docker-compose-linux-x86_64` 可用，请下载它。例如：
    ```bash
    curl -L "https://github.com/docker/compose/releases/download/v2.39.4/docker-compose-linux-x86_64" -o docker-compose
    ```

3.  **验证下载**：
    使用提供的校验和验证下载文件的完整性。例如，如果 `docker-compose-linux-x86_64.sha256` 文件可用：
    ```bash
    echo "<sha256> docker-compose" | sha256sum --check
    ```
    将 `<sha256>` 替换为发布资源中的相应哈希值（例如，`docker-compose-darwin-x86_64.sha256` 的 `df7ff3dd8080134b851e1e49265028697d27de71f9bdc187e3d833357b934f36`，但您需要 Linux 等效版本）。

4.  **安装二进制文件**：
    将二进制文件移动到您的 PATH 环境变量中的某个目录，例如 `/usr/local/bin`：
    ```bash
    chmod +x docker-compose
    sudo mv docker-compose /usr/local/bin/docker-compose
    ```

5.  **验证安装**：
    检查安装的版本：
    ```bash
    docker-compose --version
    ```
    它应输出 `Docker Compose version v2.39.4`。

### 替代安装方法
如果 `docker-compose-linux-x86_64` 二进制文件不可用，或者您更喜欢更简单的方法，您可以使用包管理器或 pip 安装 Docker Compose，因为您的系统已安装 Python 3.13.4：

#### 通过包管理器（Ubuntu 推荐）
Docker Compose 通常可在 Ubuntu 的软件仓库或 Docker 的官方仓库中找到：
```bash
sudo apt update
sudo apt install docker-compose-plugin
```
这将安装 Docker Compose 插件，这是使用 Docker Compose 的现代方式（使用 `docker compose` 而不是 `docker-compose`）。请注意，Ubuntu 软件仓库中的版本可能不完全是 v2.39.4，请使用以下命令检查：
```bash
docker compose version
```

#### 通过 pip (Python)
由于您有 Python 3.13.4，您可以通过 pip 安装 Docker Compose：
```bash
pip3 install docker-compose==2.39.4
```
这将安装特定版本。使用以下命令验证：
```bash
docker-compose --version
```

### 注意
- `checksums.txt` 文件 (SHA256: `1a9c3370b88825ab2b229bb90eda6f703d84018ea1d56b5ba573f8893c9ab6b4`) 可用于验证下载文件的完整性。
- 如果您选择从源代码编译（`Source code (zip)` 或 `Source code (tar.gz)`），您将需要 Go（您的系统信息中未列出）和额外的设置，这更复杂，除非必要，否则不推荐。
- 此版本包含改进和修复（例如，支持 `develop.watch.initial_sync`、无项目的 volume ls 以及 bake 的 TLS），如果您正在使用这些功能，这些改进和修复是相关的。

如果您在查找确切的 `docker-compose-linux-x86_64` 二进制文件时遇到问题或遇到任何问题，请告诉我，我可以进一步指导您！

[Docker Compose v2.39.4 Release](https://github.com/docker/compose/releases/tag/v2.39.4)
