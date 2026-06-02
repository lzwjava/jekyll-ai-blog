---
audio: false
generated: true
image: false
lang: en
layout: post
title: Uptime Kuma Introduction and Usage Guide
translated: false
type: note
---

**Question:** What is a comprehensive introduction to Uptime Kuma, and how do I use it?

**Answer:**

---

## Uptime Kuma — Comprehensive Introduction & Usage Guide

---

### What Is Uptime Kuma?

Uptime Kuma is a monitoring tool that allows anyone to monitor web services such as HTTP/HTTPS websites, apps, TCP ports, SSL certificates, and even MySQL databases. It is fully open-source, meaning the codebase and all files are free to download and use.

It was created as a self-hosted alternative to "Uptime Robot," built with a fancy UI, using Vue 3, Vite.js, Bootstrap 5, and WebSocket with SPA instead of a REST API.

The project has become extremely popular — with over 84,300 GitHub stars — and is actively maintained by Louis Lam and a large open-source community.

---

### Key Features

Uptime Kuma supports monitoring uptime for HTTP(s), TCP, HTTP(s) Keyword, HTTP(s) JSON Query, WebSocket, Ping, DNS Record, Push, Steam Game Server, and Docker Containers.

Other highlights include:

- **90+ notification channels**: Email (SMTP), Telegram, Signal, Slack, Discord, Splunk, SendGrid, Twilio, Pushover, and many more.
- **SSL/TLS certificate monitoring**: Check if URLs are reachable via HTTPS and detect upcoming certificate expirations.
- **Status pages**: Create multiple customizable status pages for specific services or domains to communicate health incidents and outages to users.
- **Interactive charts**: Ping monitoring data is visualized in interactive, fluid charts for every monitored host.
- **Short monitoring intervals**: Supports checks as frequent as every 20 seconds.

Uptime Kuma is compatible with multiple platforms including Linux, Windows 10 (x64), and Windows Server.

---

### Installation

#### Method 1 — Docker (Recommended)

Run the following command in your terminal:

```bash
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:2
```

Here is what each flag does:

- `--restart=always` — ensures the container restarts automatically if it crashes or when Docker restarts.
- `-p 3001:3001` — maps port 3001 of your host to port 3001 inside the container.
- `-v uptime-kuma:/app/data` — mounts a volume to the `/app/data` directory, ensuring data persistence.
- `--name uptime-kuma` — assigns a recognizable name to the container.

Once running, access Uptime Kuma at **<http://localhost:3001>**.

#### Method 2 — Docker Compose

```bash
mkdir uptime-kuma
cd uptime-kuma
curl -o compose.yaml https://raw.githubusercontent.com/louislam/uptime-kuma/master/compose.yaml
docker compose up -d
```

#### Method 3 — Node.js (Without Docker)

Clone the repo and run manually using Node.js or PM2:

```bash
git clone https://github.com/louislam/uptime-kuma.git
cd uptime-kuma
npm run setup
# Start with PM2 (recommended for background process):
npm install pm2 -g && pm2 install pm2-logrotate
pm2 start server/server.js --name uptime-kuma
pm2 startup && pm2 save
```

> **Note:** File systems like NFS (Network File System) are NOT supported. Please map to a local directory or volume.

---

### First Setup — Creating an Admin Account

After opening **<http://localhost:3001>**, you will be prompted to create an admin account. After creating the account, you will be redirected to the dashboard, which displays the status of monitored services and offers insights into uptime, downtime, and maintenance.

---

### Adding a Monitor

1. Click **"Add New Monitor"** on the dashboard.
2. Choose a **Monitor Type** (e.g., HTTP(s), TCP, Ping, DNS, Docker Container, etc.).
3. Enter the **URL or hostname** to monitor.
4. Set the **Heartbeat Interval** — the default is 60 seconds, meaning Uptime Kuma will check availability every minute.
5. Click **Save**.

The monitor will immediately begin checking and display real-time status including uptime percentage and response time history.

---

### Monitor Types Explained

| Type | Use Case |
|---|---|
| **HTTP(s)** | Monitor websites and web apps |
| **TCP Port** | Monitor open ports on servers |
| **Ping** | Check if a host is reachable |
| **DNS Record** | Monitor DNS resolution |
| **HTTP(s) Keyword** | Check if a keyword appears in a page response |
| **HTTP(s) JSON Query** | Monitor specific JSON values in API responses |
| **Docker Container** | Monitor if a container is running |
| **Steam Game Server** | Monitor game server availability |
| **Push** | Heartbeat-style monitoring (your app pings Kuma) |
| **MySQL / MariaDB** | Dedicated MySQL/MariaDB monitor with conditions support |

---

### Setting Up Notifications

1. Go to **Settings → Notifications**.
2. Click **"Add Notification"**.
3. Choose a notification type (e.g., Email/SMTP, Telegram, Slack, Discord, Microsoft Teams, Webhook, etc.).
4. Fill in the required credentials (e.g., SMTP host, bot token, webhook URL).
5. Click **"Test"** to verify it works, then save.
6. When adding or editing a monitor, **attach** the notification to it.

You can simulate downtime (e.g., disable a VM's network) to test that alerts fire correctly.

---

### Creating Status Pages

Status pages allow you to share the health of your services publicly or with your team.

1. Go to **"Status Page"** in the left sidebar.
2. Click **"New Status Page"** and give it a name and slug (e.g., `status.yourdomain.com`).
3. Add monitors to the page.
4. Customize the look (logo, title, color theme).
5. Publish it — share the URL with users or embed it.

Status pages allow you to set communications between you and your customers in the event of a health issue, current incidents, outages, and any real-time updates you can provide.

---

### Maintenance Windows

Go to **Dashboard → "Maintenance"** in the left sidebar and click **"Add"**. You can set a title, date range, timezone, strategy (manual or scheduled), and select affected monitors. When active, alerts are paused and monitors are marked as "Under Maintenance" on the status page.

---

### Reverse Proxy (Optional but Recommended)

For production use, it is common to put Uptime Kuma behind **Nginx** or **Caddy** as a reverse proxy with HTTPS/SSL. Nginx can be used as a reverse proxy with a wildcard SSL certificate for secure internal access.

Basic Nginx config:

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

> WebSocket support (`Upgrade` headers) is **required** for Uptime Kuma to work correctly behind a proxy.

---

### API Keys

You can create an API key by logging in to your Uptime Kuma instance, navigating to **Settings → API Keys**, and selecting **Add API Key**. This allows integration with external tools such as Home Assistant, automation systems, and more.

---

### Limitations to Be Aware Of

- Uptime Kuma is **single-server** — it checks from only one location. If you need multi-region monitoring to reduce false positives, you would need a separate solution or multiple instances.
- It is a **self-hosted** tool — you are responsible for keeping the server running and updated.
- There is no built-in **on-call scheduling** or **incident escalation** (those features exist in commercial tools).

---

### Summary

Uptime Kuma is an excellent, free, self-hosted monitoring solution ideal for:

- **Homelab** and personal infrastructure monitoring
- **Small-to-medium** production environments
- **DevOps/SysAdmin** setups that need a simple yet powerful status dashboard
- Anyone wanting to replace paid services like Uptime Robot with a self-hosted alternative

---

**References:**

- [Uptime Kuma GitHub Repository](https://github.com/louislam/uptime-kuma)
- [Complete Guide to Monitoring With Uptime Kuma — Better Stack](https://betterstack.com/community/guides/monitoring/uptime-kuma-guide/)
- [Uptime Kuma Official Site](https://uptimekuma.org/)
- [Uptime Kuma Installation & Monitoring Guide — Echoesofping](https://echoesofping.hashnode.dev/comprehensive-guide-to-installing-and-using-uptime-kuma-for-uptime-monitoring)
- [Uptime Kuma IT Infrastructure Guide — BuildingTheITGuy](https://www.buildingtheitguy.com/index.php/uptime-kuma-monitoring-ssl-ms-teams/it-infrastructure/)
- [Uptime Kuma Wiki](https://github.com/louislam/uptime-kuma/wiki/)
