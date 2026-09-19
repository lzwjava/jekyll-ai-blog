---
audio: false
generated: true
image: false
lang: en
layout: post
title: Config Repo Analysis and Findings
translated: false
type: note
---

Copied and verified.

## `~/projects/config` → `192.168.1.49:~/projects/config`

1.1 MB, copied as a whole (tar + scp) **with `.git` intact**:

```
git status → ## main...origin/main    (clean)
HEAD → e0b4e25 Add pi done-sound extension
remote → git@github.com:lzwjava/config.git
```

Contents: `.bashrc`, `.zprofile`, `config.yaml`, `iTerm.json`, `IDEA-settings.zip`, `README.md`, `claude/settings.json`, `hermes/` (config + plugins), `openclaw/openclaw.json`, `ww/.env` + `.env.win`, `pi/`, `test.md`. Your `~/projects/start-pi.sh` was left untouched.

### The interesting find: that `config.yaml` is your mihomo config — and it's *newer* than the live one

It's the same mihomo config I installed in the first task, but the repo copy (`Aug 14`) is newer than live (`Apr 10`) and **differs exactly where I hit trouble**:

```diff
   - name: "Proxy"
     type: select
     proxies:
+      - My Hysteria2 2      # repo: working node FIRST
       - My SS 1             # live: dead node FIRST
   ...
+  - DOMAIN-SUFFIX,kimi.com,Proxy
+  - DOMAIN-SUFFIX,trae.ai,Proxy
+  - DOMAIN-SUFFIX,discord.com,Proxy
```

That reordering is precisely the fix for the dead-node problem I reported — with this version the target would never cold-start onto the dead `My SS 1`. It also adds 3 rules. Note the repo has no `Rules/` dir, but the rule-providers are `type: http`, so mihomo fetches them by URL anyway.

Want me to apply this `config.yaml` as the mihomo config on the target (replacing the older one I copied), and also update it locally?

### Three caveats

1. **The repo's `pi/` snapshot is stale — don't use it as source of truth.** It's `lastChangelogVersion: 0.81.1` with no `defaultThinkingLevel`, and both extensions differ from live. The live `~/.pi/agent/` I copied earlier (`0.85.1`, thinking=high) is the correct one. The repo's `pi/agent/settings.json` would silently drop your `defaultThinkingLevel: high`.

2. **Secrets are now on the target** — `ww/.env` carries `GITHUB_TOKEN`, `GITHUB_PAT_TOKEN`, `OPENROUTER_API_KEY`, `GOOGLE_MAPS_API_KEY`. Expected for a config repo, but worth knowing it's sitting in plaintext there.

3. **The git remote won't work from the target.** Its `~/.ssh/` has only `authorized_keys` (inbound), no key, so:
   ```
   git@github.com: Permission denied (publickey).
   ```
   So this is a static snapshot — no `git pull` there until you add a deploy key or switch to HTTPS.