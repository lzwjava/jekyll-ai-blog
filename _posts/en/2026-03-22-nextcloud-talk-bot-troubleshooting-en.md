---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nextcloud Talk Bot Troubleshooting and Fixes
translated: false
type: note
---

Here's the full breakdown of what went wrong and how each issue was fixed:

---

### 1. Installing Nextcloud Talk (spreed app)

**Problem:** `occ app:install spreed` failed — Docker's internal DNS couldn't resolve `github.com`.

**Fix:** Downloaded the spreed v23.0.2 tarball from GitHub API on the host, `docker cp`'d it into the container, extracted to `custom_apps/spreed/`, then ran `composer install` inside the container (after installing composer) to generate the `vendor/autoload.php`.

### 2. Missing frontend assets (404 on CSS/JS)

**Problem:** GitHub source has no pre-built frontend — `talk-main.css`, `talk-icons.css`, etc. were all 404.

**Fix:** Built the frontend on the host using `npm install && npm run build`, then `docker cp`'d the compiled `css/` and `js/` directories into the container. Fixed ownership to `www-data`.

### 3. Plugin installation

**Problem:** None — `openclaw plugins install @openclaw/nextcloud-talk` worked fine. The plugin was already bundled as a stock plugin.

**Fix:** No fix needed, but note: there's a "duplicate plugin" warning because both the stock and installed copies exist. It works regardless.

### 4. Bot created with wrong features

**Problem:** `talk:bot:install --feature reaction` set features=8 (assistant only), so the bot never received chat messages. Zero error count, zero webhooks sent.

**Fix:** Deleted the bot from DB, reinstalled with `--feature webhook --feature response --feature reaction` (features=11). Then ran `talk:bot:setup 3 eu42ecdy` to enable it in the room.

### 5. UFW firewall blocking port 8788

**Problem:** The Nextcloud container couldn't reach `172.19.0.1:8788` — UFW default policy is `deny (incoming)` and port 8788 wasn't allowed. Other Docker ports (3000, 8080) worked because they had explicit UFW rules.

**Fix:** `sudo ufw allow 8788/tcp comment "OpenClaw Nextcloud Talk webhook"`

### 6. groupPolicy blocking rooms

**Problem:** Default `groupPolicy` is `allowlist`, and no rooms were listed — all messages silently dropped.

**Fix:** `openclaw config set channels.nextcloud-talk.groupPolicy open` + added room-specific config.

### 7. Gateway restart needed

**Problem:** Config changes require a gateway restart to take effect.

**Fix:** `openclaw gateway restart` after each config change.

---

### TL;DR order of operations

```bash
# 1. Install & build spreed app in Nextcloud
# 2. Install OpenClaw plugin
openclaw plugins install @openclaw/nextcloud-talk

# 3. Create bot with CORRECT features
docker exec nextcloud-app-1 php occ talk:bot:install "OpenClaw" "<secret>" "<webhook-url>" --feature webhook --feature response --feature reaction
docker exec nextcloud-app-1 php occ talk:bot:setup <bot-id> <room-token>

# 4. Open firewall
sudo ufw allow 8788/tcp

# 5. Configure OpenClaw
openclaw config set channels.nextcloud-talk.enabled true
openclaw config set channels.nextcloud-talk.baseUrl "http://localhost:8080"
openclaw config set channels.nextcloud-talk.botSecret "<secret>"
openclaw config set channels.nextcloud-talk.groupPolicy open

# 6. Restart
openclaw gateway restart
```

The big gotcha was #4 — the feature flags. `--feature reaction` alone doesn't give the bot `webhook` capability, so it never received any messages.