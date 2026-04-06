---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nextcloud Talk Config Structure Error
translated: false
type: note
---

The issue is that the Nextcloud Talk config schema uses `.strict()`, which rejects unknown keys. But the keys in your config (`enabled`, `baseUrl`, `botSecret`, etc.) are actually valid — they just need to be nested properly.

Looking at the schema in `extensions/nextcloud-talk/src/config-schema.ts`, the top-level `channels.nextcloud-talk` object expects the `NextcloudTalkConfigSchema` shape, which extends `NextcloudTalkAccountSchemaBase` and adds `accounts` and `defaultAccount`.

The keys you have (`enabled`, `baseUrl`, `botSecret`, `dmPolicy`, `allowFrom`, `rooms`, `webhookPublicUrl`, `network`) are all valid account-level keys — so they should work at the top level too since the top-level schema extends the account schema.

This likely means either:
1. Your config has a slightly different structure than expected (maybe an extra nesting level or typo)
2. The schema was recently tightened and your config predates it

Try running:

```
openclaw doctor --fix
```

If that doesn't work, check your config:

```
cat ~/.openclaw/openclaw.json | jq '.channels["nextcloud-talk"]'
```

And compare the keys against what the schema accepts. The schema does accept all those keys — so there may be a version mismatch between your installed `openclaw` and the config format. Updating to the latest version (`sudo npm i -g openclaw@latest`) might resolve it.