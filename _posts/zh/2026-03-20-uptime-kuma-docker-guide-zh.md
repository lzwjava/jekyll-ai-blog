---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Uptime Kuma Docker 安装指南
translated: true
type: note
---

## **1. 先决条件检查**
- **Docker & Docker Compose**：容器化部署所需
- **Port 3001**：必须可用（可能需要调整防火墙规则）
- **User Permissions**：当前用户应加入 `docker` 组，以无需 `sudo` 运行容器

## **2. 目录结构**
```
~/uptime-kuma/
├── docker-compose.yml          # Service definition
└── uptime-kuma-data/          # Persistent volume (created automatically)
```

## **3. Docker Compose 配置**
```yaml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1      # Official image (latest stable)
    container_name: uptime-kuma         # Fixed name for easier management
    restart: unless-stopped             # Auto-restart on failures, manual stops excluded
    volumes:
      - ./uptime-kuma-data:/app/data   # Persists configuration, database, and SSL certs
    ports:
      - "3001:3001"                     # Host:Container port mapping
    environment:
      - PUID=1000                       # User ID (matches host user)
      - PGID=1000                       # Group ID
      - TZ=Asia/Hong_Kong               # Timezone for logs and schedules
```

### **关键决策说明：**
- **Volume Mapping**：`./uptime-kuma-data:/app/data` 确保数据在容器重建后仍存活
- **Restart Policy**：`unless-stopped` 平衡自动化与手动控制
- **Port 3001**：Uptime Kuma 标准端口；冲突时可更改
- **Timezone**：对准确的正常运行时间计算和警报时机至关重要

## **4. 部署过程**
```bash
# Create directory and navigate
mkdir -p ~/uptime-kuma && cd ~/uptime-kuma

# Write docker-compose.yml (as above)
cat > docker-compose 'EOF' ...

# Pull image and start container in detached mode
docker-compose up -d

# Verify container status
docker-compose ps
docker-compose logs -f uptime-kuma  # Monitor startup logs
```

## **5. 安装后验证**
- **Container Status**：30 秒内应显示 `Up (healthy)`
- **Web Interface**：`http://localhost:3001` 重定向至 `/dashboard`
- **Health Check**：`curl -s http://localhost:3001/api/status` 返回 JSON
- **Logs**：`docker-compose logs` 中无错误消息

## **6. 初始设置（首次访问）**
1. 导航至 `http://server-ip>:3001`
2. **创建管理员账户**：
   - Username（推荐：admin 或自定义）
   - 强密码
   - Email（可选，用于警报）
3. **Dashboard 配置**：
   - 添加监控目标（网站、API、服务器）
   - 配置通知渠道（Telegram、Discord、email 等）
   - 设置检查间隔和超时时间

## **7. 持久化数据管理**
- **Location**：`~/uptime-kuma/uptime-kuma-data/`
- **Contents**：
  - SQLite 数据库（`kuma.db`）
  - SSL 证书（如果配置）
  - 配置文件
  - 上传的图像/徽标
- **Backup Strategy**：定期备份此目录

## **8. 维护命令**
```bash
# Stop service
cd ~/uptime-kuma && docker-compose down

# Start service
docker-compose up -d

# View logs
docker-compose logs -f uptime-kuma

# Update to latest version
docker-compose pull && docker-compose up -d

# Remove completely (WARNING: deletes data unless volume preserved)
docker-compose down -v
```

## **9. 安全考虑**
- **Firewall**：如果公网暴露，限制端口 3001 仅限受信任 IP
- **Reverse Proxy**：推荐用于 SSL/TLS（nginx、Caddy、Traefik）
- **Authentication**：Uptime Kuma 内置用户管理
- **Database**：SQLite（本地文件）；确保卷权限（推荐 600）

## **10. 集成选项**
- **Notifications**：支持 20+ 服务（Telegram、Discord、Slack、email、webhooks）
- **API**：REST API 可用，位于 `/api/*` 端点
- **Metrics**：Prometheus 导出位于 `/metrics`
- **Heartbeat**：支持 cron 作业的心跳监控

## **11. 故障排除**

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| Port 3001 unreachable | Firewall blocking | `ufw allow 3001/tcp` |
| Container exits immediately | Volume permission issues | `chown -R 1000:1000 uptime-kuma-data` |
| Dashboard shows "Disconnected" | Browser cache or WebSocket issue | Clear cache or check reverse proxy config |

## **12. 下一步**
1. **设置监控目标**（从关键服务开始）
2. **配置警报**（使用 Telegram/Discord 测试）
3. **考虑反向代理**以实现 HTTPS 访问
4. **`uptime-kuma-data` 目录的定期备份**
5. **监控资源使用情况**（`docker stats uptime-kuma`）

---

**当前状态**：✅ 在 `httpserver-ip>:3001` 运行，数据持久化，自动重启已启用。准备好初始配置。