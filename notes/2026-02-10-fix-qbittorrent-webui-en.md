---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Blank qBittorrent WebUI Access
translated: false
type: note
---

Question: The web UI shows nothing when accessing http://192.168.1.36:8080

Answer:

If **nothing shows** at `http://192.168.1.36:8080` (blank page, timeout, connection refused, or infinite loading), follow these troubleshooting steps in order on your Ubuntu server. Most "nothing shows" cases are caused by one of these: service not running, wrong bind address, firewall, wrong port, config issue, or browser/network problem.

### 1. Check if the service is actually running
```bash
sudo systemctl status qbittorrent-nox
```
- Look for **Active: active (running)**.
- If failed / inactive / dead → see step 7.
- Also check recent logs:
```bash
sudo journalctl -u qbittorrent-nox -n 50 --no-pager
```
Look for lines like:
- `WebUI: Now listening on IP: *, port: 8080` → good
- `WebUI: Now listening on IP: 127.0.0.1` or `localhost` → bad (only local access)
- Any errors about binding, permissions, or crashes.

### 2. Test locally on the server itself
Run this directly on the Ubuntu server (via SSH or console):
```bash
curl http://localhost:8080
```
or
```bash
curl http://127.0.0.1:8080
```
- If you get **HTML code** (starts with `<!DOCTYPE html>` or login page source) → service is running, problem is network/firewall/browser side.
- If `curl: (7) Failed to connect to localhost port 8080: Connection refused` → service not listening or bound only to wrong interface.
- If `curl: (52) Empty reply from server` or timeout → service running but WebUI broken/crashed.

### 3. Check what is actually listening on port 8080
```bash
sudo ss -tuln | grep 8080
# or
sudo netstat -tuln | grep 8080   # if netstat is installed
```
- Expected good output: `tcp LISTEN 0 128 *:8080 *:*` or `0.0.0.0:8080` (listening on all interfaces).
- If `127.0.0.1:8080` or nothing → WebUI is only bound to localhost.

**Fix if bound to localhost only**
Edit config (stop service first):
```bash
sudo systemctl stop qbittorrent-nox
```
Then edit (as the qbittorrent user or with sudo):
```bash
nano /var/lib/qbittorrent/.config/qBittorrent/qBittorrent.conf
# or wherever your config is (check with find / -name qBittorrent.conf)
```
Find or add these lines under `[Preferences]`:
```
WebUI\Address=0.0.0.0
WebUI\Port=8080
WebUI\Enabled=true
```
(0.0.0.0 means listen on all interfaces)

Restart:
```bash
sudo systemctl start qbittorrent-nox
```

Alternative: run manually with explicit bind:
```bash
sudo -u qbittorrent qbittorrent-nox --webui-port=8080 --webui-address=0.0.0.0
```

### 4. Check Ubuntu firewall (ufw)
```bash
sudo ufw status
```
If active, allow the port:
```bash
sudo ufw allow 8080/tcp
sudo ufw reload
```

### 5. Browser / network checks (from your other computer)
- Try http://192.168.1.36:8080 in **incognito/private mode** (cache/extensions can break it).
- Try a different browser.
- Ping the server: `ping 192.168.1.36` (must reply).
- Test port reachability: from your PC run `telnet 192.168.1.36 8080` or use online port checker.
- If you get connection refused → firewall/router issue or wrong IP.
- Make sure you're on the same local network (192.168.1.x).

### 6. Reset WebUI password / config (if login page appears but won't accept admin/adminadmin)
Stop service → delete or rename config:
```bash
sudo systemctl stop qbittorrent-nox
sudo mv /var/lib/qbittorrent/.config/qBittorrent/qBittorrent.conf /var/lib/qbittorrent/.config/qBittorrent/qBittorrent.conf.bak
sudo systemctl start qbittorrent-nox
```
Run once manually to see temp password in terminal:
```bash
sudo -u qbittorrent qbittorrent-nox
```

### 7. If service fails to start
- Check journalctl output for errors (permissions on /var/lib/qbittorrent, missing libs, etc.).
- Common fix: ensure folder ownership
```bash
sudo chown -R qbittorrent:qbittorrent /var/lib/qbittorrent
```
- Reinstall if corrupted:
```bash
sudo apt reinstall qbittorrent-nox
```

### Quick one-liner summary to diagnose
```bash
sudo systemctl status qbittorrent-nox && sudo ss -tuln | grep 8080 && curl -I http://localhost:8080
```

Run that and share the output if still stuck — it tells us almost everything.

References:

- [qBittorrent GitHub issues on WebUI problems](https://github.com/qbittorrent/qBittorrent/issues)
- [Running qBittorrent-nox systemd setup](https://github.com/qbittorrent/qBittorrent/wiki/Running-qBittorrent-without-X-server-(WebUI-only,-systemd-service-set-up,-Ubuntu-15.04-or-newer))
- [Common qBittorrent-nox troubleshooting threads](https://www.reddit.com/r/qBittorrent)
