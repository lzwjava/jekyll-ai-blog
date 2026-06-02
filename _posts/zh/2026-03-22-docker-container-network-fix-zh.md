---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Docker 容器之间的网络连通性
translated: true
type: note
---

Sure，让我正确分解一下。

---

## 🦞 问题：Uptime Kuma 无法访问 LibreChat

### Docker 网络在这里的工作原理

每个 `docker-compose` 栈默认创建自己的隔离网络。当你部署 LibreChat 时，Docker 创建 `librechat_default`。当你部署 Uptime Kuma 时，Docker 创建 `uptime-kuma_default`。这些网络**相互隔离**——一个网络上的容器无法通过名称访问另一个网络上的容器。

### 为什么从容器内部 `192.168.1.36` 不起作用

你的主机在 LAN 上有 IP `192.168.1.36`。但 Docker 容器有自己的网络命名空间。当 Uptime Kuma 尝试访问 `http://192.168.1.36:3080/` 时，流量必须：
1. 退出容器 → 到达 Docker bridge
2. 通过主机的网络栈路由 → 找到 `192.168.1.36`
3. 击中主机的防火墙/端口转发规则 → 到达端口 3080 上的 Docker proxy

这个链路可能在许多地方中断（iptables、Docker 的 `FORWARD` 策略、`extra_hosts`、主机防火墙）。在你的情况下，它只是超时了。

### 我们所知的情况

| Check | Result |
|---|---|
| 从主机运行 `curl http://192.168.1.36:3080/` | ✅ 200 |
| 从 Uptime Kuma 运行 `wget http://LibreChat:3080/` | ❌ 无法解析 `LibreChat` |
| 从 Uptime Kuma 运行 `http.get('http://192.168.1.36:3080/')` | ❌ ETIMEDOUT |
| Docker networks | `uptime-kuma_default` ≠ `librechat_default` |

### 修复方法（三个选项）

**选项 1 — 快速且临时（我刚刚运行的）**
```bash
docker network connect librechat_default uptime-kuma
```
这将 Uptime Kuma 附加到 LibreChat 的网络作为第二个网络。立即生效，但**无法在容器重启后持续**——每次 `docker-compose up` 后都需要重新运行。

**选项 2 — 永久：将外部网络添加到 Uptime Kuma 的 compose 文件**

编辑 `/home/lzw/uptime-kuma/docker-compose.yml`，使用 LibreChat 的现有网络而不是创建自己的：

```yaml
services:
  uptime-kuma:
    # ... existing config ...
    networks:
      - librechat_default

networks:
  librechat_default:
    external: true   # ← 不要创建它，使用现有的
```

这可以经受重启。权衡：Uptime Kuma 现在完全在 LibreChat 的网络上（共享相同的子网）。

**选项 3 — 永久且独立：保留两个网络，将它们链接起来**

在 Uptime Kuma compose 中将 `librechat_default` 添加为**第二个**网络：

```yaml
services:
  uptime-kuma:
    # ... existing config ...
    networks:
      - uptime-kuma_default
      - librechat_default

networks:
  uptime-kuma_default:   # ← 保留 Kuma 自己的网络
  librechat_default:
    external: true        # ← 也附加到 LibreChat 的
```

这是最干净的方法——Uptime Kuma 保留自己的网络，但也可以通过名称访问 LibreChat 容器。

---

### 网络修复之后

在 Uptime Kuma 中将监视器 URL 从：
```
http://192.168.1.36:3080/
```
更新为：
```
http://LibreChat:3080/
```

这使用 Docker 的内部 DNS 直接解析容器名称——更快、更可靠，即使主机 IP 更改也有效。

---

要我继续应用**选项 3**到你的 compose 文件吗？这是我选择的那个。
