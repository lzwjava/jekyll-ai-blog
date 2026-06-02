---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用服务器 SSH 密钥访问实例
translated: true
type: note
---

**问题：** 如何使用服务器生成的 SSH 密钥权限访问实例？

**回答：**

如果服务器（例如 AWS EC2、Oracle Cloud、Azure 或类似云提供商）在创建实例时**为你生成了 SSH key pair**，这几乎总是意味着：

- **public key** 已自动放置在实例上（通常在 `~/.ssh/authorized_keys` 中）。
- **private key** 以可下载文件的形式提供给你（AWS 中最常见的是 `.pem` 文件）。

你使用 **private key file**（不是 public key 或“perm”）在通过 SSH 连接时进行身份验证。

### 逐步指南：访问实例

1. **定位 private key 文件**
   - 找到你在启动实例时下载的 `.pem` 文件（AWS）或其他 private key 文件。
   - 示例名称：`my-key-pair.pem`、`id_rsa` 等。
   - 确保你知道其完整路径（例如 `~/Downloads/my-key.pem` 或 `C:\keys\my-key.pem`）。

2. **设置正确的文件权限（非常重要 – SSH 会拒绝权限过松的密钥）**
   在 Linux/macOS 上：

   ```bash
   chmod 400 /path/to/your-key.pem
   ```

   在 Windows 上（如果使用 OpenSSH 或 Git Bash）：

   ```bash
   icacls "C:\path\to\your-key.pem" /inheritance:r
   icacls "C:\path\to\your-key.pem" /grant:r "%username%:F"
   ```

   这确保只有你能读取该文件。

3. **查找实例连接详细信息**
   - Public IP address 或 Public DNS name（来自云控制台）
   - 用户名（常见默认值）：
     - AWS EC2 Amazon Linux / Fedora → `ec2-user`
     - AWS Ubuntu → `ubuntu`
     - CentOS / RHEL → `centos` 或 `ec2-user`
     - Oracle Cloud → `opc`
     - Debian → `admin` 或 `debian`
     - Google Cloud → 通常是你的 Google 用户名

4. **使用 SSH 连接**
   基本命令（Linux/macOS 或带有 OpenSSH 的 Windows）：

   ```bash
   ssh -i /path/to/your-key.pem username@public-ip-or-dns
   ```

   真实示例：

   ```bash
   # AWS Amazon Linux 示例
   ssh -i ~/my-key.pem ec2-user@ec2-54-123-45-67.compute-1.amazonaws.com

   # Ubuntu 示例
   ssh -i ~/my-key.pem ubuntu@34.89.12.34

   # 非常详细模式（用于调试很有用）
   ssh -i ~/my-key.pem -v username@public-ip
   ```

5. **“Permission denied (publickey)” 错误的常见修复方法**
   - 错误的 private key 文件 → 仔细检查你是否使用了正确的文件
   - 错误的用户名字 → 检查云提供商文档
   - 密钥权限过开 → 重新运行 `chmod 400`
   - 实例安全组不允许来自你的 IP 的 SSH（端口 22）
   - 实例位于私有子网（需要 bastion/jump host 或 VPN）
   - 启动后实例上的密钥被替换/移除

短语“its perm”很可能指的是 private key 文件权限（必须是限制性的），而不是 public key。

如果你从未收到/下载任何 private key 文件，那么实例可能没有启用基于密钥的登录 — 在这种情况下，你可能需要：

- 使用云控制台的“Connect”功能（EC2 Instance Connect、Serial Console 等）
- 通过将卷挂载到其他地方重置访问权限
- 或创建并添加新的 key pair

**参考资料：**

- [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-linux-inst-ssh.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-linux-inst-ssh.html)
- [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)
