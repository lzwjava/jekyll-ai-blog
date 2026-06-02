---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Install Latest Nginx on Ubuntu
translated: false
type: note
---

**Question:** The command 'nginx' is not found on my system. It suggests installing nginx-core, nginx-extras, or nginx-light. What should I do next to get nginx working?

**Answer:**

You are on an **Ubuntu** (or Debian-based) system, and nginx is not installed yet. Here's the recommended way to proceed in 2025/2026:

### Best option: Install the modern official nginx version (recommended)

The versions suggested by apt (`1.18.0`) are **very old** (released in 2020). You almost certainly want a newer, supported version.

#### Method 1 – Official nginx repository (cleanest & gets latest stable version)

1. Add the official nginx signing key and repository:
```bash
sudo apt update
sudo apt install -y curl gnupg2 ca-certificates lsb-release ubuntu-keyring
curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo gpg --dearmor -o /usr/share/keyrings/nginx-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/ubuntu $(lsb_release -cs) nginx" | sudo tee /etc/apt/sources.list.d/nginx.list
echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" | sudo tee /etc/apt/preferences.d/99nginx
```

2. Install nginx:
```bash
sudo apt update
sudo apt install nginx
```

3. Verify:
```bash
nginx -v
# Should show something like: nginx version: nginx/1.26.x (or newer)
sudo systemctl status nginx
```

#### Method 2 – Quick but older version (if you just want to test right now)

If you don't care about getting the latest version and just want nginx running immediately:
```bash
sudo apt update
sudo apt install nginx
# This will usually install nginx-core or the default variant
```

After either method, your original config should work once you:
- Place it in `/etc/nginx/sites-available/` (e.g. `/etc/nginx/sites-available/movies`)
- Create symlink: `sudo ln -s /etc/nginx/sites-available/movies /etc/nginx/sites-enabled/`
- Remove or disable default site if needed: `sudo rm /etc/nginx/sites-enabled/default`
- Test config: `sudo nginx -t`
- Reload: `sudo systemctl reload nginx` (or `sudo nginx -s reload`)

### Quick summary – what most people should run right now
```bash
# Recommended – get current stable nginx from official source
sudo apt update
sudo apt install -y curl gnupg2 ca-certificates lsb-release ubuntu-keyring
curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo gpg --dearmor -o /usr/share/keyrings/nginx-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/ubuntu $(lsb_release -cs) nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list

sudo apt update
sudo apt install nginx

nginx -v
```

After this you can use the `nginx` command and your directory listing setup at `/movies/` should work.

**References:**

- [http://nginx.org/en/linux_packages.html](http://nginx.org/en/linux_packages.html)
- [https://nginx.org/en/docs/install.html](https://nginx.org/en/docs/install.html)
