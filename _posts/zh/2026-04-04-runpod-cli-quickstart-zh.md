---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod CLI 入门指南
translated: true
type: note
---

**问题：** 请全面介绍 RunPod CLI (`runpodctl`)——RunPod GPU 平台的命令行界面。

**回答：**

---

## RunPod CLI (`runpodctl`) 简介

### 什么是 RunPod CLI？

`runpodctl` 是一款开源命令行界面工具，用于从本地机器远程管理您的 RunPod 资源。您可以在本地系统与 RunPod 之间传输文件和资料，在远程 Pod 上执行代码，并自动化 Pod 部署工作流。

该 CLI 提供几个核心功能：管理 Pod（创建、列出、启动、停止、终止），在本地机器与 Pod 之间传输文件，以及使用 RunPod 项目开发和部署 Serverless 端点。

您部署的每个 Pod 都预装了 `runpodctl` 命令和一个 Pod 作用域的 API 密钥。您也可以将其安装在本地机器上，以便从自己的系统远程管理您的 Pod。

---

### 安装

#### macOS

```bash
# Homebrew（推荐）
brew install runpod/runpodctl/runpodctl

# Apple Silicon（ARM）
wget --quiet --show-progress https://github.com/runpod/runpodctl/releases/download/v1.14.3/runpodctl-darwin-arm64 \
  -O runpodctl && chmod +x runpodctl && sudo mv runpodctl /usr/local/bin/runpodctl

# Intel（AMD）
wget --quiet --show-progress https://github.com/runpod/runpodctl/releases/download/v1.14.3/runpodctl-darwin-amd64 \
  -O runpodctl && chmod +x runpodctl && sudo mv runpodctl /usr/local/bin/runpodctl
```

#### Linux

```bash
wget --quiet --show-progress https://github.com/Run-Pod/runpodctl/releases/download/v1.14.3/runpodctl-linux-amd64 \
  -O runpodctl && chmod +x runpodctl && sudo cp runpodctl /usr/bin/runpodctl
```

#### Windows

```bash
wget https://github.com/runpod/runpodctl/releases/download/v1.14.3/runpodctl-windows-amd64.exe -O runpodctl.exe
```

#### 通用一键安装器

```bash
wget -qO- cli.runpod.net | bash
```

---

### 配置——API 密钥设置

在本地使用 `runpodctl` 之前，必须使用您的 RunPod API 密钥进行身份验证：

```bash
runpodctl config --apiKey YOUR_API_KEY
```

这会将密钥保存到 `~/.runpod/config.toml` 中。要验证安装：

```bash
runpodctl version
```

---

### 命令结构

命令遵循“名词-动词”模式：`runpodctl <资源> <操作>`。例如：

```bash
runpodctl pod list
runpodctl pod get <id>
runpodctl pod create --image=<img>
```

---

### 核心命令类别

#### 1. Pod 管理

主要的 Pod 命令有：

```bash
runpodctl pod list              # 列出所有 Pod
runpodctl pod get <id>          # 获取 Pod 详细信息
runpodctl pod create --image=runpod/pytorch:latest --gpu-id=NVIDIA_A100   # 创建 Pod
runpodctl pod update <id>       # 更新 Pod
runpodctl pod start <id>        # 启动已停止的 Pod
runpodctl pod stop <id>         # 停止正在运行的 Pod
runpodctl pod delete <id>       # 删除 Pod
```

您也可以设置竞价来启动一个 Spot Pod：

```bash
runpodctl start pod {podId} --bid=0.3
```

您设置的竞价是您在未被出价更高者取代时需要支付的价格。

#### 2. Serverless 端点管理

```bash
runpodctl serverless list          # 列出端点（别名：sls）
runpodctl serverless get <id>      # 获取端点详细信息
runpodctl serverless create        # 创建端点
runpodctl serverless update <id>   # 更新端点
runpodctl serverless delete <id>   # 删除端点
```

#### 3. 文件传输（`send` / `receive`）

`runpodctl` 可用于在 Pod 与您的本地计算机之间或在 Pod 与 Pod 之间来回传输文件。

要发送文件，运行 send 命令，您将收到一个唯一的、一次性传输码，例如 `8338-galileo-collect-fidel`。在目标机器上，使用该码配合 receive 命令。

```bash
# 在发送方机器上
runpodctl send data.txt
# 输出：Code is: 8338-galileo-collect-fidel

# 在接收方机器上
runpodctl receive 8338-galileo-collect-fidel
```

请注意，使用 runpodctl 无需打开任何 HTTP 或 TCP 端口，只需终端访问权限即可。

#### 4. 其他资源管理

`runpodctl` 管理的其他资源包括：

- `template`（别名：`tpl`）— 管理模板
- `network-volume`（别名：`nv`）— 管理网络卷
- `registry`（别名：`reg`）— 管理容器注册表身份验证
- `model` — 管理模型仓库

#### 5. 信息和实用程序命令

```bash
runpodctl user         # 显示账户信息和余额（别名：me）
runpodctl gpu          # 列出可用的 GPU 类型
runpodctl datacenter   # 列出数据中心及其可用性（别名：dc）
runpodctl billing      # 查看账单历史
runpodctl doctor       # 诊断并修复 CLI 问题
runpodctl ssh          # 管理 SSH 密钥和连接
```

#### 6. SSH 密钥管理

```bash
runpodctl ssh add-key      # 将 SSH 公钥添加到您的账户
runpodctl ssh list-keys    # 列出所有已添加的 SSH 密钥
```

---

### 输出格式

默认输出为 JSON（针对代理优化）。使用 `--output` 标志进行其他格式选择：

```bash
runpodctl pod list                   # JSON（默认）
runpodctl pod list --output=table    # 人类可读的表格
runpodctl pod list --output=yaml     # YAML 格式
```

---

### RunPod 项目——无 Docker Serverless 工作流

RunPod 在 `runpodctl` 版本 1.11.0+ 中引入了“无 Docker”功能，简化了 AI 开发过程，允许您在 serverless 平台上部署自定义端点，无需处理 Docker 的复杂性。

该流程包括：
1.  使用您的 API 密钥配置 `runpodctl`
2.  创建一个新项目（提示设置并创建项目文件夹）
3.  启动开发会话
4.  部署您的 Serverless 端点

生成的项目文件包括：
-   `.runpodignore` — 指定部署时要排除的文件
-   `builder/requirements.txt` — pip 依赖项
-   `runpod.toml` — 项目配置和部署设置

```bash
# 创建一个新项目
runpodctl project create -n my-project && cd my-project

# 启动开发会话（自动同步代码更改）
runpodctl project dev

# 部署为 Serverless 端点
runpodctl project deploy
```

这会在您的本地环境与一个 RunPod Pod 之间建立连接。对代码的更改会自动同步到 Pod，从而实现无需重建 Docker 镜像的实时测试。

---

### 通过 JSON 配置 Pod（高级）

您可以使用 JSON 配置文件创建 Pod。有三种示例类型：最小配置、完整配置以及 Spot/可中断配置。所有 Pod 配置字段都是可选的，并有合理的默认值。

JSON 配置示例：

```json
{
  "name": "开发 Pod",
  "imageName": "runpod/pytorch:2.0.0-py3.10-cuda11.8.0-devel-ubuntu22.04",
  "cloudType": "SECURE",
  "gpuTypeIds": ["NVIDIA GeForce RTX 4090"],
  "gpuCount": 1,
  "containerDiskInGb": 50,
  "volumeInGb": 100,
  "ports": ["8888/http", "22/tcp"]
}
```

```bash
runpod-cli pods create --config my-pod.json
```

---

### CI/CD 集成

RunPod 的 MLOps 集成围绕着全面的 API 和 CLI 支持，以实现 CI/CD 流水线集成。该平台通过 RESTful API 调用和命令行界面，与 GitHub Actions、GitLab CI、Jenkins 和 CircleCI 协同工作。

您可以通过将 API 密钥作为密钥存储在 CI/CD 系统中，并在流水线步骤中调用 `runpodctl` 命令来自动化部署——例如，在测试通过后启动 Pod，或部署新的 Serverless 端点版本。

---

### 获取帮助

```bash
runpodctl help                # 通用帮助
runpodctl [command] help      # 特定命令的帮助
runpodctl doctor              # 诊断并修复问题
```

---

### 概要表格

| 类别 | 命令 |
|---|---|
| Pod 生命周期 | `pod list`, `pod get`, `pod create`, `pod start`, `pod stop`, `pod delete` |
| Serverless | `serverless list/get/create/update/delete` |
| 文件传输 | `send`, `receive` |
| 项目 | `project create`, `project dev`, `project deploy` |
| 存储 | `network-volume`（别名 `nv`） |
| SSH | `ssh add-key`, `ssh list-keys` |
| 信息 | `user`, `gpu`, `datacenter`, `billing` |
| 实用程序 | `doctor`, `update`, `version` |

---

**参考文献：**

-   [RunPod CLI 官方文档（概述）](https://docs.runpod.io/runpodctl/overview)
-   [runpodctl GitHub 仓库](https://github.com/runpod/runpodctl)
-   [RunPod CLI — DeepWiki](https://deepwiki.com/runpod/docs/5.1-runpod-cli-(runpodctl))
-   [RunPod 无 Docker CLI 博客文章](https://www.runpod.io/blog/dockerless-cli-runpod)
-   [RunPod 文件传输文档](https://docs.runpod.io/pods/storage/transfer-files)
-   [runpodctl Go 包参考](https://pkg.go.dev/github.com/runpod/runpodctl)
-   [Pod 配置示例（MomentFactory）](https://github.com/MomentFactory/runpod-cli/blob/main/examples/POD_CONFIG.md)
