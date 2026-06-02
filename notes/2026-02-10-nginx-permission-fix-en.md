---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Nginx Permission Denied Fix Guide
translated: false
type: note
---

**Question:** Nginx is failing to start with these new errors: could not open error log file (Permission denied), "user" directive ignored, and bind() to 0.0.0.0:80 failed (Permission denied). How do I fix this?

**Answer:**

These errors show that nginx is **not running as root** at startup. The master process must start as root (or with enough privileges) to:

- Bind to TCP port 80 (ports below 1024 are privileged)
- Open/write to log files in `/var/log/nginx/` (usually owned by root or www-data)

Right now your nginx is being started as a normal user (most likely `lzw`), which causes both the bind() and log file errors.

### Root cause summary

You previously set nginx to run as user `lzw` (via `systemctl edit` or `user` directive), but:

- Normal users cannot bind port 80
- Normal users cannot write to `/var/log/nginx/`
- The `user` directive is ignored unless the master process starts as root

→ nginx fails immediately during startup.

### Correct & Recommended Fix (undo non-root user)

1. **Remove the override that sets User=lzw**

   ```bash
   sudo rm -f /etc/systemd/system/nginx.service.d/override.conf
   sudo systemctl daemon-reload
   ```

   This removes any custom `User=` and `Group=` settings you added.

2. **(Optional but recommended) Make sure no `user` line exists in nginx.conf**

   Open the config:

   ```bash
   sudo nano /etc/nginx/nginx.conf
   ```

   Look for and **comment out or delete** any line like:

   ```nginx
   user lzw lzw;
   # or
   user lzw;
   ```

   Save the file.

3. **Test configuration and restart nginx**

   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   sudo systemctl status nginx
   ```

   You should now see:

   - Active: active (running)
   - No permission denied errors on port 80 or logs
   - Worker processes running as `www-data` (or whatever group is default)

4. **Fix the original folder access (so /movies/ stops giving 403)**

   ```bash
   # Give nginx group access to your downloads folder
   sudo chgrp -R www-data /home/lzw/qDownloads
   sudo chmod -R g+rx /home/lzw/qDownloads

   # Allow nginx to enter your home directory
   sudo chmod g+x /home/lzw
   ```

   Reload nginx:

   ```bash
   sudo systemctl reload nginx
   ```

   Then open <http://192.168.1.36/movies/> in your browser — it should show directory listing.

### If you really want nginx to run fully as lzw (not recommended)

You must avoid privileged operations:

- Change `listen 80;` → `listen 8080;` (or any port > 1024)
- Move logs to a folder lzw owns:

  In `/etc/nginx/nginx.conf`:

  ```nginx
  user lzw lzw;
  error_log  /home/lzw/nginx/error.log warn;
  http {
      access_log /home/lzw/nginx/access.log;
  }
  ```

  Create the folder first:

  ```bash
  mkdir -p /home/lzw/nginx
  chown lzw:lzw /home/lzw/nginx
  ```

  But again: this only makes sense for testing or if port 80 is blocked/used by something else. For normal use → keep the default root-master + www-data-workers model.

### Quick one-liner sequence to recover right now

```bash
sudo rm -f /etc/systemd/system/nginx.service.d/override.conf
sudo systemctl daemon-reload
sudo sed -i '/^user\s\+lzw/d' /etc/nginx/nginx.conf   # remove user line if present
sudo nginx -t && sudo systemctl restart nginx
sudo systemctl status nginx
```

After this nginx should start normally again. Then apply the group permissions fix for your `/movies/` location.

**References:**

- None needed – this follows standard nginx startup and Linux privilege behavior.
