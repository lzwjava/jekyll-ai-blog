---
audio: false
date: 2025-09-14
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Disabling LibreChat Authentication Workarounds
translated: false
type: note
---

Short answer: you can’t completely turn off authentication in LibreChat, but you can stop the “keep asking me to log in” problem and make it feel close to “no-login.” Here’s what actually works (and why):

### 1) You can’t disable auth entirely

This is confirmed by the maintainer: registration can be disabled, but the auth system itself can’t be turned off. ([GitHub][1])

### 2) Why you keep getting logged out

If you access your instance over **HTTP** (e.g., LAN IP), cookies are marked `secure` in production so the browser won’t keep them; you get booted back to login. Use **HTTPS** (even self-signed) or run the API in a dev mode that disables secure cookies. ([GitHub][1])

### 3) Two reliable fixes

#### Option A — Proper/secure (recommended)

* Put LibreChat behind HTTPS (nginx/caddy/traefik; self-signed is fine on LAN).
* Then bump the session windows in your `.env`:

  ```
  SESSION_EXPIRY=1000 * 60 * 60 * 24       # 24h
  REFRESH_TOKEN_EXPIRY=(1000 * 60 * 60 * 24) * 30  # 30d
  ```
* Restart containers after changing env.
  This keeps you logged in for days/weeks and fixes the cookie drop. ([GitHub][2])

#### Option B — “I’m on a private LAN and just want it to stop logging out”

* Create a `docker-compose.override.yml` and run the API in dev mode (disables secure cookies):

  ```yaml
  services:
    api:
      command: npm run backend:dev
  ```
* `docker compose up -d` to apply.
  This is less secure (cookies not `secure`), but it stops the forced re-login over plain HTTP. ([librechat.ai][3])

### 4) Optional quality-of-life tweaks

* **Disable new signups** so it’s effectively single-user:

  ```
  ALLOW_REGISTRATION=false
  ```

  (You can still add users via `npm run create-user` if needed.) ([librechat.ai][4])
* Keep other auth toggles in `.env` (email/social login flags) if you want the simplest login path. ([librechat.ai][5])

### 5) Quick checklist for your case (v0.8.0-rc3)

1. Decide: HTTPS proxy (best) **or** dev mode (quick LAN fix).
2. Set longer `SESSION_EXPIRY` and `REFRESH_TOKEN_EXPIRY` in `.env`.
3. Restart the stack so env changes take effect.
4. (Optional) Turn off registration for a “single-user” feel.

If you want, paste your current `docker-compose.yml` and `.env` (without secrets). I’ll mark exactly what to add/change for your setup.

[1]: https://github.com/danny-avila/LibreChat/discussions/572 "[Question]: Require login every time refresh · danny-avila LibreChat · Discussion #572 · GitHub"
[2]: https://github.com/danny-avila/LibreChat/discussions/2571?utm_source=chatgpt.com "Is there a way to increase or disable the auto-logoff time?"
[3]: https://www.librechat.ai/blog/2024-05-16_unsecured_http "GitHub"
[4]: https://www.librechat.ai/docs/configuration/authentication "GitHub"
[5]: https://www.librechat.ai/docs/configuration/dotenv "GitHub"
