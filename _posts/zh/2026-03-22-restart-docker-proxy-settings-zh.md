---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重启 Docker 以应用代理设置
translated: true
type: note
---

Sure，以下是完整分析：

---

## 根本原因：Docker Daemon Proxy 未应用

### 错误信息
```
Get "https://auth.docker.io/token?account=lzwjava&scope=repository%3Alibrary%2Fnode%3Apull&service=registry.docker.io": EOF
```

### 发生的情况

Docker Hub 在拉取任何镜像前都需要 auth token。流程如下：

1. Docker 联系 `registry-1.docker.io` 获取镜像 manifest
2. Registry 返回 "401 — 去 `auth.docker.io` 获取 token"
3. Docker 访问 `auth.docker.io/token?scope=...`
4. Auth server 返回 JWT token
5. Docker 使用 token 重试 manifest 请求
6. 下载镜像层

**第 3 步失败了。** 与 `auth.docker.io` 的 TCP 连接收到 `EOF` — 意味着连接立即被断开。这通常发生在防火墙或网络路径阻断了连接（在 HK/China 访问 Docker Hub 时很常见）。

### 为什么 Proxy 没有生效

你的机器运行 **mihomo**（基于 Clash 的 proxy）在 `localhost:7890`。`daemon.json` 已配置 proxy 设置：

```json
{
  "proxies": {
    "http-proxy": "http://localhost:7890",
    "https-proxy": "http://localhost:7890",
    "no-proxy": "localhost,127.0.0.1,.local"
  }
}
```

但问题是 — **Docker daemon 不会热重载 `daemon.json` 中的 proxy 配置**。编辑 `daemon.json` 后，运行中的 `dockerd` 进程不会读取变更。proxy 设置只是被*写入*，从未*应用*到运行中的 daemon。

我确认了 proxy 本身工作正常：
```
$ curl -x http://localhost:7890 https://registry-1.docker.io/v2/
{"errors":[{"code":"UNAUTHORIZED","message":"authentication required"}]}
```

`UNAUTHORIZED` 响应是正常的 — 它表示 proxy 成功到达 Docker Hub（只是说“先登录”）。所以 proxy 是可用的；只是 Docker 没有使用它。

### 修复方法

```bash
sudo systemctl restart docker
```

重启 Docker 强制 `dockerd` 重新读取 `daemon.json` 并应用 proxy 配置。重启后，所有 Docker Hub 的出站流量都会通过 mihomo → proxy server → Docker Hub 路由，绕过被阻断的连接。

### 验证

```
$ docker pull node:16-bullseye
e12e3f6cbdd8: Pull complete
139c9fa440fc: Pull complete
Status: Downloaded newer image for node:16-bullseye ✅
```

两个镜像（`node:16-bullseye` 和 `node:16-buster`）都通过 proxy 成功拉取。

### 为什么 curl 有效但 Docker 无效

**curl** 显式使用了 `-x http://localhost:7890` — 我告诉它通过 proxy 路由。

**dockerd** 是一个长期运行的 daemon。它在启动时读取配置。运行中编辑 `daemon.json` 就像修改配置文件而不重启服务 — 变更只存在于磁盘上，但进程仍使用启动时的内存配置。

### 总结

| 项目 | 修改前 | 修改后 |
|---|---|---|
| Docker daemon proxy | 已写入配置，未应用 | 重启后应用 |
| `auth.docker.io` 连接 | EOF（被阻断） | ✅ 通过 mihomo 路由 |
| `node:16-bullseye` 镜像 | 未缓存 | 本地缓存 |
| `node:16-buster` 镜像 | 未缓存 | 本地缓存 |
| Runner 服务 | 停止（Docker 重启导致） | 已重启，运行中 |

---

够清楚吗，老板？