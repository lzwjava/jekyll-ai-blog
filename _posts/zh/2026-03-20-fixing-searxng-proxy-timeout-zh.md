---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 SearXNG Docker 代理超时问题
translated: true
type: note
---

## 我如何解决 SearXNG 代理问题

### 问题
SearXNG 在所有搜索引擎（Google、Brave、DuckDuckGo 等）上超时，因为它无法访问互联网。需要的修复是将它的流量通过本地 Mihomo 代理路由。

---

### 根本原因链

1. **SearXNG 在 Docker 中运行** — 它无法使用 `127.0.0.1` 访问主机
2. **错误的 host IP** — `host.docker.internal` 被硬编码为 `172.17.0.1`（默认 Docker bridge），但容器位于*自定义* Docker 网络（`172.20.0.0/16`），网关为 `172.20.0.1`
3. **UFW 阻塞** — 即使找到正确的 IP，UFW 的 `INPUT DROP` 策略仍会阻塞来自 Docker 子网到端口 7890 的 TCP 流量
4. **settings.yml 代理格式** — SearXNG 的 `outgoing.proxies` 需要是纯字符串，而不是 YAML 列表

---

### 修复步骤

1. 确认主机上代理正常工作：`curl --proxy http://127.0.0.1:7890 https://google.com` ✅
2. 检查容器环境变量 — `HTTP_PROXY` 设置为 `host.docker.internal:7890`，但解析到错误的 IP
3. 检查容器路由：`ip route` 显示网关为 `172.20.0.1`，而非 `172.17.0.1`
4. 从容器测试到 `172.20.0.1:7890` 的 TCP — 成功
5. 添加 iptables 规则允许 Docker 子网通过 UFW
6. 在 `settings.yml` 的 `outgoing:` 下设置 `proxies: http://172.20.0.1:7890`
7. 重启容器 → 返回 25 个结果

---

### 新安装指南

```bash
# 1. 创建目录
mkdir ~/searxng && cd ~/searxng

# 2. 创建 docker-compose.yml
cat > docker-compose.yml <<'EOF'
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "8888:8080"
    volumes:
      - ./searxng-data:/etc/searxng
    restart: unless-stopped
EOF

# 3. 启动一次以生成 settings.yml
docker compose up -d
sleep 5
docker compose down

# 4. 在 settings.yml 中设置代理
# 查找您的 Docker 网络网关：
docker network inspect bridge | grep Gateway
# 使用该 IP（默认通常为 172.17.0.1，或检查您的自定义网络）

# 编辑 searxng-data/settings.yml，在 outgoing 下：
#   proxies: http://<GATEWAY_IP>:7890

# 5. 允许 Docker 子网通过防火墙
sudo iptables -I INPUT -s 172.20.0.0/16 -p tcp --dport 7890 -j ACCEPT
# 使其持久化：
sudo apt install iptables-persistent && sudo netfilter-persistent save

# 6. 启动
docker compose up -d
```

---

### 关键经验教训

- 始终检查容器实际位于哪个 Docker 网络 — 自定义网络使用不同于默认 bridge 的子网
- UFW 会静默丢弃 Docker 到主机的流量；您需要为 Docker 子网添加明确的 INPUT 规则
- SearXNG 的代理配置放在 `settings.yml` 的 `outgoing.proxies` 下，作为纯字符串而非列表