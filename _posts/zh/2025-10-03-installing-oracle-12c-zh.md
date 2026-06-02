---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在Ubuntu系统上安装Oracle 12c数据库
translated: true
type: note
---

### 在 Ubuntu 22.04 x86_64 上通过压缩包安装 Oracle Database 12c 第 1 版（12.1.0.2 含补丁 12.1.2？）

文件 `v12.1.2_linuxx64_server_dec.tar.gz` 似乎是 Oracle Database 12c 第 1 版的压缩包（可能是版本 12.1.0.2 捆绑了 12.1.2 补丁，服务器版，可能 "dec" 表示已解除配置）。这是较旧版本的 Oracle Database（约 2013-2014 年发布），且 Oracle **不正式支持 Ubuntu**。在 Ubuntu 22.04（使用现代库如 glibc 2.35）上安装可能可行，但可能需要解决兼容性问题，例如库链接或内核参数。预计会出现依赖项错误——请先在虚拟机中测试。

**警告：**
- Oracle 12c 扩展支持已终止（截至 2022 年），因此用于测试/生产环境需自行承担风险。生产环境请考虑使用 19c 或 23ai 等更新版本。
- 需要 root/sudo 权限。
- 最低硬件要求：2 GB RAM（推荐 8 GB），2 个 CPU 核心，10 GB 可用磁盘空间用于软件（数据库需要更多空间）。
- 操作前备份系统。
- 如果此压缩包非来自 Oracle 官方源，请验证其完整性（例如校验和）以避免恶意软件。

#### 步骤 1：准备系统
1. **更新 Ubuntu**：
   ```
   sudo apt update && sudo apt upgrade -y
   ```

2. **安装所需依赖项**：
   Oracle 12c 需要特定库。通过 apt 安装：
   ```
   sudo apt install -y oracle-java8-installer bc binutils libaio1 libaio-dev libelf-dev libnuma-dev libstdc++6 unixodbc unixodbc-dev
   ```
   - 如果 `oracle-java8-installer` 不可用（位于旧仓库中），请添加 Oracle 的 Java PPA 或手动下载 JDK 8：
     ```
     sudo add-apt-repository ppa:webupd8team/java -y
     sudo apt update
     sudo apt install oracle-java8-installer -y
     ```
     安装过程中接受许可证。设置 JAVA_HOME：
     ```
     echo 'export JAVA_HOME=/usr/lib/jvm/java-8-oracle' >> ~/.bashrc
     source ~/.bashrc
     ```

3. **创建 Oracle 用户和组**：
   以 root 或使用 sudo 运行：
   ```
   sudo groupadd -g 54321 oinstall
   sudo groupadd -g 54322 dba
   sudo useradd -u 54321 -g oinstall -G dba -s /bin/bash oracle
   sudo passwd oracle  # 为 oracle 用户设置密码
   ```

4. **配置内核参数**：
   编辑 `/etc/sysctl.conf`：
   ```
   sudo nano /etc/sysctl.conf
   ```
   添加以下行（根据您的 RAM/磁盘调整；这些是最低值）：
   ```
   fs.file-max = 6815744
   kernel.sem = 250 32000 100 128
   kernel.shmmni = 4096
   kernel.shmall = 1073741824
   kernel.shmmax = 4398046511104
   kernel.panic_on_oops = 1
   net.core.rmem_default = 262144
   net.core.rmem_max = 4194304
   net.core.wmem_default = 262144
   net.core.wmem_max = 1048576
   fs.aio-max-nr = 1048576
   vm.swappiness = 0
   ```
   应用更改：
   ```
   sudo sysctl -p
   ```

5. **为 Oracle 用户设置 Shell 限制**：
   编辑 `/etc/security/limits.conf`：
   ```
   sudo nano /etc/security/limits.conf
   ```
   添加：
   ```
   oracle soft nproc 2047
   oracle hard nproc 16384
   oracle soft nofile 1024
   oracle hard nofile 65536
   oracle soft stack 10240
   oracle hard stack 32768
   ```
   编辑 `/etc/pam.d/login` 并添加：
   ```
   sudo nano /etc/pam.d/login
   ```
   追加：`session required pam_limits.so`

6. **创建目录**：
   ```
   sudo mkdir -p /u01/app/oracle/product/12.1.0/dbhome_1
   sudo mkdir -p /u01/app/oraInventory
   sudo chown -R oracle:oinstall /u01
   sudo chmod -R 775 /u01
   ```

7. **交换空间**（如果 RAM < 8 GB，添加交换空间）：
   对于 2 GB RAM，创建 2 GB 交换文件：
   ```
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```

8. **禁用防火墙/SElinux**（如果启用）：
   ```
   sudo ufw disable  # 或根据需要配置端口 1521、5500
   sudo apt remove apparmor -y  # 如果 AppArmor 干扰
   ```

#### 步骤 2：解压压缩包
切换到 oracle 用户：
```
su - oracle
cd ~/Downloads  # 或文件所在位置
```
解压（这将创建数据库主目录结构）：
```
tar -xzf v12.1.2_linuxx64_server_dec.tar.gz -C /u01/app/oracle/product/12.1.0/
```
- 这应创建 `/u01/app/oracle/product/12.1.0/dbhome_1` 并包含如 `runInstaller` 的文件。
- 如果压缩包解压到不同结构，请相应调整路径（例如 `database/` 目录）。

#### 步骤 3：运行安装程序
仍以 oracle 用户身份：
```
cd /u01/app/oracle/product/12.1.0/dbhome_1
./runInstaller
```
- GUI 安装程序将启动（如果通过 SSH 需要 X11 转发；使用 `ssh -X` 或启用 X11）。
- **安装选项**：
  - 选择“仅创建和配置数据库软件”或“单实例数据库安装”（用于服务器版）。
  - ORACLE_HOME：`/u01/app/oracle/product/12.1.0/dbhome_1`
  - 清单：`/u01/app/oraInventory`
  - 如果仅是软件（不创建数据库），选择“仅安装数据库软件”。
- 遵循向导：尽可能接受默认值，但设置 SYS/SYSTEM 的密码。
- 初始时忽略任何“先决条件”警告——如有需要在安装后修复。

如果 GUI 失败（例如 DISPLAY 错误），运行静默安装：
```
./runInstaller -silent -responseFile /path/to/responsefile.rsp
```
您需要准备响应文件（示例在解压目录中，例如 `db_install.rsp`）。使用您的设置（ORACLE_HOME 等）编辑它并运行。

#### 步骤 4：安装后步骤
1. **运行 root.sh**（以 root 身份）：
   ```
   sudo /u01/app/oraInventory/orainstRoot.sh
   sudo /u01/app/oracle/product/12.1.0/dbhome_1/root.sh
   ```

2. **设置环境变量**（为 oracle 用户，添加到 `~/.bash_profile`）：
   ```
   export ORACLE_HOME=/u01/app/oracle/product/12.1.0/dbhome_1
   export PATH=$ORACLE_HOME/bin:$PATH
   export ORACLE_SID=orcl  # 更改为您的 SID
   export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib
   export CLASSPATH=$ORACLE_HOME/jlib:$ORACLE_HOME/rdbms/jlib
   ```
   ```
   source ~/.bash_profile
   ```

3. **创建数据库**（如果安装期间未完成）：
   ```
   dbca  # 数据库配置助手（GUI/静默）
   ```
   或使用 SQL*Plus 进行手动创建。

4. **启动/停止服务**：
   ```
   sqlplus / as sysdba
   STARTUP;  # 或 shutdown
   ```
   添加到 systemd 以实现自动启动（创建 `/etc/systemd/system/oracle.service` 并执行 `dbstart`）。

#### 在 Ubuntu 22.04 上的常见问题排查
- **Glibc/依赖项错误**：Oracle 12c 期望 glibc <=2.17。Ubuntu 22.04 使用 2.35——使用 `ldd` 检查，或安装兼容库：
  ```
  sudo apt install libc6:i386 libncurses5:i386 libstdc++6:i386
  ```
  如果出现链接器错误，设置 `LD_PRELOAD` 或使用带有 Oracle Linux 的 Docker 容器。
- **Java/显示问题**：确保 JDK 8 已设置（`java -version` 应显示 1.8）。对于无头模式：`export DISPLAY=:0`。
- **内存不足**：增加 ulimit 或 RAM。如果需要，编辑 `runInstaller` 参数。
- **补丁 12.1.2**：如果未捆绑，从 My Oracle Support 下载并在安装后使用 `opatch` 应用。
- **日志**：检查 `/u01/app/oraInventory/logs/installActions*.log` 以查找错误。
- **兼容性修复**：一些用户符号链接库（例如 `sudo ln -s /lib/x86_64-linux-gnu/libpthread.so.0 /u01/app/oracle/product/12.1.0/dbhome_1/lib/libpthread_nonshared.a`——根据错误研究具体方法）。

#### 验证
- 运行 `sqlplus / as sysdba` 并执行 `SELECT * FROM v$version;`。
- 监听器：`lsnrctl start`。

如果遇到特定错误，请提供日志输出以获取更多帮助。有关官方（尽管以 RHEL 为重点）文档，请参阅 Oracle 的 12c 安装指南。如果这是用于其他产品（非数据库），请澄清压缩包内容！
