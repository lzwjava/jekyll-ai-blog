---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing Docker GHCR TLS Timeout Error
translated: false
type: note
---

The error you're encountering, `Get "https://ghcr.io/v2/": net/http: TLS handshake timeout`, typically indicates a network issue when Docker tries to pull images from GitHub Container Registry (GHCR). Here are some steps to troubleshoot and fix the issue:

---

### 1. **Check Your Internet Connection**
- Ensure your machine has a stable internet connection.
- Try accessing `https://ghcr.io` in your browser to confirm you can reach the site.

---

### 2. **Check Docker Daemon Status**
- Restart the Docker daemon:
  ```bash
  sudo systemctl restart docker
  ```
- Verify Docker is running:
  ```bash
  sudo systemctl status docker
  ```

---

### 3. **Configure Docker DNS**
- If you're behind a corporate network or proxy, Docker might need custom DNS settings.
- Edit or create `/etc/docker/daemon.json`:
  ```json
  {
    "dns": ["8.8.8.8", "1.1.1.1"]
  }
  ```
- Restart Docker:
  ```bash
  sudo systemctl restart docker
  ```

---

### 4. **Check for Proxy Settings**
- If you're behind a proxy, configure Docker to use it:
  ```bash
  mkdir -p ~/.docker
  echo '{
    "proxies": {
      "default": {
        "httpProxy": "http://your-proxy-address:port",
        "httpsProxy": "http://your-proxy-address:port",
        "noProxy": "localhost,127.0.0.1"
      }
    }
  }' > ~/.docker/config.json
  ```
- Replace `your-proxy-address:port` with your actual proxy details.

---

### 5. **Retry Pulling the Image Manually**
- Try pulling the image manually to see if the issue persists:
  ```bash
  docker pull ghcr.io/librechat/librechat:latest
  ```
- If it works, retry `docker-compose up -d`.

---

### 6. **Check for Firewall/Network Restrictions**
- Ensure your firewall or network isn't blocking access to `ghcr.io`.
- Temporarily disable the firewall to test:
  ```bash
  sudo ufw disable
  ```
  (Re-enable it after testing if needed.)

---

### 7. **Update Docker and Docker-Compose**
- Ensure you're using the latest versions:
  ```bash
  sudo apt update && sudo apt upgrade docker-ce docker-compose-plugin
  ```

---

### 8. **Set UID/GID Environment Variables**
- The warnings about `UID` and `GID` are not critical, but you can set them in your `.env` file or `docker-compose.yml` to suppress the warnings:
  ```bash
  echo "UID=$(id -u)" >> .env
  echo "GID=$(id -g)" >> .env
  ```

---

### 9. **Use a Different Registry Mirror (Optional)**
- If GHCR is consistently unreachable, you can try using a mirror (though this is not recommended for production):
  ```json
  {
    "registry-mirrors": ["https://mirror.example.com"]
  }
  ```
  Add this to `/etc/docker/daemon.json` and restart Docker.

---

### 10. **Check for Time Synchronization**
- Ensure your system time is synchronized:
  ```bash
  sudo apt install ntp
  sudo systemctl restart ntp
  ```

---

### Summary Table of Commands



| Step | Command/Action |
|------|----------------|
| Restart Docker | `sudo systemctl restart docker` |
| Check Docker Status | `sudo systemctl status docker` |
| Configure DNS | Edit `/etc/docker/daemon.json` |
| Pull Image Manually | `docker pull ghcr.io/librechat/librechat:latest` |
| Set UID/GID | `echo "UID=$(id -u)" >> .env` |

---

If the issue persists after trying these steps, let me know the output of:
```bash
docker info
```
and any error messages you see when running the above commands. This will help diagnose further!
