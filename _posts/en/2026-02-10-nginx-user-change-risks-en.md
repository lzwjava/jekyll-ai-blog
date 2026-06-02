---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Nginx User Change Risks and Steps
translated: false
type: note
---

**Question:** What if I change the Nginx running user to 'lzw' instead of 'www-data'?

**Answer:**

You can change Nginx to run as your own user `lzw`. This will solve the permission problem immediately because Nginx will then have the same access rights as you do (you can read `/home/lzw/qDownloads` without any extra chmod).

However, this approach has **important advantages and disadvantages**. Here is a clear comparison and how to do it safely.

### Advantages
- Immediate fix — no need to change folder permissions, chmod, chgrp, etc.
- Very convenient for personal/test/development machines
- Nginx can access anything your user `lzw` can access

### Big disadvantages / security risks
- If there is any nginx security vulnerability (remote code execution, misconfiguration, etc.), the attacker gets full rights as user `lzw` → can read all your files, ssh keys, qBittorrent downloads, personal data, etc.
- `www-data` is a low-privilege system user with no login shell and very limited rights → much safer
- Breaks standard Ubuntu/Debian packaging expectations (logrotate, apparmor profiles, php-fpm pools, etc. expect `www-data`)
- Some monitoring/security tools flag non-standard users as suspicious

→ **Only do this on a private, non-internet-facing machine or a test setup.**

### How to change Nginx to run as user `lzw`

Two main ways (choose **one**):

#### Method 1 – Edit the systemd service file (recommended, cleanest)

```bash
sudo systemctl edit nginx
```

This opens an editor. Paste the following:

```ini
[Service]
User=lzw
Group=lzw
```

Save and exit.

Then reload systemd and restart nginx:

```bash
sudo systemctl daemon-reload
sudo systemctl restart nginx
```

#### Method 2 – Edit the main nginx config (older / less preferred way)

Edit `/etc/nginx/nginx.conf`:

```nginx
user lzw lzw;    # first = user, second = group
```

Then restart:

```bash
sudo nginx -t
sudo systemctl restart nginx
```

### After changing

Check that nginx is now running as `lzw`:

```bash
ps aux | grep nginx
# You should see lines like: lzw   ... nginx: worker process
```

Then test your `/movies/` URL again — it should work without any 403 errors (assuming the directory exists and has files).

### Recommendation summary – 2026 best practice

| Situation                        | Recommended approach                          |
|----------------------------------|-----------------------------------------------|
| Personal NAS / home server       | Change to user `lzw` (quick & easy)           |
| Any public-facing / internet server | Keep `www-data` + fix permissions (chmod/chgrp) |
| You want both convenience + safety | Use `chgrp www-data` + `chmod g+rx` method    |

If you decide to go with user `lzw`, Method 1 (systemd override) is the cleanest and survives package upgrades.

**References:**

- None needed – this is standard nginx + systemd configuration knowledge.
