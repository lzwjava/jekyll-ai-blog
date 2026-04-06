---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resolve Nextcloud-Talk Configuration Error
translated: false
type: note
---

Question: How do I resolve the "invalid config" error regarding the legacy Nextcloud-Talk setting in OpenClaw?

Answer: The error indicates that the configuration key `allowPrivateNetwork` has been deprecated in OpenClaw 2026.4.5 and replaced with a more explicit security setting. You can resolve this by updating your JSON configuration file manually or using the built-in repair tool.

### Option 1: Automatic Repair (Recommended)
The fastest way to fix the syntax is to let the OpenClaw CLI handle the migration. Run the following command in your terminal:

```bash
openclaw doctor --fix
```

This will automatically rename the legacy key to the new standard in your `~/.openclaw/openclaw.json` file.

### Option 2: Manual Edit
If you prefer to edit the file yourself, open `/home/lzw/.openclaw/openclaw.json` and locate the `nextcloud-talk` channel section.

**Old Configuration:**
```json
"nextcloud-talk": {
  "allowPrivateNetwork": true
}
```

**New Configuration:**
```json
"nextcloud-talk": {
  "network": {
    "dangerouslyAllowPrivateNetwork": true
  }
}
```

### Restart the Gateway
Once the changes are saved, you can restart the service:

```bash
openclaw gateway restart
```