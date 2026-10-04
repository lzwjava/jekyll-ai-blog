---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Ubuntu上启用SSH服务器
translated: true
type: note
---

问题：如何在 Ubuntu 上启用并启动 SSH 服务器？

答案：

1. **安装 OpenSSH 服务器**
   ```bash
   sudo apt update
   sudo apt install openssh-server
   ```

2. **启动服务并设置开机自启**
   ```bash
   sudo systemctl enable --now ssh
   ```

3. **检查服务是否运行**
   ```bash
   sudo systemctl status ssh
   ```
   你应该看到 `active (running)`。

4. **允许 SSH 通过防火墙（如果 UFW 已启用）**
   ```bash
   sudo ufw allow ssh
   sudo ufw status
   ```

5. **查找你的 IP 地址**
   ```bash
   ip a
   ```

6. **从另一台机器连接**
   ```bash
   ssh username@your_server_ip
   ```

**常用命令**
- 配置更改后重启：`sudo systemctl restart ssh`
- 停止服务：`sudo systemctl stop ssh`
- 配置文件：`/etc/ssh/sshd_config`

**安全提示**
- 使用 SSH 密钥认证，并在密钥正常工作后将 `sshd_config` 中的 `PasswordAuthentication` 设置为 `no`。
- 设置 `PermitRootLogin no` 以阻止直接 root 登录。
- 可选：更改默认端口（22）并更新防火墙规则以匹配。

参考资料：
- [Ubuntu Server 文档：OpenSSH 服务器](https://documentation.ubuntu.com/server/how-to/security/openssh-server/)
- [Ubuntu 社区帮助 Wiki：SSH](https://help.ubuntu.com/community/SSH)