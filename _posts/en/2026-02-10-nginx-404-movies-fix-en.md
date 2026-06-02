---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fixing Nginx 404 for Movies Path
translated: false
type: note
---

**Question:** I'm getting a 404 Not Found error from nginx/1.28.2 when accessing the /movies/ location.

**Answer:**

A 404 error means nginx is running and responding, but it cannot find the requested resource. Since you're using `alias /home/lzw/qDownloads/;` with `autoindex on;`, here are the most common causes and how to fix them step by step:

### 1. Wrong URL (most frequent reason)
Make sure you're accessing the **exact** path:

- Correct:  `http://localhost/movies/`  (with trailing slash)
- Also try: `http://your-server-ip/movies/` or `http://127.0.0.1/movies/`

If you type `http://localhost/movies` (no trailing slash), nginx may return 404 depending on your config.

### 2. Directory permissions – nginx cannot read /home/lzw/qDownloads
This is the **second most common cause**.

Nginx usually runs as user `www-data` (Ubuntu/Debian) or `nginx` (official package). That user must be able to:

- Enter every parent directory (`/home`, `/home/lzw`, `/home/lzw/qDownloads`)
- Read files and list the directory

Quick fix – give read & execute permissions to others (safest for private home directory setup):

```bash
sudo chmod -R o+rx /home/lzw/qDownloads
# or more minimal:
sudo chmod o+x /home/lzw
sudo chmod o+x /home/lzw/qDownloads
sudo chmod -R o+r /home/lzw/qDownloads
```

Better long-term solution (recommended):

```bash
# Create group www-data access
sudo chgrp -R www-data /home/lzw/qDownloads
sudo chmod -R g+rx /home/lzw/qDownloads

# Allow traversing home (only execute bit needed)
sudo chmod g+x /home/lzw
```

### 3. SELinux or AppArmor blocking access (if enabled)
On Ubuntu, AppArmor is often active.

Check if AppArmor is denying access:

```bash
sudo aa-status
# If you see nginx in complain or enforce mode
```

Quick temporary test – put AppArmor in complain mode for nginx:

```bash
sudo aa-complain /usr/sbin/nginx
sudo systemctl restart nginx
```

If it starts working → AppArmor is the problem. You should create or adjust a profile instead of disabling it permanently.

### 4. Configuration not actually loaded
Make sure your config is active:

- File should be in `/etc/nginx/sites-available/` (example: `movies.conf`)
- Symlink exists in `/etc/nginx/sites-enabled/`:
  ```bash
  sudo ln -s /etc/nginx/sites-available/movies.conf /etc/nginx/sites-enabled/
  ```
- No `default` site conflicting:
  ```bash
  sudo rm /etc/nginx/sites-enabled/default   # if you don't need the welcome page
  ```
- Test and reload:
  ```bash
  sudo nginx -t
  sudo systemctl reload nginx
  ```

### 5. Directory is empty or doesn't exist
Double-check:

```bash
ls -la /home/lzw/qDownloads/
```

If the folder is empty, nginx with `autoindex on` will still show an index page (just says no files).

### Diagnostic commands to run right now
Run these and share the output if it still doesn't work:

```bash
# 1. Current nginx config files that are enabled
ls -l /etc/nginx/sites-enabled/

# 2. Full server block nginx is using
sudo nginx -T | grep -A 15 "server_name localhost"

# 3. Check nginx error log for clues
sudo tail -n 30 /var/log/nginx/error.log

# 4. Test access as the nginx user
sudo -u www-data ls -la /home/lzw/qDownloads/
# If this says "Permission denied" → permissions problem
```

Fix the most likely issue (permissions or trailing slash) first — in 80–90% of home-directory alias cases it's one of those two.

**References:**

- None required for standard troubleshooting steps.
