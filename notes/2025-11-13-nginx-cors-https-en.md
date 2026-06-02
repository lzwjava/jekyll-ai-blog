---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Nginx CORS and HTTPS Configuration
translated: false
type: note
---

```nginx
# Define a map to handle the allowed origins
map $http_origin $cors_origin {
    default "https://example.com";
    "http://localhost:3000" "http://localhost:3000";
    "https://example.com" "https://example.com";
    "https://www.example.com" "https://www.example.com";
}
```

### What it does

- Creates a variable `$cors_origin` based on the value of the incoming `Origin` header (`$http_origin`).
- If the request comes from `http://localhost:3000`, `https://example.com`, or `https://www.example.com`, it echoes that exact origin back.
- For any other origin (or no origin), it defaults to `https://example.com`.
- This is used later to set the `Access-Control-Allow-Origin` header dynamically, enabling CORS only for trusted front-end domains.

---

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com api.example.com;
    return 301 https://$host$request_uri;
}
```

### What it does

- Listens on port 80 (HTTP).
- Matches requests to `example.com` or `api.example.com`.
- Permanently redirects (301) all traffic to the HTTPS version of the same URL.
- Forces secure connections; no plain HTTP access is allowed.

---

```nginx
# Main site configuration for example.com
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";

    root /home/project/project-web;
    index index.html index.htm index.php default.html default.htm default.php;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$ {
        expires 30d;
    }

    location ~ .*\.(js|css)?$ {
        expires 12h;
    }

    error_page 404 /index.html;
}
```

### What it does

- **HTTPS server** for `example.com` on port 443 with SSL enabled.
- Uses **Let’s Encrypt** certificates (auto-renewable, free).
- Enforces modern TLS versions (`TLSv1.2`, `TLSv1.3`) and strong ciphers for security.
- Serves static files from `/home/project/project-web`.
- Tries to serve requested file → directory → 404.
- Sets **cache headers**:
  - Images: cache for 30 days.
  - JS/CSS: cache for 12 hours.
- All 404 errors are routed to `index.html` → enables **SPA (Single Page App)** routing (e.g., React, Vue).

---

```nginx
# API configuration for api.example.com
server {
    listen 443 ssl;
    server_name api.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com-0001/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com-0001/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";

    location / {
        # Clear any pre-existing Access-Control headers
        more_clear_headers 'Access-Control-Allow-Origin';

        # Handle CORS preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' $cors_origin;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
            add_header 'Access-Control-Allow-Headers' 'Origin, Content-Type, Accept, Authorization, X-Client-Info, X-Trace-Id, X-Requested-With, X-HTTP-Method-Override, DNT, Keep-Alive, User-Agent, If-Modified-Since, Cache-Control, Content-Range, Range';
            add_header 'Access-Control-Max-Age' 3600;
            return 204;
        }

        add_header 'Access-Control-Allow-Origin' $cors_origin always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
        add_header 'Access-Control-Allow-Headers' '...' always;

        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        send_timeout 600s;
    }
}
```

### What it does

- **HTTPS reverse proxy** for `api.example.com`.
- Uses a **separate Let’s Encrypt cert** (likely due to multiple domains/SANs).
- All traffic is proxied to a **local backend** running on `localhost:5000` (e.g., Flask, Node.js, etc.).

#### CORS Handling

- Uses the `$cors_origin` map to **dynamically allow** only approved origins.
- **Clears any existing** `Access-Control-Allow-Origin` to prevent conflicts.
- Handles **OPTIONS preflight**:
  - Returns `204 No Content` immediately.
  - Allows common methods and headers.
  - Caches preflight for 1 hour (`Max-Age: 3600`).
- For actual requests, adds CORS headers with `always` so they appear even on error responses.

#### Proxy Settings

- Forwards real client IP and protocol info to the backend.
- High timeouts (10 minutes) → suitable for long-running API operations (e.g., file uploads, heavy computations).

---

### Summary of Architecture

| Component           | Purpose |
|---------------------|--------|
| `example.com`       | Serves static SPA (React/Vue/etc.) |
| `api.example.com`   | Secure API gateway → backend on port 5000 |
| HTTP → HTTPS        | All traffic enforced over TLS |
| CORS                | Restricted to `example.com`, `www`, and `localhost:3000` |
| Caching             | Optimized for performance |
| SSL                 | Let’s Encrypt, modern ciphers |

### Security Notes

- Strong TLS config (A+ on SSL Labs likely).
- CORS is **not wildcard** → prevents unauthorized sites from calling API.
- Preflight handled efficiently.
- Real IP forwarded → useful for logging/rate-limiting in backend.

Let me know if you want a diagram or Dockerized version!
