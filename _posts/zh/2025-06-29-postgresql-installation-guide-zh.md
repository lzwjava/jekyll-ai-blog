---
audio: false
generated: true
lang: zh
layout: post
title: 通过安装PostgreSQL修复psycopg2问题
translated: true
type: note
---

您遇到的错误表明 `psycopg2` 包需要 PostgreSQL 的 `pg_config` 可执行文件才能从源代码构建，但在您的系统中找不到该文件。这意味着您需要在 macOS 系统上安装 PostgreSQL 以提供必要的依赖项。以下是在 macOS 上安装 PostgreSQL 并解决此问题的步骤。

### 在 macOS 上安装 PostgreSQL 的步骤

#### 1. **使用 Homebrew 安装 PostgreSQL（推荐）**

Homebrew 是在 macOS 上安装和管理 PostgreSQL 最简单的方法。

1. **安装 Homebrew（如果尚未安装）**：
   - 打开终端并运行：

     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```

   - 按照屏幕上的说明完成 Homebrew 的安装。

2. **安装 PostgreSQL**：
   - 在终端中运行：

     ```bash
     brew install postgresql
     ```

   - 此命令将安装 PostgreSQL 及其依赖项，包括 `psycopg2` 所需的 `pg_config` 可执行文件。

3. **启动 PostgreSQL**：
   - 要启动 PostgreSQL 服务，请运行：

     ```bash
     brew services start postgresql
     ```

   - 或者，为单个会话手动启动：

     ```bash
     pg_ctl -D /opt/homebrew/var/postgres start
     ```

4. **验证安装**：
   - 检查 PostgreSQL 是否已安装并正在运行：

     ```bash
     psql --version
     ```

   - 您应该会看到 PostgreSQL 版本（例如 `psql (PostgreSQL) 17.0`）。
   - 您还可以登录到 PostgreSQL shell 进行确认：

     ```bash
     psql -U $(whoami)
     ```

#### 2. **安装 PostgreSQL 后安装 `psycopg2`**

安装 PostgreSQL 后，重试安装 `psycopg2`。`pg_config` 可执行文件现在应该在您的 PATH 中可用。

1. **安装 `psycopg2`**：
   - 运行：

     ```bash
     pip install psycopg2
     ```

   - 如果您使用的是 requirements 文件，请运行：

     ```bash
     pip install -r scripts/requirements/requirements.local.txt
     ```

2. **替代方案：安装 `psycopg2-binary`（更简单的选项）**：
   - 如果您希望避免从源代码构建 `psycopg2`（这需要 PostgreSQL 依赖项），可以安装预编译的 `psycopg2-binary` 包：

     ```bash
     pip install psycopg2-binary
     ```

   - 注意：由于潜在的兼容性问题，`psycopg2-binary` 不推荐用于生产环境，但适用于开发或测试。

#### 3. **可选：将 `pg_config` 添加到 PATH（如果需要）**

如果安装 PostgreSQL 后仍然找不到 `pg_config` 可执行文件，您可能需要手动将其添加到 PATH 中。

1. 定位 `pg_config`：
   - Homebrew 通常将 PostgreSQL 安装在 `/opt/homebrew/bin`（适用于 Apple Silicon）或 `/usr/local/bin`（适用于 Intel Mac）。
   - 验证位置：

     ```bash
     find /opt/homebrew -name pg_config
     ```

     或

     ```bash
     find /usr/local -name pg_config
     ```

2. 添加到 PATH：
   - 如果找到 `pg_config`（例如在 `/opt/homebrew/bin` 中），请通过编辑您的 shell 配置文件（例如 `~/.zshrc` 或 `~/.bash_profile`）将其添加到 PATH：

     ```bash
     echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
     ```

   - 应用更改：

     ```bash
     source ~/.zshrc
     ```

3. 验证 `pg_config`：
   - 运行：

     ```bash
     pg_config --version
     ```

   - 如果返回版本号，则 PATH 设置正确。

#### 4. **故障排除**

- **错误仍然存在**：如果 `pip install psycopg2` 仍然失败，请确保您安装了必要的构建工具：
  - 安装 Xcode 命令行工具：

    ```bash
    xcode-select --install
    ```

  - 如果需要，显式安装 `libpq`（PostgreSQL 客户端库）：

    ```bash
    brew install libpq
    ```

- **Python 版本兼容性**：确保您的 Python 版本（在您的情况下为 3.13）与 `psycopg2` 兼容。如果问题仍然存在，请考虑使用稍旧 Python 版本（例如 3.11 或 3.12）的虚拟环境：

  ```bash
  python3.11 -m venv venv
  source venv/bin/activate
  pip install psycopg2
  ```

- **检查 Homebrew**：确保 Homebrew 是最新的：

  ```bash
  brew update
  brew upgrade
  ```

#### 5. **替代安装方法（可选）**

如果您不想使用 Homebrew，可以通过以下方式安装 PostgreSQL：

- **Postgres.app**：
  - 从 [postgresapp.com](https://postgresapp.com/) 下载。
  - 按照设置说明安装并启动 PostgreSQL。
  - 如上所述，将 `bin` 目录（例如 `/Applications/Postgres.app/Contents/Versions/latest/bin`）添加到您的 PATH 中。
- **官方 PostgreSQL 安装程序**：
  - 从 [postgresql.org](https://www.postgresql.org/download/macosx/) 下载 macOS 安装程序。
  - 按照安装向导操作。

#### 6. **重试您的项目**

安装 PostgreSQL 和 `psycopg2`（或 `psycopg2-binary`）后，重试运行您的项目或重新安装 requirements：

```bash
pip install -r scripts/requirements/requirements.local.txt
```

### 附加说明

- **错误原因**：`psycopg2` 包需要 PostgreSQL 开发库（特别是 `libpq`）才能从源代码构建。通过 Homebrew 安装 PostgreSQL 会提供这些库。
- **生产环境注意事项**：对于生产环境，请使用 `psycopg2`（而不是 `psycopg2-binary`），并确保您的 PostgreSQL 版本与目标环境匹配。
- **文档**：有关更多详细信息，请参阅 `psycopg2` 安装指南：[psycopg.org/docs/install.html](https://www.psycopg.org/docs/install.html)。

如果您遇到其他问题，请分享具体的错误消息，我可以帮助进一步排除故障！
