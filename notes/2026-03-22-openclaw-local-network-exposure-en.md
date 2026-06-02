---
audio: false
generated: true
image: false
lang: en
layout: post
title: Exposing OpenClaw to Local Network interfaces
translated: false
type: note
---

Question: How can I access the OpenClaw AI agent running on 192.168.1.36:18789 directly without using SSH tunneling?

Answer:Answer:

## Root Cause

The problem is that OpenClaw is **bound to `127.0.0.1:18789`** on the remote server — meaning it only listens on localhost, not the network interface. That's why you need the SSH tunnel in the first place.

The cleanest fix is to **make OpenClaw listen on `0.0.0.0:18789`** instead of `127.0.0.1:18789`.

---

## Solution 1: Change OpenClaw's Bind Address (Best Solution)

On the remote server `192.168.1.36`, find how OpenClaw is started and change the bind host.

Typically in a config file or startup command:

```bash
# Before (localhost only)
host = "127.0.0.1"
port = 18789

# After (all interfaces, accessible via LAN IP)
host = "0.0.0.0"
port = 18789
```

Or if it's started via command line argument:
```bash
# Change from
openclaw --host 127.0.0.1 --port 18789

# To
openclaw --host 0.0.0.0 --port 18789
```

After this, you can access it directly at `http://192.168.1.36:18789` from any machine on the same LAN.

---

## Solution 2: Use a Reverse Proxy (nginx) on the Remote Server

If you cannot change OpenClaw's config, set up nginx on `192.168.1.36` to proxy the port:

```bash
sudo apt install nginx
```

Create a config file `/etc/nginx/sites-available/openclaw`:
```nginx
server {
    listen 18790;              # external port (or use 18789 if you change openclaw's port)
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/openclaw /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Then access via `http://192.168.1.36:18790`.

---

## Solution 3: Use `socat` to Expose the Port Directly

A quick one-liner on `192.168.1.36`:

```bash
socat TCP-LISTEN:18790,fork,reuseaddr TCP:127.0.0.1:18789
```

This forwards all connections on port `18790` (accessible by LAN IP) to the local `18789`. Access it at `http://192.168.1.36:18790`.

To keep it running persistently, wrap it in a systemd service or use `nohup`:
```bash
nohup socat TCP-LISTEN:18790,fork,reuseaddr TCP:127.0.0.1:18789 &
```

---

## Summary

| Solution | Effort | Notes |
|---|---|---|
| Change OpenClaw bind address | Low | Best and cleanest |
| nginx reverse proxy | Medium | Good for production |
| socat | Low | Quick temporary fix |

**Solution 1 is recommended** — changing the bind address to `0.0.0.0` is the most direct approach. Just make sure your firewall on the remote server allows port `18789` through: `sudo ufw allow 18789`.

References:

- [SSH Tunneling Explained - Linuxize](https://linuxize.com/post/how-to-setup-ssh-tunneling/)
- [A Visual Guide to SSH Tunnels - iximiuz](https://iximiuz.com/en/posts/ssh-tunnels/)
