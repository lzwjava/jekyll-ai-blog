---
audio: false
generated: true
lang: zh
layout: post
title: 在 Debian 上通过 APT 安装 Go
translated: true
type: note
---

要在基于 Debian 的 Linux 系统（如 Ubuntu）上使用 `apt` 安装 Go，请按照以下步骤操作。请注意，`apt` 可能会安装较旧版本的 Go（例如 Ubuntu 22.04 上是 1.18 版），因此您需要确认其是否满足项目要求（检查 `~/Projects/clash-core` 中的 `go.mod` 文件以获取所需 Go 版本）。

### 使用 APT 安装 Go 的步骤

1. **更新软件包索引**
   - 确保软件包列表是最新的：
     ```bash
     sudo apt update
     ```

2. **安装 Go**
   - 安装 Go 软件包：
     ```bash
     sudo apt install golang-go
     ```
   - 这将安装 Go 编译器、工具和标准库。

3. **验证安装**
   - 检查已安装的 Go 版本：
     ```bash
     go version
     ```
   - 您应该会看到类似输出：
     ```
     go version go1.18.1 linux/amd64
     ```
     （具体版本取决于您发行版的软件仓库。）

4. **设置 GOPATH（可选）**
   - 现代 Go 版本（1.13+）使用模块，因此 `GOPATH` 是可选的，但设置它对某些项目可能有用。
   - 编辑您的 shell 配置文件（如 `~/.bashrc` 或 `~/.zshrc`）：
     ```bash
     nano ~/.bashrc
     ```
   - 添加以下内容：
     ```bash
     export GOPATH=$HOME/go
     export PATH=$PATH:$GOPATH/bin
     ```
   - 保存并重新加载 shell 配置：
     ```bash
     source ~/.bashrc
     ```

5. **重新尝试构建**
   - 进入项目目录：
     ```bash
     cd ~/Projects/clash-core
     ```
   - 再次运行 `make` 命令：
     ```bash
     make
     ```

### 注意事项
- **版本检查**：如果您的项目需要更新的 Go 版本（如 1.20 或更高），`apt` 版本可能过时。请检查 `go.mod` 或项目文档中的所需版本。如果需要，请通过从 [https://go.dev/dl/](https://go.dev/dl/) 下载压缩包手动安装新版本（如先前回复中所述）。
- **替代软件仓库**：要通过 `apt` 获取更新版本，您可以添加第三方 PPA（例如 Ubuntu 上的 `ppa:longsleep/golang-backports`）。运行：
  ```bash
  sudo add-apt-repository ppa:longsleep/golang-backports
  sudo apt update
  sudo apt install golang-go
  ```
- **故障排除**：
  - 如果找不到 `go`，请确保 `/usr/bin/go` 存在（`ls /usr/bin/go`）。如果不存在，请使用 `sudo apt install --reinstall golang-go` 重新安装。
  - 如果出现依赖错误，请运行 `sudo apt install -f` 进行修复。
  - 对于权限问题，请确保您拥有 `sudo` 权限。

### 来源
- Ubuntu Go 安装指南：[https://ubuntu.com/server/docs/programming-go](https://ubuntu.com/server/docs/programming-go)
- 通用 apt 使用指南：[https://help.ubuntu.com/community/AptGet/Howto](https://help.ubuntu.com/community/AptGet/Howto)

如果安装的版本过旧或遇到问题，请告诉我您的 Linux 发行版（例如 Ubuntu 22.04）和所需的 Go 版本，我将为您提供进一步指导！
