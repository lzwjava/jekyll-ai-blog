---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 导出GPG私钥
translated: true
type: note
---

### 从服务器导出 GPG 私钥

导出私钥需要通过 SSH 或终端访问服务器。GPG 私钥属于敏感信息——请务必安全处理并在传输后删除导出文件。

1. **列出您的私钥**（通过邮箱或密钥 ID 识别密钥）：
   ```
   gpg --list-secret-keys
   ```
   查找类似 `sec   rsa4096/ABC123DEF456 2023-01-01 [SC]` 的条目。记录邮箱或密钥 ID（如 `user@example.com` 或 `ABC123DEF456`）。

2. **导出私钥**（使用 `--armor` 参数生成 ASCII 格式，便于传输）：
   ```
   gpg --export-secret-keys --armor user@example.com > private-key.asc
   ```
   - 将 `user@example.com` 替换为您的实际邮箱或密钥 ID
   - 此操作会在当前目录生成 `private-key.asc` 文件
   - 若存在多个密钥，请指定密钥 ID 确保精确：`gpg --export-secret-keys --armor ABC123DEF456 > private-key.asc`
   - **安全提示**：此操作导出的密钥不包含密码。导入时如需密码提示，需输入原密码

3. **安全传输文件**到本地笔记本电脑：
   - 使用 `scp`（在本地机器执行）：
     ```
     scp user@server-ip:/path/to/private-key.asc ./
     ```
     将 `user@server-ip` 替换为服务器信息，`/path/to/` 替换为实际路径
   - 替代方案：大文件可使用 `rsync`，图形界面可选 SFTP。避免通过邮件或未加密渠道传输

4. **清理服务器文件**：
   ```
   rm private-key.asc
   ```
   使用 `ls` 命令确认文件已删除

### 在本地笔记本电脑导入 GPG 私钥

假设已安装 GPG（Linux 可通过 `apt install gnupg`，macOS 通过 `brew install gnupg`，Windows 通过 Chocolatey 安装）

1. **导入密钥**：
   ```
   gpg --import private-key.asc
   ```
   - 将看到类似 "gpg: key ABC123DEF456: secret key imported" 的输出
   - 导入过程中若提示输入密码，请输入原始密码

2. **验证导入**：
   ```
   gpg --list-secret-keys
   ```
   您的密钥现在应出现在 "sec" 栏目下

3. **可选：设置信任级别**（若用于签名/邮件）：
   ```
   gpg --edit-key user@example.com
   ```
   - 在交互界面中输入 `trust`，选择 "ultimate"（选项 5），随后输入 `save` 和 `quit`
   - 此操作将在本地机器将密钥标记为完全可信

### 提示与警告
- **密码**：务必使用高强度密码。一旦遗忘，密钥将无法使用
- **子密钥**：若密钥包含子密钥（如用于加密），需配合 `--export-secret-subkeys` 参数一并导出
- **备份**：将导出文件存储在加密驱动器等安全存储中
- **版本**：本指南基于 GPG 2.x 测试，1.x 版本操作类似
- 更多细节请参阅官方文档：[GnuPG 手册](https://www.gnupg.org/documentation/manuals/gnupg/)
