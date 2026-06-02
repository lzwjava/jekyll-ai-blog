---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为本地自定义域名绕过代理
translated: true
type: note
---

## 问题

您有一个本地服务（例如 Uptime Kuma）在您的 LAN 服务器上运行，您希望通过自定义域名如 `http://myapp.local:3001` 访问它，而不是使用 IP 地址。

您已将条目添加到 `/etc/hosts`：

```
192.168.1.36 myapp.local
```

`ping myapp.local` 有效，但 **浏览器无法连接**。

## 根本原因

系统代理（ClashX、V2Ray、Surge 等）正在拦截 HTTP/HTTPS 流量。代理不知道 `myapp.local` 是本地地址，因此尝试通过外部隧道路由它 — 这会失败。

**关键洞察：** `ping` 和 `curl`（无代理环境变量）绕过代理。浏览器遵守系统代理设置。

## 解决方案：为本地域名绕过代理

### 步骤 1：识别您的代理工具

macOS 上常见的：

- **ClashX** / **ClashX Pro**
- **Surge**
- **V2Ray**
- **Quantumult X**

### 步骤 2：添加绕过规则

将这些添加到您的代理的 **bypass list** 或 **direct rules** 中：

```
myapp.local
*.local
192.168.1.0/24
```

#### ClashX 示例（`config.yaml`）

```yaml
bypass:
  - myapp.local
  - '*.local'
  - 192.168.1.0/24
```

#### 系统代理（macOS）

1. 系统偏好设置 → 网络 → 高级 → 代理
2. 选中 **“为这些主机和域名绕过代理设置”**
3. 添加：`myapp.local, *.local, 192.168.1.*`

### 步骤 3：验证

```bash
# 测试解析
ping myapp.local

# 无代理测试
curl --noproxy '*' http://myapp.local:3001

# 代理测试（绕过后也应有效）
curl http://myapp.local:3001
```

## 调试检查清单

| 检查 | 命令 | 预期 |
|-------|---------|----------|
| DNS 解析 | `ping myapp.local` | 解析为 `192.168.1.36` |
| 服务运行 | `curl http://192.168.1.36:3001` | HTTP 200/302 |
| 防火墙开放 | `sudo ufw status` | 端口 3001 已允许 |
| 代理绕过 | `curl --noproxy '*' http://myapp.local:3001` | HTTP 200/302 |
| 浏览器绕过 | DevTools → Network → 检查请求目标 | 直接到 LAN IP |

## 常见陷阱

1. **编辑服务器的 `/etc/hosts` 而非客户端的** — hosts 文件必须在运行浏览器的机器上
2. **忘记防火墙规则** — 在服务器上运行 `sudo ufw allow 3001/tcp`
3. **代理拦截本地流量** — 始终将 `.local` 和 LAN CIDR 添加到绕过列表
4. **浏览器 DNS 缓存** — 使用 `chrome://net-internals/#dns`（Chrome）清除或重启浏览器

## 快速参考

```bash
# 在服务器上（192.168.1.36）
sudo ufw allow 3001/tcp                    # 打开防火墙
docker ps                                  # 验证服务运行

# 在客户端上（192.168.1.37）
echo "192.168.1.36 myapp.local" >> /etc/hosts  # DNS 映射
# 然后将 myapp.local 添加到代理绕过列表
```
