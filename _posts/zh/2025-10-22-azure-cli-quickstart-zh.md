---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Azure CLI 快速入门指南
translated: true
type: note
---

Azure CLI（命令行界面）是一套跨平台工具集，可通过命令行管理 Azure 资源。它非常适合自动化任务、编写部署脚本以及与 Azure 服务交互，无需使用 Web 门户。它支持在 Windows、macOS 和 Linux 系统上使用 Bash、PowerShell 和命令提示符。

## 安装

1. **先决条件**：确保已安装 Python 3.8 或更高版本（使用 `python --version` 检查）。

2. **通过包管理器安装**（推荐）：
   - **Windows**：使用 Winget（`winget install Microsoft.AzureCLI`）或 Chocolatey（`choco install azure-cli`）。
   - **macOS**：使用 Homebrew（`brew install azure-cli`）。
   - **Linux（Ubuntu/Debian）**：运行 `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`。
   - **其他 Linux 系统**：使用 RPM 或从官网手动下载安装。

3. **验证安装**：打开终端并运行 `az --version`。您应看到 CLI 版本信息（例如，截至 2025 年底为 2.64.0）。

有关特定平台的详细安装步骤，请参阅官方安装文档。

## 身份验证

使用 Azure CLI 前，请先登录您的 Azure 账户：

1. **交互式登录**：运行 `az login`。这将打开浏览器进行 Microsoft Entra ID 身份验证。按照提示完成登录。

2. **服务主体（用于自动化）**：使用 `az ad sp create-for-rbac --name "MyApp" --role contributor --scopes /subscriptions/{subscription-id}` 创建服务主体。然后使用 `az login --service-principal -u <app-id> -p <password> --tenant <tenant-id>` 登录。

3. **检查登录状态**：使用 `az account show` 验证当前活跃订阅。

4. **注销**：运行 `az logout`。

支持多重身份验证 (MFA)，您可以使用 `az account set --subscription <id>` 管理多个订阅。

## 基本命令

Azure CLI 使用 `az` 命令后接组（例如 `vm`、`storage`）和子命令。使用 `az --help` 获取概览，或使用 `az <group> --help` 获取特定命令帮助。

### 常用全局选项
- `--help` 或 `-h`：显示帮助信息。
- `--output table/json/yaml`：格式化输出（默认：表格）。
- `--query`：使用 JMESPath 查询过滤 JSON 输出（例如 `--query "[].name"`）。

### 关键示例
- **列出订阅**：`az account list --output table`
- **获取资源组**：`az group list --output table`
- **创建资源组**：`az group create --name "MyResourceGroup" --location "eastus"`

## 管理虚拟机
Azure CLI 擅长管理虚拟机生命周期。

1. **创建虚拟机**：
   ```
   az vm create \
     --resource-group "MyResourceGroup" \
     --name "MyVM" \
     --image Ubuntu2204 \
     --admin-username azureuser \
     --admin-password MyP@ssw0rd123! \
     --location "eastus"
   ```

2. **列出虚拟机**：`az vm list --output table`

3. **启动/停止虚拟机**：`az vm start --name "MyVM" --resource-group "MyResourceGroup"` 或 `az vm stop --name "MyVM" --resource-group "MyResourceGroup"`

4. **SSH 连接虚拟机**：`az vm ssh "MyVM" --resource-group "MyResourceGroup"`

5. **删除虚拟机**：`az vm delete --name "MyVM" --resource-group "MyResourceGroup" --yes`

## 管理存储账户
1. **创建存储账户**：
   ```
   az storage account create \
     --name mystorageaccount \
     --resource-group "MyResourceGroup" \
     --location "eastus" \
     --sku Standard_LRS
   ```

2. **上传 Blob**：首先使用 `az storage account keys list --account-name mystorageaccount --resource-group "MyResourceGroup" --query "[0].value -o tsv"` 获取密钥。然后运行：`az storage blob upload --account-name mystorageaccount --container-name mycontainer --name myfile.txt --file ./myfile.txt --auth-mode key`

## 其他常见场景
- **部署 ARM 模板**：`az deployment group create --resource-group "MyResourceGroup" --template-file template.json`
- **查询资源**：`az resource list --resource-group "MyResourceGroup" --output table`
- **更新 CLI**：`az upgrade`
- **扩展功能**：安装扩展以获取额外命令，例如 `az extension add --name azure-devops`。

对于脚本编写，可与 Bash/PowerShell 循环结合使用，或在 CI/CD 管道（如 GitHub Actions）中使用 Azure CLI。

## 提示与最佳实践
- 使用 `--dry-run` 进行预览（在支持的情况下）。
- 启用自动补全：在 Bash 中运行 `az completion`。
- 错误处理：检查退出代码（0 表示成功）并使用 `--debug` 进行故障排除。
- 安全性：避免硬编码凭据；使用环境变量或 Azure Key Vault。

## 参考文档
[安装 Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
[Azure CLI 参考文档](https://learn.microsoft.com/en-us/cli/azure/)
[Azure CLI 快速入门](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli)
