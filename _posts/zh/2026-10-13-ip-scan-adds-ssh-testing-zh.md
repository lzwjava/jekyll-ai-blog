---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IP扫描新增SSH测试
translated: true
type: note
---

完成。`ww network ip-scan --hostname lzw` 现在会扫描网络，并测试每个存活主机的 SSH 访问。

**所做更改：**

1. **`ww/network/ip_scan.py`** — 新增 SSH 访问测试：
   - `--hostname USER` — 要在存活主机上测试的 SSH 用户名
   - `--ssh-port PORT` — 要测试的 SSH 端口（默认 22）
   - `test_ssh_access()` — 执行 `ssh -o BatchMode=yes -o PasswordAuthentication=no -o StrictHostKeyChecking=accept-new <user>@<ip> true`（仅基于密钥认证，不提示输入密码；新的主机密钥会保存到 known_hosts）
   - 测试在并行线程中运行（与 ping 扫描使用相同的信号量模式）

2. **`ww/main.py`** — 更新了 network 帮助文本，加入 `--hostname` 标志

3. **`completions/_ww`** — 添加了 `network ip-scan` 的标志补全（`--hostname`、`--ssh-port`、`--delay`、`-p`）

**在你的网络上的实际测试结果：**

- 端口 22 开放：`192.168.1.36`（认证被拒绝）、`192.168.1.34`、`192.168.1.62`、`192.168.1.137`
- **可作为 `lzw` 通过 SSH 访问：** `192.168.1.34`、`192.168.1.62`、`192.168.1.137`
- `.36` 上 SSH 正在运行，但拒绝了该密钥（权限被拒绝）

Ruff 与基线相比未显示新的 lint 错误，pyright 检查通过。在 zsh shell 中运行 `compinit` 重新加载补全，以启用新的标志。
