---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu SSH服务器设置指南
translated: true
type: note
---

**问题：** 如何在 Ubuntu 上设置并启动 SSH 服务器？

**答案：**

以下是在 Ubuntu 上安装并启用 SSH 服务器的步骤：

**1. 安装 OpenSSH 服务器**
```bash
sudo apt update
sudo apt install openssh-server -y
```

**2. 启动并启用 SSH 服务**
```bash
sudo systemctl start ssh
sudo systemctl enable ssh   # 开机自启动
```

**3. 检查服务状态**
```bash
sudo systemctl status ssh
```
输出中应显示 `active (running)`。

**4. 允许 SSH 通过防火墙（UFW）**
```bash
sudo ufw allow ssh
sudo ufw enable        # 如果 UFW 尚未启用
sudo ufw status        # 验证规则
```

**5. 查找您的 IP 地址（供客户端连接）**
```bash
ip a
# 或
hostname -I
```

**6. 从另一台机器连接**
```bash
ssh username@your-server-ip
```

---

**可选：基本 SSH 配置**

编辑 `/etc/ssh/sshd_config` 配置文件以自定义设置（例如，更改端口、禁用 root 登录）：
```bash
sudo nano /etc/ssh/sshd_config
```

配置文件修改后，重启 SSH：
```bash
sudo systemctl restart ssh
```

---

**参考资料：**
- [Ubuntu SSH 服务器文档](https://ubuntu.com/server/docs/service-openssh)
- [OpenSSH 手册](https://www.openssh.com/manual.html)
- [UFW 防火墙指南](https://help.ubuntu.com/community/UFW)