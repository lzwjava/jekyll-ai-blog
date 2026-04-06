---
audio: false
generated: true
image: false
lang: en
layout: post
title: Plugin Configuration Schema Bug
translated: false
type: note
---

**The problem:**
Your openclaw gateway wouldn't start because config validation rejected all keys under `channels.nextcloud-talk` — `enabled`, `baseUrl`, `botSecret`, `dmPolicy`, `allowFrom`, `rooms`, `webhookPublicUrl`, `network` — as "unrecognized".

**Investigation:**

1. SSHed into `lzw@192.168.1.36` and read `~/.openclaw/openclaw.json`. The nextcloud-talk config looked correct — all those keys are valid account-level fields per the source schema in `extensions/nextcloud-talk/src/config-schema.ts`.

2. Found two versions of the plugin: a stale external install at `2026.3.13` (in `~/.openclaw/extensions/nextcloud-talk/`, referenced in `plugins.installs`) and the bundled version at `2026.4.5` (in the global npm openclaw package at `dist/extensions/nextcloud-talk/`).

3. Inspected the bundled plugin's `openclaw.plugin.json` — it declares `"configSchema": {"type": "object", "additionalProperties": false, "properties": {}}`. Empty properties with `additionalProperties: false` means the manifest-level JSON Schema rejects every key. This is the direct cause of the validation error. The runtime TypeScript schema (zod) never gets a chance to run because the manifest schema blocks first.

4. The bundled plugin also has a broken export — `index.js` is missing the `register/activate` function, so even with valid config the plugin wouldn't load.

5. Tried `openclaw doctor --fix` but it couldn't help because config validation runs before doctor logic.

**What was changed on the remote machine:**

- Removed the stale `nextcloud-talk` entry from `plugins.installs` (so it doesn't try to load the old `2026.3.13` version)
- Saved the original nextcloud-talk channel config to `~/.openclaw/nextcloud-talk-backup.json`
- Set `channels.nextcloud-talk` to `{}` in `openclaw.json`
- Verified `openclaw doctor --fix` now runs successfully — Telegram, Slack, WhatsApp, and openclaw-weixin all report healthy

**Conclusion:** This is a packaging/build bug in openclaw `2026.4.5` — the nextcloud-talk plugin shipped with an empty config schema and broken exports. The config you had was valid; the plugin just can't accept it in this version. Once a fixed release ships, restore the backup config.