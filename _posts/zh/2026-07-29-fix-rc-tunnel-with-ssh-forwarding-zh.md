---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用SSH转发修复RC隧道
translated: true
type: note
---

## ❌ RC Tunnel — 此 Pod 无法修复

**根本原因：** 这是一个在 **隧道功能启用之前** 创建的旧 Notebook Pod。平台从未注入 `FRP_BROKER_URL`，因此：
- 安装脚本拒绝运行
- 之前的客户端凭据（`krXGr4aWPwFUYOzWQgLPOX13xL2-Zn5-mtBcqkWq2_g`）已 **过期**（`invalid_client`）
- 无法从 Pod 内部注册新的客户端

平台文档证实：*“关闭并重新创建 Notebook，然后重试。”*

---

## ✅ 可用的替代方案 — SSH 端口转发

在 **本地机器** 上运行以下命令，即可立即访问服务：

### AI 视频生成器（AHL 演示）— 端口 8000
```bash
ssh -L 8000:localhost:8000 -p 31005 root@36.150.116.206 -N
```
然后打开：**http://localhost:8000**

### Jupyter Lab — 端口 8888
```bash
ssh -L 8888:localhost:8888 -p 31005 root@36.150.116.206 -N
```
然后打开：**http://localhost:8888/instances/u-9758-811746f0/**（令牌：`amd-oneclick`）

### 隧道演示页面 — 端口 8081
```bash
ssh -L 8081:localhost:8081 -p 31005 root@36.150.116.206 -N
```
然后打开：**http://localhost:8081**

> 💡 添加 `-f` 参数可在后台运行，例如 `ssh -f -L 8000:localhost:8000 -p 31005 root@36.150.116.206 -N`

---

## 🔄 获取公共 URL（正确修复）

您需要从平台控制台 **重新创建 Notebook** — 关闭此 Pod 并启动一个新的。之后，隧道将自动工作：

```bash
/var/run/secrets/frp-self-service/install
rc-tunnel expose --port 8000
```

需要我现在为您设置 SSH 端口转发吗？