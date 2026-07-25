---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FRP隧道系统架构
translated: true
type: note
---

好问题！以下是整个系统在底层的工作原理：

---

## 🧠 架构：FRP隧道系统

`rc-tunnel` 工具是一个基于 [**frp**（Fast Reverse Proxy）](https://github.com/fatedier/frpc) 构建的 **客户端-服务器隧道**。下面是完整的架构图：

### 1. 核心组件

```
┌──────────────────────────────────┐       ┌──────────────────────────────┐
│     你的笔记本 (Pod)             │       │   平台 / Ops 端             │
│                                  │       │                              │
│  ┌──────────┐   ┌───────────┐    │       │  ┌──────────────────────┐   │
│  │ 你的应用  │──▶│ frpc      │────┼──────▶│  │ frps（代理服务器）    │   │
│  │ :8081     │   │ (客户端)   │    │       │  │ :8443                 │   │
│  └──────────┘   └───────────┘    │       │  └──────┬───────────────┘   │
│                                  │       │         │                    │
│   身份与密钥：                    │       │  ┌──────▼───────────────┐   │
│   /var/run/secrets/frp-self-     │       │  │ 公共 Nginx/代理       │   │
│     service/                     │       │  │ *.radeon.firstdg.ai  │   │
│     ├── ca.crt  (TLS CA)         │       │  └──────────────────────┘   │
│     ├── token   (JWT 认证)       │       └──────────────────────────────┘
│     ├── namespace                │
│     └── install (脚本)           │               🌐 互联网
│                                  │                   │
└──────────────────────────────────┘         ┌─────────▼──────────┐
                                             │ 最终用户的浏览器   │
                                             │ curl https://rc-... │
                                             └────────────────────┘
```

### 2. 启动流程

以下是逐步执行的逻辑：

```
第1步：身份注入
─────────────────────────
Kubernetes 将以下内容注入 Pod：
  ├── /var/run/secrets/frp-self-service/ca.crt   ← TLS 信任锚点
  ├── /var/run/secrets/frp-self-service/token    ← 用于认证的 JWT
  ├── /var/run/secrets/frp-self-service/namespace ← K8s 命名空间
  └── 环境变量（通过 PID 1）：
      ├── FRP_BROKER_URL = https://10.110.220.177:8443
      └── FRP_BROKER_TLS_SERVER_NAME = frp-broker.frp-self-service-poc.svc.cluster.local

第2步：安装脚本
──────────────────────
/var/run/secrets/frp-self-service/install 执行以下操作：
  1. 验证环境变量是否存在（FRP_BROKER_URL, FRP_BROKER_TLS_SERVER_NAME）
  2. 从代理下载 rc-tunnel 二进制文件：
     curl --cacert ca.crt \
          --connect-to <tls_host>:<port>:<broker_ip>:<port> \
          https://<tls_host>:<port>/downloads/rc-tunnel-linux-amd64
     → --connect-to 绕过 DNS（这是一个集群内部服务）
  3. 安装到 ~/.local/bin/rc-tunnel
  4. 将 ~/.local/bin 添加到 PATH（在 .bashrc/.profile 中）

第3步：认证
──────────────────────
当你运行 "rc-tunnel expose --port 8081" 时：
  1. rc-tunnel 从 /var/run/secrets/frp-self-service/token 读取 JWT 令牌
  2. 使用该令牌向 FRP 代理进行认证
  3. 代理的 frps 验证 JWT（由 Kubernetes API 服务器签名）
  4. 成功后，代理分配一个唯一域名：rc-<random>.radeon.firstdg.ai

第4步：隧道建立
─────────────────────────────
  1. rc-tunnel 在 ~/.local/state/rc-tunnel/frpc.toml 生成 frpc 配置文件
  2. 下载 frpc 二进制文件（实际的 FRP 客户端）
  3. 以子进程形式启动 frpc（在我们的例子中 PID 为 1140）
  4. frpc 打开到 frps 的持久 TCP 连接（10.110.220.177:8443）
  5. 双方使用 CA 证书进行双向 TLS 验证
  6. frps 注册代理路由：rc-a899e6bb9beab78e → 该 Pod 的 :8081

第5步：请求流程
─────────────────────
  用户 → https://rc-a899e6bb9beab78e.radeon.firstdg.ai
         ↓
  DNS 解析 → 平台的公共负载均衡器
         ↓
  Nginx/代理（平台端） → frps（代理）
         ↓
  frps 查找路由 → 找到我们的 frpc 连接
         ↓
  frps 通过持久 TCP 隧道转发 HTTP 请求
         ↓
  我们 Pod 中的 frpc 接收请求 → 转发到 127.0.0.1:8081
         ↓
  我们的 Python HTTP 服务器响应 → 响应通过隧道返回
```

### 3. 为什么环境变量不在 Shell 中

这是我们遇到的一个棘手问题。笔记本 **确实是** 足够新的 Pod（它拥有身份目录），但是：

```bash
# 这些变量在容器启动时设置，但并未导出到登录 shell：
/proc/1/environ 包含：
  FRP_BROKER_URL=https://10.110.220.177:8443
  FRP_BROKER_TLS_SERVER_NAME=frp-broker.frp-self-service-poc.svc.cluster.local

# 但是当你通过 SSH 登录时，你的 shell 并不会继承它们
echo $FRP_BROKER_URL  # (空)
```

这就是为什么我们必须手动从 `/proc/1/environ` 中 source 它们——Pod 初始化将它们注入到 PID 1，但没有写入 `/etc/environment` 或 profile 脚本。

### 4. 安全模型

| 层级 | 机制 |
|-------|-----------|
| **TLS 传输** | frpc ↔ frps 之间双向 TLS，通过 `ca.crt` 验证 |
| **认证** | 由 Kubernetes API 服务器签名的 JWT 令牌（服务账户） |
| **身份绑定** | 令牌嵌入了 Pod 名称、命名空间和节点信息——frps 验证该 Pod 是否有权暴露端口 |
| **无密钥共享** | 切勿将 `~/.local/state/rc-tunnel` 或令牌复制到其他 Pod |
| **用户责任** | 隧道 URL 是公开的——你的应用必须自行实施身份验证 |

### 5. 生命周期

```
                    ┌────────────┐
                    │ Pod 启动   │
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │ 安装       │  ← 运行一次安装脚本
                    │ rc-tunnel  │
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │ rc-tunnel  │  ← "expose --port 8081"
                    │ expose     │     请求域名，启动 frpc
                    └─────┬──────┘
                          │
               ┌──────────▼──────────┐
               │ 隧道激活            │  ← 公共 URL 生效
               │ PID: 1140           │     每 N 秒心跳
               └──────────┬──────────┘
                          │
               ┌──────────▼──────────┐
               │ rc-tunnel stop      │  ← 域名进入 24 小时冻结期
               │ （或 Pod 终止）     │     端口立即释放
               └─────────────────────┘
```

### 6. “旧 Pod”检查

安装脚本会预先进行以下检查：

```bash
broker_url=${FRP_BROKER_URL:?FRP_BROKER_URL is not injected into this Notebook}
tls_host=${FRP_BROKER_TLS_SERVER_NAME:?FRP_BROKER_TLS_SERVER_NAME is not injected into this Notebook}
```

`:?` 在 bash 中的含义是 **“如果变量未设置或为空，则打印此错误并退出”**。因此，如果环境变量根本不存在（旧 Pod 的情况），脚本会立即失败并显示该消息——如果不重新创建笔记本，你将无法继续。

---

**简而言之：** 笔记本充当 frpc 客户端，打开一条到中央 frps 代理的持久 TCP 连接。代理分配一个公共子域名，并通过该隧道将 HTTP 流量反向代理回你的本地端口。这就像一个为此平台量身定制的、经过认证的 ngrok。