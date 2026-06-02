---
audio: false
generated: true
lang: zh
layout: post
title: 解决macOS中Go命令未找到的问题
translated: true
type: note
---

错误信息 `/bin/sh: go: command not found` 表明您的 macOS 系统未安装 Go 编程语言，或者其未在 PATH 环境变量中正确配置。`make` 命令试图运行 Go 构建过程，这需要 Go 编译器 (`go`)。以下是解决此问题并在 macOS 上安装 Go 的步骤。

### 在 macOS 上安装 Go 的步骤

在 macOS 上安装 Go 主要有两种方法：使用官方 Go 安装程序或使用 Homebrew。我将介绍这两种方法，但对于 macOS 用户来说，Homebrew 通常更简单。请根据您的偏好选择一种方法。

#### 前提条件

- 确保您的 macOS 版本为 10.10 或更高版本，以兼容近期的 Go 版本。
- 您需要管理员权限来安装 Go 和修改系统文件。
- 需要一个终端应用程序（位于 应用程序 > 实用工具 > 终端）。

#### 方法 1：使用 Homebrew 安装 Go（推荐）

Homebrew 是 macOS 上流行的软件包管理器，可简化软件安装。

1. **安装 Homebrew（如果尚未安装）**：
    - 打开终端并运行：

      ```bash
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```

    - 按照屏幕上的说明完成安装。

2. **安装 Go**：
    - 运行以下命令安装最新版本的 Go：

      ```bash
      brew install go
      ```

    - 这将把 Go 安装到 `/usr/local/Cellar/go`（或类似路径），并将 Go 二进制文件添加到 `/usr/local/bin`。

3. **验证安装**：
    - 通过运行以下命令检查已安装的 Go 版本：

      ```bash
      go version
      ```

    - 您应该看到类似 `go version go1.23.x darwin/amd64` 的输出，确认 Go 已安装。

4. **设置环境变量（如果需要）**：
    - Homebrew 通常会自动将 Go 添加到您的 PATH 中，但如果 `go` 命令不工作，请将 Go 二进制文件路径添加到您的 Shell 配置文件中：
      - 打开或创建相应的 Shell 配置文件（例如，对于 Zsh（自 Catalina 起是 macOS 的默认 Shell）使用 `~/.zshrc`，对于 Bash 使用 `~/.bash_profile`）：

        ```bash
        nano ~/.zshrc
        ```

      - 添加以下行：

        ```bash
        export PATH=$PATH:/usr/local/go/bin
        ```

      - 保存文件（在 nano 中按 Ctrl+X，然后按 Y，再按 Enter）并应用更改：

        ```bash
        source ~/.zshrc
        ```

      - 如果您想使用自定义工作区，请设置 `GOPATH`（可选，因为 Go 模块通常消除了对此的需求）：

        ```bash
        export GOPATH=$HOME/go
        export PATH=$PATH:$GOPATH/bin
        ```

      - 再次 source 该文件：

        ```bash
        source ~/.zshrc
        ```

5. **测试 Go 安装**：
    - 再次运行 `go version` 以确保命令被识别。
    - （可选）创建一个简单的 Go 程序以确认一切正常：

      ```bash
      mkdir -p ~/go/src/hello
      nano ~/go/src/hello/main.go
      ```

      - 添加以下代码：

        ```go
        package main
        import "fmt"
        func main() {
            fmt.Println("Hello, World!")
        }
        ```

      - 保存并退出（Ctrl+X, Y, Enter），然后编译并运行：

        ```bash
        cd ~/go/src/hello
        go run main.go
        ```

      - 您应该看到 `Hello, World!` 作为输出。

#### 方法 2：使用官方安装程序安装 Go

如果您不想使用 Homebrew，可以使用官方的 macOS 软件包安装 Go。

1. **下载 Go 安装程序**：
    - 访问官方 Go 下载页面：<https://go.dev/dl/>
    - 为您的系统架构下载 macOS 软件包（`.pkg`）（例如，对于 Intel Mac 下载 `go1.23.x.darwin-amd64.pkg`，对于 Apple Silicon Mac 下载 `go1.23.x.darwin-arm64.pkg`）。

2. **运行安装程序**：
    - 在访达中双击下载的 `.pkg` 文件。
    - 按照屏幕上的说明安装 Go。默认情况下，它将被安装到 `/usr/local/go`。
    - 您可能需要输入管理员密码。

3. **设置环境变量**：
    - 打开终端并编辑您的 Shell 配置文件（例如 `~/.zshrc` 或 `~/.bash_profile`）：

      ```bash
      nano ~/.zshrc
      ```

    - 添加以下行：

      ```bash
      export GOROOT=/usr/local/go
      export GOPATH=$HOME/go
      export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
      ```

    - 保存并应用更改：

      ```bash
      source ~/.zshrc
      ```

    - 注意：除非您正在开发 Go 本身或需要非标准安装路径，否则 `GOROOT` 是可选的。现代 Go 版本通常不需要设置 `GOROOT`。

4. **验证安装**：
    - 运行：

      ```bash
      go version
      ```

    - 您应该看到已安装的 Go 版本（例如 `go version go1.23.x darwin/amd64`）。

5. **测试 Go 安装**：
    - 按照方法 1 中的步骤 5 创建并运行 "Hello, World!" 程序。

#### 排查原始问题

安装 Go 后，返回到您的 `clash-core` 目录并重试 `make` 命令：

```bash
cd /path/to/clash-core
make
```

如果您遇到问题：

- **代理设置**：您的终端输出显示 `HTTP_PROXY` 和 `HTTPS_PROXY` 设置为 `http://127.0.0.1:7890`。请确保您的代理处于活动状态且未干扰 Go 的网络访问（例如，下载依赖项）。您可以临时禁用代理进行测试：

  ```bash
  unset HTTP_PROXY HTTPS_PROXY
  make
  ```

- **权限**：如果出现权限错误，请确保您对项目目录和 Go 工作区（`$GOPATH` 或 `$HOME/go`）具有写权限。
- **Go 模块**：`clash-core` 项目很可能使用 Go 模块。确保您在包含 `go.mod` 的正确目录中，并在运行 `make` 之前运行 `go mod tidy` 来获取依赖项：

  ```bash
  go mod tidy
  make
  ```

- **架构不匹配**：`make` 命令正在为 `linux-amd64`（`GOOS=linux GOARCH=amd64`）构建。如果您打算在 macOS 上运行该二进制文件，可能需要修改 Makefile 或构建命令以定位 `darwin-amd64`（针对 Intel Mac）或 `darwin-arm64`（针对 Apple Silicon）。检查 Makefile 中的 `linux-amd64` 目标并进行调整，或者运行：

  ```bash
  GOARCH=amd64 GOOS=darwin CGO_ENABLED=0 go build -trimpath -ldflags '-X "github.com/Dreamacro/clash/constant.Version=1.18" -X "github.com/Dreamacro/clash/constant.BuildTime=Sat Jun 28 12:24:27 UTC 2025" -w -s -buildid=' -o bin/clash-darwin-amd64
  ```

  如果您使用的是 Apple Silicon，请将 `amd64` 替换为 `arm64`。

#### 补充说明

- **卸载旧版 Go**：如果之前安装过 Go，请将其移除以避免冲突：

  ```bash
  sudo rm -rf /usr/local/go
  sudo rm -f /etc/paths.d/go
  ```

  然后使用上述方法之一重新安装。
- **Go 工作区**：如果您设置了 `GOPATH`，请创建该目录：

  ```bash
  mkdir -p $HOME/go/{bin,src,pkg}
  ```

  但是，对于使用 Go 模块的大多数现代项目（如 `clash-core`），`GOPATH` 就不那么关键了。
- **Xcode 命令行工具**：某些 Go 项目需要 C 依赖项（例如 `CGO_ENABLED=1`）。如果需要，请安装 Xcode 命令行工具：

  ```bash
  xcode-select --install
  ```

- **多版本 Go**：如果您需要多个 Go 版本，请考虑使用版本管理器，如 `gvm`（可通过 Homebrew 或脚本安装）。

#### 验证

一旦 Go 安装成功且 `make` 命令执行成功，`clash-core` 二进制文件应出现在 `bin/` 目录中（例如 `bin/clash-linux-amd64` 或 `bin/clash-darwin-amd64`）。通过运行以下命令验证其是否工作：

```bash
./bin/clash-darwin-amd64 --version
```

如果您需要进一步的帮助或遇到特定的错误，请告诉我确切错误信息或上下文，我可以提供更有针对性的帮助！
