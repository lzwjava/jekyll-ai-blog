---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing SearXNG Docker Proxy Timeout Issue
translated: false
type: note
---

## How I Solved the SearXNG Proxy Issue

### The Problem
SearXNG was timing out on all search engines (Google, Brave, DuckDuckGo, etc.) because it couldn't reach the internet. The fix needed was routing its traffic through the local Mihomo proxy.

---

### Root Cause Chain

1. **SearXNG runs in Docker** — it can't use `127.0.0.1` to reach the host
2. **Wrong host IP** — `host.docker.internal` was hardcoded to `172.17.0.1` (default Docker bridge), but the container was on a *custom* Docker network (`172.20.0.0/16`) with gateway `172.20.0.1`
3. **UFW blocking** — even after finding the right IP, UFW's `INPUT DROP` policy was blocking TCP from the Docker subnet to port 7890
4. **settings.yml proxy format** — SearXNG's `outgoing.proxies` needed to be a plain string, not a YAML list

---

### Steps to Fix

1. Confirmed proxy works from host: `curl --proxy http://127.0.0.1:7890 https://google.com` ✅
2. Checked container env vars — `HTTP_PROXY` was set to `host.docker.internal:7890` but that resolved to the wrong IP
3. Inspected container routing: `ip route` revealed gateway is `172.20.0.1`, not `172.17.0.1`
4. Tested TCP from container to `172.20.0.1:7890` — succeeded
5. Added iptables rule to allow Docker subnet through UFW
6. Set `proxies: http://172.20.0.1:7890` in `settings.yml` under `outgoing:`
7. Restarted container → 25 results returned

---

### Fresh Install Guide

```bash
# 1. Create directory
mkdir ~/searxng && cd ~/searxng

# 2. Create docker-compose.yml
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

# 3. Start once to generate settings.yml
docker compose up -d
sleep 5
docker compose down

# 4. Set proxy in settings.yml
# Find your Docker network gateway:
docker network inspect bridge | grep Gateway
# Use that IP (usually 172.17.0.1 for default, or check your custom network)

# Edit searxng-data/settings.yml, under outgoing:
#   proxies: http://<GATEWAY_IP>:7890

# 5. Allow Docker subnet through firewall
sudo iptables -I INPUT -s 172.20.0.0/16 -p tcp --dport 7890 -j ACCEPT
# Make persistent:
sudo apt install iptables-persistent && sudo netfilter-persistent save

# 6. Start
docker compose up -d
```

---

### Key Lessons

- Always check which Docker network your container is actually on — custom networks use different subnets than the default bridge
- UFW silently drops Docker-to-host traffic; you need an explicit INPUT rule for the Docker subnet
- SearXNG's proxy config goes in `settings.yml` under `outgoing.proxies` as a plain string, not a list
