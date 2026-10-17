---
audio: false
generated: true
image: false
lang: en
layout: post
title: HTTPS Live and Auto-Renewing
translated: false
type: note
---

HTTPS is live and renewing automatically. Summary:

## Live now

```
https://web.funlive.io/   → 200 (HTTP/2, TLS 1.2/1.3)
https://web.funlive.io/api/lives/1 → 200
http://web.funlive.io/    → 301 https://web.funlive.io/
```

Cert: **Let's Encrypt** `CN=web.funlive.io`, valid until **2027-01-13**, chain verified (`ssl_verify_result 0`). Mobile site on port 80/8088 untouched (still 200).

## How it's set up (on the VM, `/home/lzw/live-server`)

**docker-compose.yml**

- New `certbot` service (`certbot/certbot`) with two volumes: `letsencrypt` → `/etc/letsencrypt`, `certbot-www` → `/var/www/certbot` (ACME http-01 webroot)
- `web` (nginx) got `443:443` published plus read-only mounts of both volumes

**nginx.conf** — two new blocks for `web.funlive.io`:

- `:80` — serves `/.well-known/acme-challenge/` from the webroot volume, 301s everything else to HTTPS
- `:443 ssl` + `http2 on` — full SPA config + Mozilla-intermediate TLS settings; `/api/` still proxied to the CI4 app

**`/home/lzw/live-server/renew-certs.sh`** — `docker compose run --rm certbot renew` + nginx reload. Installed in crontab: `17 3 * * *`, output to `renew-certs.log`. Verified with `certbot renew --dry-run` (success) and one real run of the script (exit 0).

**GCP** — the VM already had the `https-server` network tag, so the existing `default-allow-https` firewall rule covers 443. No Namecheap change needed (no paid cert to buy).

## Repo updated (`~/projects/live-web`)

- `deploy/nginx-web.conf` — reference copy of the full VM config (verified byte-identical apart from the header comment)
- `README.md` — new "HTTPS (Let's Encrypt)" section with the renewal commands

Deploy flow is unchanged: `./deploy/deploy.sh` (it never touches certs; only a rebuild + `nginx` apply).

Two optional follow-ups if you want them:

- **HSTS** — add `add_header Strict-Transport-Security "max-age=31536000" always;` to the `:443` block (safe: it only affects the `web.funlive.io` hostname).
- **HTTPS for the mobile site** — it currently has no hostname (served on the IP/`localhost` block). If you give it a domain, I can reuse the same certbot volumes.
