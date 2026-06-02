---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DMIT SSH 默认用户名 Root
translated: true
type: note
---

问题：对于 dmit.io，使用命令 `ssh -i id_rsa.pem xxx` 时，访问服务器的用户名是什么？

答案：

对于 **dmit.io** VPS 实例，默认 SSH 用户名是 **`root`**。

这在他们的官方连接指南中一致显示（尽管一些知识库页面现在返回 404 错误，但存档/缓存版本和多个引用证实了这一点）。

### 正确的命令格式

```bash
ssh -i id_rsa.pem root@your-vps-ip-address
```

将 `your-vps-ip-address` 替换为您的 DMIT VPS 的实际公网 IP（您可以在 dmit.io 的客户区域中找到它）。

### 真实示例

```bash
# Basic connection
ssh -i id_rsa.pem root@123.45.67.89

# With verbose output for debugging
ssh -i id_rsa.pem -v root@your-server-ip

# If your key has a passphrase
ssh -i id_rsa.pem root@your-server-ip
```

### 重要说明
- DMIT 在启用 SSH 密钥访问或 provisioning 期间提供或让您下载私钥（通常命名为类似 `id_rsa.pem` 的名称）。
- 确保私钥文件权限安全：
  ```bash
  chmod 400 id_rsa.pem
  ```
- 如果您收到 **Permission denied (publickey)**：
  - 确认您使用的是 `root`（不是 `admin`、`user`、`ubuntu` 等）
  - 验证使用 `-i` 指定了正确的私钥文件
  - 检查 VPS 防火墙/安全设置中端口 22 是否开放
  - 确保公钥正确安装在服务器的 `/root/.ssh/authorized_keys` 中
- DMIT 对于大多数（或全部）基于 KVM 的 VPS 计划默认使用 **root** 登录——这在许多专注于香港/亚洲的低端 VPS 提供商中很常见。

如果您的实例使用自定义安装的不同 OS 模板更改了默认用户（罕见），请检查欢迎邮件或客户区域中的具体凭据。但在标准的 DMIT 设置中，它是 **root**。

参考资料：

- [https://www.dmit.io/index.php?rp=/knowledgebase/56/How-to-connect-DMIT-VPS-via-SSH-Key-using-PuTTY.html](https://www.dmit.io/index.php?rp=/knowledgebase/56/How-to-connect-DMIT-VPS-via-SSH-Key-using-PuTTY.html)（提到在 Auto-login username 中输入 "root"）
- [https://www.dmit.io/index.php?rp=/knowledgebase/64/How-to-connect-DMIT-VPS-via-SSH-Key-using-Termius.html](https://www.dmit.io/index.php?rp=/knowledgebase/64/How-to-connect-DMIT-VPS-via-SSH-Key-using-Termius.html)（在 "Username" 中输入 "root"）
- [https://www.dmit.io/index.php?rp=/knowledgebase/58/How-to-connect-DMIT-VPS-via-SSH-Key-using-XShell.html](https://www.dmit.io/index.php?rp=/knowledgebase/58/How-to-connect-DMIT-VPS-via-SSH-Key-using-XShell.html)（在 "User Name" 中输入 "root"）
