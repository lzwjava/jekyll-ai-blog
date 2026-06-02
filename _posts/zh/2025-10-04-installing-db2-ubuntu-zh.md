---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在Ubuntu上安装IBM Db2
translated: true
type: note
---

### 在 Ubuntu 22.04 或 24.04 上从 `ibm_db2_v12.1.2_linuxx64_server_dec.tar.gz` 安装 IBM Db2 12.1.2

IBM Db2 版本 12.1.2（修订包 2）支持最新的 Ubuntu 版本，包括 22.04（Jammy）和 24.04（Noble），只要您的系统满足硬件和软件先决条件。本安装使用 tar.gz 文件中的图形或静默安装程序。建议您查阅 IBM Db2 12.1 的官方文档（例如，在 IBM Knowledge Center 或 Db2 下载页面），以获取最新详细信息，因为不同版本（此处为服务器版）的要求可能有所不同。

**开始前的重要说明：**

- **系统要求**：
  - 64 位 x86_64 架构（Intel/AMD）。
  - 至少 4 GB RAM（推荐 8 GB）和 2 GB 交换空间。
  - 基础安装需要 10 GB 可用磁盘空间（数据存储需要更多）。
  - Root 或 sudo 访问权限。
  - 内核版本：Ubuntu 22.04/24.04 应该可以工作，但请确保内核至少为 3.10（使用 `uname -r` 检查）。
  - 防火墙：临时禁用或打开端口（Db2 默认端口：50000，用于 TCP/IP）。
- **在 Ubuntu 上的潜在问题**：
  - Db2 主要在 RHEL/SUSE 上测试，但通过 Debian 包支持 Ubuntu。您可能需要解决库依赖关系。
  - 如果您使用的是 Ubuntu 24.04，它非常新——请先在虚拟机中测试，因为完全认证可能会滞后。
  - 这将安装服务器版。对于其他版本（例如 Express-C），请下载相应的 tar.gz 文件。
- **备份**：在继续之前备份您的系统。
- 从官方 IBM Passport Advantage 或 Db2 下载站点下载文件（需要 IBM ID）。

#### 步骤 1：安装先决条件

更新系统并安装所需的库。Db2 需要异步 I/O、PAM 和其他运行时库。

```bash
sudo apt update
sudo apt upgrade -y

# 安装基本包（Db2 在 Ubuntu/Debian 上的常见包）
sudo apt install -y libaio1 libpam0g:i386 libncurses5 libstdc++6:i386 \
    unixodbc unixodbc-dev libxml2 libxslt1.1 wget curl

# 对于 Ubuntu 24.04，您可能还需要：
sudo apt install -y libc6:i386 libgcc-s1:i386

# 验证 glibc 兼容性（Db2 12.1 需要 glibc 2.17+）
ldd --version  # 在 Ubuntu 22.04/24.04 上应显示 glibc 2.35+
```

如果遇到缺少 32 位库的问题（例如，对于 Java 组件），启用多架构支持：

```bash
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install -y libc6:i386 libncurses5:i386 libstdc++6:i386
```

#### 步骤 2：准备安装文件

1. 创建一个临时目录用于解压（例如，`/tmp/db2_install`）：

   ```bash
   sudo mkdir -p /tmp/db2_install
   cd /tmp/db2_install
   ```

2. 将 tar.gz 文件复制到此目录（假设您已下载，例如在 `~/Downloads` 中）：

   ```bash
   cp ~/Downloads/ibm_db2_v12.1.2_linuxx64_server_dec.tar.gz .
   ```

3. 解压存档：

   ```bash
   tar -xzf ibm_db2_v12.1.2_linuxx64_server_dec.tar.gz
   ```

   - 这将创建一个目录，如 `db2` 或 `sqllib`，其中包含安装程序文件（例如 `db2setup`）。

4. 切换到解压后的目录：

   ```bash
   cd db2  # 或者任何顶级目录——使用 `ls` 检查
   ```

#### 步骤 3：运行安装程序

Db2 提供图形安装程序（`db2setup`）或用于静默安装的响应文件。以 root/sudo 身份运行。

**选项 A：图形安装程序（推荐用于首次设置）**

1. 确保您有显示设备（如果在没有 GUI 的服务器上，使用 SSH 的 X 转发：`ssh -X user@host`）。
2. 运行安装程序：

   ```bash
   sudo ./db2setup
   ```

   - 安装向导将引导您：
     - 接受许可证。
     - 为服务器版选择“典型”安装。
     - 选择安装路径（默认：`/opt/ibm/db2/V12.1`——确保 `/opt/ibm` 存在且可写；如果需要，使用 `sudo mkdir -p /opt/ibm` 创建）。
     - 创建一个 Db2 实例（例如，“db2inst1”）——这将设置数据库管理员用户。
     - 设置身份验证（例如，本地或 LDAP）。
     - 启用功能，如 SQL 过程语言（如果需要）。
   - 安装程序将编译并设置实例。

**选项 B：静默安装（非交互式）**
如果您偏好脚本化安装：

1. 在试运行期间生成响应文件：

   ```bash
   sudo ./db2setup -g  # 在当前目录生成 `db2setup.rsp`
   ```

   编辑 `db2setup.rsp`（例如，设置 `LIC_AGREEMENT=ACCEPT`、`INSTALL_TYPE=TYPICAL`、`CREATE_DB2_INSTANCE=YES` 等）。

2. 运行静默安装：

   ```bash
   sudo ./db2setup -u db2setup.rsp
   ```

- 安装需要 10-30 分钟。注意检查 `/tmp/db2setup.log` 中的错误。

#### 步骤 4：安装后设置

1. **验证安装**：
   - 以实例所有者身份登录（例如，`db2inst1`——在安装期间创建）：

     ```bash
     su - db2inst1
     ```

   - 检查 Db2 版本：

     ```bash
     db2level
     ```

   - 启动实例：

     ```bash
     db2start
     ```

   - 测试连接：

     ```bash
     db2 connect to sample  # 如果不存在样本数据库，则创建一个
     db2 "select * from sysibm.sysdummy1"
     db2 disconnect all
     db2stop  # 完成后停止
     ```

2. **创建数据库（如果在安装期间未完成）**：

   ```bash
   su - db2inst1
   db2sampl  # 可选：创建样本数据库
   # 或创建自定义数据库：
   db2 "create database MYDB"
   db2 connect to MYDB
   ```

3. **环境设置**：
   - 将 Db2 添加到实例用户的 PATH 中（添加到 `~/.bashrc`）：

     ```bash
     export PATH=/opt/ibm/db2/V12.1/bin:$PATH
     export DB2INSTANCE=db2inst1
     ```

   - 重新加载：`source ~/.bashrc`。

4. **启用远程访问（可选）**：
   - 更新服务：

     ```bash
     su - db2inst1
     db2 update dbm cfg using SVCENAME db2i  # 或您的端口
     db2set DB2COMM=TCPIP
     db2start
     ```

   - 编辑 `/etc/services`（以 root 身份）添加：

     ```
     db2i          50000/tcp
     ```

   - 重新启动实例。

5. **防火墙配置**：

   ```bash
   sudo ufw allow 50000/tcp  # 用于 Db2 默认端口
   sudo ufw reload
   ```

#### 步骤 5：应用更新（推荐）

- 如果需要，下载并应用最新的修订包（12.1.2 是 FP2；检查 FP3+）：
  - 使用 `db2iupdt` 工具或 IBM 的更新安装程序。
- 监控日志：`/tmp/db2` 或 `/opt/ibm/db2/V12.1/instance/db2inst1/sqllib/db2dump`。

#### 常见问题故障排除

- **“没有合适的 Java 运行时”**：安装 OpenJDK：`sudo apt install openjdk-11-jre-headless`。
- **库错误（例如，libaio.so）**：确保 `libaio1` 已安装并运行 `sudo ldconfig`。
- **权限被拒绝**：以 root 身份运行安装程序；确保 `/opt/ibm` 的所有权：`sudo chown -R db2inst1:db2iadm1 /opt/ibm/db2`。
- **Glibc 不兼容**：在 Ubuntu 22.04/24.04 上不太可能，但如果出现问题，考虑使用容器（Docker）安装。
- **静默安装失败**：检查 `db2setup.log` 以获取线索。
- **Ubuntu 24.04 特定问题**：如果库依赖失败，您可能需要添加 PPA 或编译缺失的库。首先在 22.04 上测试。
- 错误？搜索 IBM 的支持论坛或作为实例用户运行 `db2diag`。

如果您遇到特定错误，请提供详细信息以获得更有针对性的帮助。对于生产用途，请考虑 IBM 的认证环境或咨询支持。成功！您的 Db2 实例现在应该已准备好创建数据库和使用。
