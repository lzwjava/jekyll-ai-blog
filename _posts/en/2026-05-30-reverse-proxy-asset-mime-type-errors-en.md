---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reverse Proxy Asset MIME Type Errors
translated: false
type: note
---

**Question:** Why is `https://liber.davirain.xyz` throwing MIME type errors for CSS and JS assets?

**Answer:**

These are classic **reverse proxy misconfiguration** or **asset path routing** errors. Here's exactly what's happening:

## Root Cause

The browser fetched `https://liber.davirain.xyz/assets/index-KsAjyADz.css` but the server returned `Content-Type: text/html` instead of `text/css`. Same for the JS file — got `text/html` back when it expected `application/javascript`.

This means the server is **returning an HTML page** (likely a 404 or index.html fallback) for those asset URLs, not the actual files.

## Why This Happens

**Most likely causes, in order of probability:**

### 1. SPA fallback misconfiguration (most common)

The server has a catch-all rule that serves `index.html` for all unmatched routes — including `/assets/*`. This is a common Nginx/Caddy misconfiguration for SPAs:

```nginx
# BAD: this catches /assets/* too
location / {
    try_files $uri $uri/ /index.html;
}
```

Fix: assets should be served before the fallback:

```nginx
location /assets/ {
    root /var/www/dist;
    # no try_files fallback here
}

location / {
    try_files $uri /index.html;
}
```

### 2. Assets not deployed / wrong build output path

The `/assets/` directory wasn't uploaded or the build output dir is wrong. Server can't find the file → returns 404 HTML page.

Check: `curl -I https://liber.davirain.xyz/assets/index-KsAjyADz.css` — if you get `200` with `text/html`, it's serving index.html. If `404`, assets aren't there.

### 3. CDN/proxy stripping the path

A reverse proxy (Cloudflare, Nginx upstream) is rewriting `/assets/...` to `/` and serving the root HTML.

### 4. Wrong `base` in Vite/build config

The app was built with a non-root base (e.g. `base: '/subpath/'`) but deployed to root, so asset URLs resolve to wrong paths:

```js
// vite.config.js
export default {
  base: '/liber/'  // assets become /liber/assets/... but deployed at /
}
```

## Quick Diagnosis

```bash
# Check what the server actually returns for the CSS file
curl -sv https://liber.davirain.xyz/assets/index-KsAjyADz.css 2>&1 | grep -E "content-type|HTTP/"

# Check if it's serving HTML
curl -s https://liber.davirain.xyz/assets/index-KsAjyADz.css | head -5
```

If the output starts with `<!DOCTYPE html>` — confirmed: server is returning index.html for asset requests.

## Fix

Depends on the stack. If it's a static site on Nginx:

```nginx
server {
    listen 443 ssl;
    server_name liber.davirain.xyz;
    root /var/www/liber/dist;
    index index.html;

    # Serve static assets directly
    location ~* \.(js|css|png|jpg|svg|woff2?)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files $uri =404;  # 404, not fallback to index.html
    }

    # SPA fallback only for HTML routes
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

If hosted on GitHub Pages / Vercel / Netlify — the issue is almost certainly the `base` in `vite.config.js` or the build artifacts not being in the right directory.
