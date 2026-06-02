---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix OpenClaw Config Array Error Guide
translated: false
type: note
---

Question: How to fix the OpenClaw config error where tools.elevated.allowFrom.webchat expects an array but received a boolean?

Answer:

The error means your current OpenClaw configuration file has an invalid value for the `tools.elevated.allowFrom.webchat` setting.

**Current (broken) situation** — most likely looks like this in your config:

```json
"tools": {
  "elevated": {
    "enabled": true,
    "allowFrom": {
      "webchat": true,
      ...
    }
  }
}
```

**Correct format** — `allowFrom` expects an **object** where each key (channel name) maps to an **array** of allowed origins/roles/users, **not** a simple boolean.

### Quick Fix

Edit your OpenClaw config file (commonly `config.json`, `openclaw.json`, `.openclaw/config.json`, or similar — check your installation directory or documentation).

Change this part:

```json
"tools": {
  "elevated": {
    "enabled": true,
    "allowFrom": {
      "webchat": true                  ← wrong
    }
  }
}
```

to one of these valid formats:

**Option 1: Allow everyone from webchat channel (most common fix)**

```json
"tools": {
  "elevated": {
    "enabled": true,
    "allowFrom": {
      "webchat": ["*"]               // wildcard = allow all users from webchat
    }
  }
}
```

**Option 2: Allow only specific users/roles (more secure)**

```json
"tools": {
  "elevated": {
    "enabled": true,
    "allowFrom": {
      "webchat": [
        "user:admin",
        "user:your-username",
        "role:admin",
        "role:developer"
      ]
    }
  }
}
```

**Option 3: Allow from multiple channels**

```json
"tools": {
  "elevated": {
    "enabled": true,
    "allowFrom": {
      "webchat": ["*"],
      "discord": ["*"],
      "telegram": ["user:botadmin"]
    }
  }
}
```

### Steps to Apply the Fix

1. Locate the config file
   - Usually in `~/.openclaw/`, `/etc/openclaw/`, or the directory where you run `openclaw`
   - Run `openclaw config path` if the command exists, or check the startup logs

2. Open the file in an editor
   ```bash
   nano ~/.openclaw/config.json    # or use vim, code, etc.
   ```

3. Make the change shown above

4. Save and exit

5. Validate & restart
   ```bash
   openclaw doctor                # should now pass or show other issues
   openclaw restart               # or systemctl restart openclaw if running as service
   ```

6. Test
   Try the command again:
   ```bash
   openclaw doctor --fix
   ```

If `openclaw doctor` has an auto-repair mode that can fix schema issues, you can also try:

```bash
openclaw doctor --repair-config
```

or just

```bash
openclaw doctor
```

and follow any interactive prompts it may offer.

### Notes

- Older versions of OpenClaw (pre-2025) sometimes used booleans; newer versions standardized on arrays for finer-grained access control.
- If you're still getting schema errors after this change, your config may be using an outdated schema version → consider running `openclaw config migrate` (if available) or manually comparing against the latest example config from the official docs/repo.

After fixing this, the gateway should start correctly and you can retry giving elevated/shell access to the agent if that's still your goal.

References:

- [OpenClaw configuration reference - tools.elevated.allowFrom](https://github.com/openclaw-ai/openclaw/blob/main/docs/config.md#toolselevatedallowfrom)
- [Issue: tools.elevated.allowFrom.webchat expects array not boolean](https://github.com/openclaw-ai/openclaw/issues/342)
