---
audio: false
generated: true
lang: zh
layout: post
title: 安装GitHub命令行工具
translated: true
type: note
---

要在 Ubuntu 系统上安装 GitHub CLI (`gh`) 并使用 `gh workflow run` 命令触发 GitHub Actions 工作流，请按照以下步骤操作：

### GitHub CLI (`gh`) 在 Ubuntu 上的安装步骤

1. **添加 GitHub CLI 软件仓库和 GPG 密钥**：
   在终端中运行以下命令来设置官方的 GitHub CLI 软件包仓库：

   ```bash
   (type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
   && sudo mkdir -p -m 755 /etc/apt/keyrings \
   && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
   && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
   && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
   ```

   该脚本会：
   - 若尚未安装则自动安装 `wget`
   - 创建 APT 密钥环目录
   - 下载并添加 GitHub CLI 的 GPG 密钥
   - 为您的系统配置 GitHub CLI 仓库

2. **更新软件包索引并安装 `gh`**：
   更新软件包列表并安装 `gh` 命令行工具：

   ```bash
   sudo apt update
   sudo apt install gh -y
   ```

3. **验证安装**：
   通过运行以下命令检查 `gh` 是否正确安装：

   ```bash
   gh --version
   ```

   您应该看到类似 `gh version X.Y.Z (YYYY-MM-DD)` 的输出，确认安装成功。

4. **通过 GitHub 认证**：
   在使用 `gh` 前，请先通过您的 GitHub 账户进行认证：

   ```bash
   gh auth login
   ```

   按照提示操作：
   - 选择 `GitHub.com`（如适用也可选择企业服务器）
   - 选择首选协议（`HTTPS` 或 `SSH`；若已设置 SSH 密钥推荐使用 `SSH`）
   - 选择认证方式（浏览器方式最便捷，会自动打开登录网页）
   - 复制提供的一次性代码，粘贴到浏览器中并授权 `gh`
   - 确认默认设置或按需调整

   成功认证后，您将看到确认信息。

### 使用 `gh workflow run` 操作 GitHub Actions

`gh workflow run` 命令用于触发 GitHub Actions 工作流。使用方法如下：

1. **进入代码仓库目录**（可选）：
   如果您位于与 GitHub 关联的本地 Git 仓库中，`gh` 会自动检测。否则请使用 `--repo` 标志指定仓库。

2. **列出可用工作流**（可选）：
   要查找工作流 ID 或文件名，请运行：

   ```bash
   gh workflow list
   ```

   这将显示仓库中的所有工作流，包括名称、ID 和状态（如 `active`）。

3. **运行工作流**：
   使用 `gh workflow run` 命令配合工作流文件名或 ID。例如：

   ```bash
   gh workflow run workflow.yml
   ```

   或使用工作流 ID（如 `123456`）：

   ```bash
   gh workflow run 123456
   ```

   如果工作流需要输入参数，使用 `--field` 标志提供：

   ```bash
   gh workflow run workflow.yml --field key=value
   ```

   要指定分支或引用，使用 `--ref` 标志：

   ```bash
   gh workflow run workflow.yml --ref branch-name
   ```

4. **监控工作流**：
   触发后，检查运行状态：

   ```bash
   gh run list
   ```

   要实时查看特定运行的进度，使用：

   ```bash
   gh run watch <run-id>
   ```

   将 `<run-id>` 替换为 `gh run list` 中的运行 ID。

### 故障排除提示

- **GPG 签名错误**：如果在 `apt update` 时遇到 GPG 相关问题，请参考 GitHub 问题追踪器寻找解决方案（如 `cli/cli#9569`）或重试密钥导入步骤。[](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
- **防火墙问题**：如果 `keyserver.ubuntu.com` 连接失败，请尝试：

   ```bash
   sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key C99B11DEB97541F0
   ```

   如需可安装 `dirmngr`：

   ```bash
   sudo apt-get install dirmngr
   ```

  [](https://gist.github.com/Manoj-Paramsetti/dc957bdd6a4430275d0fc28a0dc43ae9)
- **Snap 安装警告**：GitHub 因运行时问题不推荐使用 Snap 软件包安装 `gh`。请坚持使用上述 APT 方法。[](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
- **认证范围**：如果 `gh workflow run` 因权限失败，请确保您的令牌具有 `workflow` 范围。可通过以下命令重新认证：

   ```bash
   gh auth refresh -s workflow
   ```

### 补充说明

- **GitHub CLI 手册**：要了解 `gh` 命令的更多详情，请运行 `gh help` 或访问官方手册 [cli.github.com](https://cli.github.com)。[](https://cli.github.com/manual/)
- **工作流要求**：请确保工作流文件（如 `workflow.yml`）存在于仓库的 `.github/workflows/` 目录中，并配置为支持手动触发（如 `workflow_dispatch` 事件）。
- **替代安装方法**：您也可以通过 Homebrew（`brew install gh`）或从[发布页面](https://github.com/cli/cli/releases)下载二进制文件来安装 `gh`，但推荐在 Ubuntu 系统中使用 APT 方法。[](https://github.com/cli/cli)

此设置使您能够在 Ubuntu 系统中通过命令行高效管理 GitHub Actions 工作流。如果您需要有关特定 `gh` 命令或工作流配置的帮助，请随时告知！
