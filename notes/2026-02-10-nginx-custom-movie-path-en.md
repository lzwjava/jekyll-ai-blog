---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Nginx Config for Custom Movie Path
translated: false
type: note
---

**Question:** Change the Nginx configuration to serve files from /home/lzw/qDownloads instead of /var/www/movies/, keeping the /movies/ URL path and directory listing enabled.

**Answer:**

Here is the updated Nginx configuration using your new directory:

```nginx
server {
    listen 80;
    server_name localhost;

    location /movies/ {
        alias /home/lzw/qDownloads/;
        autoindex on;
    }
}
```

### Alternative version (using `root` instead of `alias` – also very common):

```nginx
server {
    listen 80;
    server_name localhost;

    location /movies/ {
        root /home/lzw;
        # or: root /home/lzw/qDownloads/..;  ← same effect
        try_files $uri $uri/ =404;
        autoindex on;
    }
}
```

### Most recommended version (clean + safe):

```nginx
server {
    listen 80;
    server_name localhost;

    location /movies/ {
        alias /home/lzw/qDownloads/;
        autoindex on;

        # Optional but recommended additions:
        charset utf-8;
        autoindex_exact_size off;     # shows human-readable sizes (KB, MB…)
        autoindex_localtime on;       # shows file times in server timezone
    }
}
```

After changing the config:

1. Check syntax:  
   `sudo nginx -t`

2. Reload nginx:  
   `sudo systemctl reload nginx`  
   or  
   `sudo nginx -s reload`

Now http://your-server-ip/movies/ should show the contents of `/home/lzw/qDownloads/`.

**References:**

- None needed for this straightforward config change.