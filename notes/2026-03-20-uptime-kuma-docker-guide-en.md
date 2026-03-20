---
audio: false
generated: true
image: false
lang: en
layout: post
title: Uptime Kuma Docker Installation Guide
translated: false
type: note
---

## **1. Prerequisites Check**
- **Docker & Docker Compose**: Required for containerized deployment
- **Port 3001**: Must be available (firewall rules may need adjustment)
- **User Permissions**: Current user should be in `docker` group to run containers without `sudo`

## **2. Directory Structure**
```
~/uptime-kuma/
├── docker-compose.yml          # Service definition
└── uptime-kuma-data/          # Persistent volume (created automatically)
```

## **3. Docker Compose Configuration**
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

### **Key Decisions Explained:**
- **Volume Mapping**: `./uptime-kuma-data:/app/data` ensures data survives container recreation
- **Restart Policy**: `unless-stopped` balances automation with manual control
- **Port 3001**: Standard Uptime Kuma port; can be changed if conflicted
- **Timezone**: Critical for accurate uptime calculations and alert timing

## **4. Deployment Process**
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

## **5. Post-Install Verification**
- **Container Status**: Should show `Up (healthy)` within 30 seconds
- **Web Interface**: `http://localhost:3001` redirects to `/dashboard`
- **Health Check**: `curl -s http://localhost:3001/api/status` returns JSON
- **Logs**: No error messages in `docker-compose logs`

## **6. Initial Setup (First Access)**
1. Navigate to `http://server-ip>:3001`
2. **Create Admin Account**:
   - Username (recommend: admin or custom)
   - Strong password
   - Email (optional, for alerts)
3. **Dashboard Configuration**:
   - Add monitoring targets (websites, APIs, servers)
   - Configure notification channels (Telegram, Discord, email, etc.)
   - Set check intervals and timeouts

## **7. Persistent Data Management**
- **Location**: `~/uptime-kuma/uptime-kuma-data/`
- **Contents**:
  - SQLite database (`kuma.db`)
  - SSL certificates (if configured)
  - Configuration files
  - Uploaded images/logos
- **Backup Strategy**: Backup this directory regularly

## **8. Maintenance Commands**
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

## **9. Security Considerations**
- **Firewall**: Restrict port 3001 to trusted IPs if exposed publicly
- **Reverse Proxy**: Recommended for SSL/TLS (nginx, Caddy, Traefik)
- **Authentication**: Uptime Kuma has built‑in user management
- **Database**: SQLite (local file); ensure volume permissions (600 recommended)

## **10. Integration Options**
- **Notifications**: 20+ supported services (Telegram, Discord, Slack, email, webhooks)
- **API**: REST API available at `/api/*` endpoints
- **Metrics**: Prometheus export at `/metrics`
- **Heartbeat**: Supports heartbeat monitoring for cron jobs

## **11. Troubleshooting**

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| Port 3001 unreachable | Firewall blocking | `ufw allow 3001/tcp` |
| Container exits immediately | Volume permission issues | `chown -R 1000:1000 uptime-kuma-data` |
| Dashboard shows "Disconnected" | Browser cache or WebSocket issue | Clear cache or check reverse proxy config |

## **12. Next Steps**
1. **Set up monitoring targets** (start with critical services)
2. **Configure alerts** (test with Telegram/Discord)
3. **Consider reverse proxy** for HTTPS access
4. **Regular backups** of `uptime-kuma-data` directory
5. **Monitor resource usage** (`docker stats uptime-kuma`)

---

**Current Status**: ✅ Running at `httpserver-ip>:3001`, data persisted, auto‑restart enabled. Ready for initial configuration.