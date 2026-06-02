---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Nginx User and Permissions Error
translated: false
type: note
---

**Question:** Why is nginx failing to start after changing the user to 'lzw', and how do I fix the permission denied error on /var/log/nginx/error.log plus the warning about the "user" directive?

**Answer:**

Nginx fails to start because you changed the user to `lzw` (a normal non-root user), but the master process still needs **root privileges** to:

- Bind to port 80 (privileged port < 1024)
- Open/write log files owned by root or www-data (like `/var/log/nginx/error.log`)
- Perform other privileged operations

When you run nginx as a non-root user (`lzw`), it cannot open `/var/log/nginx/error.log` → **Permission denied (13)** → emergency exit.

The warning message
`the "user" directive makes sense only if the master process runs with super-user privileges, ignored`
confirms exactly this: nginx ignored your `user lzw;` line because it wasn't started as root.

### Recommended Fix – Keep nginx running as root (master) but drop to user `lzw` for workers

This is the **standard and safe** way nginx is designed to work.

1. **Remove or undo the user change** you made earlier

   If you used `systemctl edit nginx` and added:

   ```ini
   [Service]
   User=lzw
   Group=lzw
   ```

   Delete that override:

   ```bash
   sudo rm /etc/systemd/system/nginx.service.d/override.conf
   sudo systemctl daemon-reload
   ```

   Or if you edited `/etc/nginx/nginx.conf` and added `user lzw lzw;`, comment it out or remove it:

   ```nginx
   # user lzw lzw;   ← comment or delete this line
   ```

2. **Restart nginx (should work again as www-data)**

   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   sudo systemctl status nginx
   ```

3. **Fix the original directory permission problem** (so /movies/ works without 403)

   Use the group method (clean & secure):

   ```bash
   sudo chgrp -R www-data /home/lzw/qDownloads
   sudo chmod -R g+rx /home/lzw/qDownloads
   sudo chmod g+x /home/lzw               # allow group to traverse your home
   ```

   Then reload:

   ```bash
   sudo systemctl reload nginx
   ```

   Test: `http://192.168.1.36/movies/`

### Alternative – Run everything as user lzw (not recommended for port 80)

If you really want nginx to run completely as `lzw` (no root at all):

- Change listen port to something > 1024 (e.g. 8080)
- Fix all log / pid file permissions

Example config changes in `/etc/nginx/nginx.conf`:

```nginx
user lzw lzw;
...
http {
    ...
    access_log /home/lzw/nginx/access.log;
    error_log  /home/lzw/nginx/error.log;
}
```

And in your server block:

```nginx
server {
    listen 8080;
    ...
}
```

Then also create the log directory and give ownership:

```bash
mkdir -p /home/lzw/nginx
chown lzw:lzw /home/lzw/nginx
```

But again: **this is only practical if you don't need port 80/443**. Most people keep the default root → drop-privileges model.

### Quick summary – what to do right now (99% of cases)

```bash
# 1. Undo the bad systemd override
sudo rm /etc/systemd/system/nginx.service.d/override.conf
sudo systemctl daemon-reload

# 2. (optional) make sure no user line in nginx.conf
sudo nano /etc/nginx/nginx.conf   # remove or comment "user lzw ..."

# 3. Fix your download folder perms
sudo chgrp -R www-data /home/lzw/qDownloads
sudo chmod -R g+rx /home/lzw/qDownloads
sudo chmod g+x /home/lzw

# 4. Start nginx normally
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx
```

You should see Active: active (running) and no permission errors.

**References:**

- None required – this is standard nginx privilege model behavior documented on nginx.org.
