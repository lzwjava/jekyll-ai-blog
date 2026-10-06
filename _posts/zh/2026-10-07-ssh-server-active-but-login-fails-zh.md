---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH服务器运行中但登录失败
translated: true
type: note
---

**结论：SSH服务器已安装并在192.168.1.137上运行。** 连接失败是由于身份验证问题，而非服务器缺失。

收集的证据：

| 检查项 | 结果 |
|---|---|
| 主机可达性（ping） | ✅ 可达（延迟约2.9ms） |
| TCP端口22 | ✅ 开放（检测到`ssh`服务） |
| SSH服务器（sshd） | ✅ 已安装并运行 — 返回了SSH协议握手，支持`publickey,password`认证方式 |
| 登录认证 | ❌ 失败：`Permission denied (publickey,password)` |

为何我确信服务器已安装：`nc`报告端口22为`ssh`，且SSH客户端已到达**认证阶段**，收到了服务器返回的认证方式列表（`publickey,password`）——该响应仅在sshd正在运行时才会出现。

**为何当前登录失败：** 我尝试了三个本地密钥（`~/.ssh/id_rsa`、`~/.ssh/id_ed25519`、`private_key.pem`），远程主机均拒绝用于用户`lzw`。此外，`BatchMode=yes`阻止了交互式密码输入。

登录方式：
1. **交互式密码登录**：`ssh lzw@192.168.1.137`（会提示输入lzw的密码）
2. **设置密钥认证**：一旦能登录，运行`ssh-copy-id lzw@192.168.1.137`安装你的公钥，之后即可无密码访问

是否需要我尝试交互登录（你需要提供密码），或者运行其他检查？