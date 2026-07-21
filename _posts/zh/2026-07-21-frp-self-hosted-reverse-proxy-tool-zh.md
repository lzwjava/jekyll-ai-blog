---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'frp: 自托管反向代理工具'
translated: true
type: note
---

问题：什么是 `fatedier/frp`？

答案：

frp（Fast Reverse Proxy）是一个用 Go 语言编写的**反向代理/隧道工具**。它帮助将位于 NAT 或防火墙后面的服务暴露到公共互联网。

仓库地址：[https://github.com/fatedier/frp](https://github.com/fatedier/frp)

核心思想：

```
客户端机器（局域网内部）
        |
        | 出站连接
        |
        v
frpc  <----------------->  frps
                          |
                          |
                    公共服务器
                    拥有公网 IP
```

* `frps` = 服务端，运行在拥有公网 IP 的 VPS 上。
* `frpc` = 客户端，运行在 NAT 后面的机器上。

示例：

你有一个本地服务：

```
localhost:3000
```

可能是：

* 本地 Web 应用
* SSH 服务器
* Jupyter notebook
* LLM API 服务器（vLLM）
* 家庭实验室服务

你的家庭网络没有公网 IP。开始：

```
你的笔记本电脑
    |
    | frpc 隧道
    |
    v
VPS（公网 IP）
    |
    v
https://your-domain.com
```

现在全世界都可以访问你的本地服务。

---

### 典型使用场景

#### 1. 暴露本地开发服务器

本地：

```
npm run dev

localhost:5173
```

frpc 配置：

```toml
[[proxies]]
name = "frontend"
type = "http"
localIP = "127.0.0.1"
localPort = 5173
customDomains = ["demo.example.com"]
```

然后：

```
https://demo.example.com
```

会打开你的本地应用。

---

#### 2. SSH 进入 NAT 后面的机器

客户端：

```
家庭 PC
  sshd :22
```

frpc：

```toml
[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 6000
```

然后：

```bash
ssh user@your-vps-ip -p 6000
```

---

#### 3. AI / LLM 服务

与你的设置相关：

```
RTX 4070 机器
      |
      | frpc
      |
      v
云 VPS
      |
      v
兼容 OpenAI 的 API
```

示例：

```
localhost:8000/v1
```

（vLLM 服务器）

暴露：

```
https://api.example.com/v1
```

适用于：

* 远程测试 agent
* 分享演示
* 黑客马拉松
* Webhook 回调

---

### 与其他工具对比

| 工具               | 用途                         |
| ------------------ | ------------------------------- |
| frp                | 通用 TCP/HTTP 反向代理  |
| ngrok              | 简单的临时隧道          |
| Cloudflare Tunnel  | 在 Cloudflare 背后的 HTTP 服务 |
| Tailscale Funnel   | 基于 Tailnet 的共享           |
| SSH 反向隧道      | 最简的手动解决方案         |

frp 之所以流行，是因为它：

* 自托管
* 速度快
* Go 单二进制文件
* 支持 TCP/UDP/HTTP/HTTPS
* 支持身份验证
* 支持多客户端

---

### 最小化部署

VPS：

```bash
wget https://github.com/fatedier/frp/releases/latest/download/frp_linux_amd64.tar.gz

tar xzf frp_linux_amd64.tar.gz
cd frp_*
```

`frps.toml`

```toml
bindPort = 7000
```

运行：

```bash
./frps -c frps.toml
```

客户端：

`frpc.toml`

```toml
serverAddr = "your-vps-ip"
serverPort = 7000

[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 6000
```

运行：

```bash
./frpc -c frpc.toml
```

---

对于你的 AI 工作流，一个有趣的用例是：**在 GPU 机器（AMD Cloud、RunPod、家庭 GPU）上运行 vLLM/Jupyter/agent 服务器，并使用 frp 通过一个廉价的 VPS 暴露它们，而无需公网 IP。**
