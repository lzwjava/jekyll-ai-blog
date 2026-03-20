---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Uptime Kuma 介绍与使用指南
translated: true
type: note
---

**问题：** Uptime Kuma 的全面介绍是什么，以及如何使用它？

**答案：**

---

## Uptime Kuma — 全面介绍与使用指南

---

### 什么是 Uptime Kuma？

Uptime Kuma 是一个监控工具，允许任何人监控 web 服务，例如 HTTP/HTTPS 网站、应用、TCP 端口、SSL 证书，甚至 MySQL 数据库。它是完全开源的，意味着代码库和所有文件都可以免费下载和使用。

它被创建为 “Uptime Robot” 的自托管替代品，使用精美的 UI 构建，采用 Vue 3、Vite.js、Bootstrap 5 和 WebSocket，并使用 SPA 而非 REST API。

该项目已成为极受欢迎的项目——拥有超过 84,300 个 GitHub stars——由 Louis Lam 和庞大的开源社区积极维护。

---

### 主要特性

Uptime Kuma 支持监控 HTTP(s)、TCP、HTTP(s) Keyword、HTTP(s) JSON Query、WebSocket、Ping、DNS Record、Push、Steam Game Server 和 Docker Containers 的正常运行时间。

其他亮点包括：

- **90+ 种通知渠道**：Email (SMTP)、Telegram、Signal、Slack、Discord、Splunk、SendGrid、Twilio、Pushover 等众多渠道。
- **SSL/TLS 证书监控**：检查 URL 是否可以通过 HTTPS 访问，并检测即将到期的证书。
- **状态页面**：为特定服务或域名创建多个可自定义的状态页面，向用户传达健康事件和中断情况。
- **交互式图表**：每个监控主机的 Ping 监控数据以交互式、流畅的图表形式可视化。
- **短监控间隔**：支持最短 20 秒的检查间隔。

Uptime Kuma 兼容多种平台，包括 Linux、Windows 10 (x64) 和 Windows Server。

---

### 安装

#### 方法 1 — Docker（推荐）

在终端运行以下命令：

```bash
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:2
```

以下是每个标志的作用：

- `--restart=always` — 确保容器在崩溃或 Docker 重启时自动重启。
- `-p 3001:3001` — 将主机的 3001 端口映射到容器内的 3001 端口。
- `-v uptime-kuma:/app/data` — 将卷挂载到 `/app/data` 目录，确保数据持久化。
- `--name uptime-kuma` — 为容器分配一个易识别的名称。

运行后，通过 **http://localhost:3001** 访问 Uptime Kuma。

#### 方法 2 — Docker Compose

```bash
mkdir uptime-kuma
cd uptime-kuma
curl -o compose.yaml https://raw.githubusercontent.com/louislam/uptime-kuma/master/compose.yaml
docker compose up -d
```

#### 方法 3 — Node.js（无需 Docker）

克隆仓库并使用 Node.js 或 PM2 手动运行：

```bash
git clone https://github.com/louislam/uptime-kuma.git
cd uptime-kuma
npm run setup
# 使用 PM2 启动（推荐用于后台进程）：
npm install pm2 -g && pm2 install pm2-logrotate
pm2 start server/server.js --name uptime-kuma
pm2 startup && pm2 save
```

> **注意：** 不支持 NFS（Network File System）等文件系统。请映射到本地目录或卷。

---

### 首次设置 — 创建管理员账户

打开 **http://localhost:3001** 后，您将被提示创建管理员账户。创建账户后，将被重定向到仪表板，该仪表板显示监控服务的状态，并提供正常运行时间、中断时间和维护的洞察。

---

### 添加监控项

1. 在仪表板上点击 **“Add New Monitor”**。
2. 选择 **Monitor Type**（例如 HTTP(s)、TCP、Ping、DNS、Docker Container 等）。
3. 输入要监控的 **URL 或主机名**。
4. 设置 **Heartbeat Interval** — 默认值为 60 秒，表示 Uptime Kuma 将每分钟检查一次可用性。
5. 点击 **Save**。

监控项将立即开始检查，并显示实时状态，包括正常运行时间百分比和响应时间历史。

---

### 监控类型说明

 

| Type | Use Case |
|---|---|
| **HTTP(s)** | 监控网站和 web 应用 |
| **TCP Port** | 监控服务器上的开放端口 |
| **Ping** | 检查主机是否可达 |
| **DNS Record** | 监控 DNS 解析 |
| **HTTP(s) Keyword** | 检查页面响应中是否出现关键字 |
| **HTTP(s) JSON Query** | 监控 API 响应中的特定 JSON 值 |
| **Docker Container** | 监控容器是否正在运行 |
| **Steam Game Server** | 监控游戏服务器可用性 |
| **Push** | 心跳式监控（您的应用 ping Kuma） |
| **MySQL / MariaDB** | 支持条件的专用 MySQL/MariaDB 监控 |

---

### 设置通知

1. 转到 **Settings → Notifications**。
2. 点击 **“Add Notification”**。
3. 选择通知类型（例如 Email/SMTP、Telegram、Slack、Discord、Microsoft Teams、Webhook 等）。
4. 填写所需凭据（例如 SMTP 主机、bot token、webhook URL）。
5. 点击 **“Test”** 验证其工作正常，然后保存。
6. 在添加或编辑监控项时，将通知**附加**到它。

您可以模拟中断（例如禁用 VM 的网络）来测试警报是否正确触发。

---

### 创建状态页面

状态页面允许您公开或与团队分享服务的健康状况。

1. 在左侧边栏转到 **“Status Page”**。
2. 点击 **“New Status Page”** 并为其命名并设置 slug（例如 `status.yourdomain.com`）。
3. 将监控项添加到页面。
4. 自定义外观（徽标、标题、颜色主题）。
5. 发布它 — 与用户分享 URL 或嵌入它。

状态页面允许您在健康问题、当前事件、中断以及您能提供的任何实时更新时，与客户进行沟通。

---

### 维护窗口

在左侧边栏转到 **Dashboard → “Maintenance”** 并点击 **“Add”**。您可以设置标题、日期范围、时区、策略（手动或计划），并选择受影响的监控项。激活时，警报将暂停，监控项在状态页面上标记为“Under Maintenance”。

---

### 反向代理（可选，但推荐）

对于生产使用，通常将 Uptime Kuma 置于 **Nginx** 或 **Caddy** 后面作为反向代理，并启用 HTTPS/SSL。Nginx 可以用通配符 SSL 证书作为反向代理，用于安全的内部访问。

基本的 Nginx 配置：

```nginx
server {
    listen 443 ssl;
    server_name status.yourdomain.com;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

> WebSocket 支持（`Upgrade` 标头）是 Uptime Kuma 在代理后面正常工作的**必需**条件。

---

### API 密钥

您可以通过登录 Uptime Kuma 实例，转到 **Settings → API Keys** 并选择 **Add API Key** 来创建 API 密钥。这允许与外部工具（如 Home Assistant、自动化系统等）集成。

---

### 需要注意的限制

- Uptime Kuma 是**单服务器**的——它仅从一个位置进行检查。如果需要多区域监控以减少误报，则需要单独的解决方案或多个实例。
- 它是**自托管**工具——您负责保持服务器运行和更新。
- 没有内置的**值班调度**或**事件升级**（这些功能存在于商业工具中）。

---

### 总结

Uptime Kuma 是一个优秀的、免费的自托管监控解决方案，非常适合：

- **Homelab** 和个人基础设施监控
- **中小型**生产环境
- 需要简单却强大的状态仪表板的 **DevOps/SysAdmin** 设置
- 任何想用自托管替代品替换 Uptime Robot 等付费服务的人

---

**参考资料：**

- [Uptime Kuma GitHub Repository](https://github.com/louislam/uptime-kuma)
- [Complete Guide to Monitoring With Uptime Kuma — Better Stack](https://betterstack.com/community/guides/monitoring/uptime-kuma-guide/)
- [Uptime Kuma Official Site](https://uptimekuma.org/)
- [Uptime Kuma Installation & Monitoring Guide — Echoesofping](https://echoesofping.hashnode.dev/comprehensive-guide-to-installing-and-using-uptime-kuma-for-uptime-monitoring)
- [Uptime Kuma IT Infrastructure Guide — BuildingTheITGuy](https://www.buildingtheitguy.com/index.php/uptime-kuma-monitoring-ssl-ms-teams/it-infrastructure/)
- [Uptime Kuma Wiki](https://github.com/louislam/uptime-kuma/wiki/)