---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pi End-to-End Verification Success
translated: false
type: note
---

Done and verified end-to-end.

## Result on `lzw@192.168.1.49`

**Final check: `pi -p "Reply with exactly: PI-WORKS"` → `PI-WORKS`** (via `deepseek/deepseek-v4-flash`).

### What I found

You had **already installed pi yourself** at `~/.local` (created 17:52, while I was working) — that's the `# Pi` PATH line and the empty `sessions/` dir I spotted. I had concurrently installed a second copy to `~/.npm-global`. Both were `0.85.1`, so I **consolidated on yours**: removed my `~/.npm-global` copy and reverted the npm prefix I'd set (`~/.npmrc` deleted → back to `/usr/local`).

### Config copied to `~/.pi/agent/`

| File | Notes |
| --- | --- |
| `settings.json` | `deepseek` / `deepseek-v4-flash`, thinking=high |
| `models-store.json` | 304 KB catalog (deepseek, mistral, openrouter) |
| `auth.json` | `{}` — empty on the source too |
| `trust.json` | `/home/lzw/projects` |
| `AGENTS.md` | your global English-only rule |
| `extensions/` | `done-sound.ts`, `note/index.ts` (both use `homedir()`, portable) |
| `bin/fd` | pi's file-search binary |

**Not copied:** `sessions/` (25 MB of history — that's history, not config). Say the word if you want it.

### Env keys

Appended to `~/.bashrc` (12 lines, idempotent): `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`, `MISTRAL_API_KEY`, `CLOUDFLARE_API_KEY`, `CLOUDFLARE_API_TOKEN`, `TELEGRAM_BOT_API_KEY`, `TELEGRAM_LOCATION_BOT_API_KEY`, `SERVER_IP`, `MODEL_PROVIDER`, `MODEL`. Skipped the commented-out Cloudflare key and machine-specific `CLASH_EXECUTABLE` (points at a local path that doesn't exist on the target).

Also added `~/.local/bin/rg` (ripgrep 14.1.0) — the target had no `rg` or `fd`.

### Three things worth knowing

1. **A wrong test nearly sent me down a rabbit hole.** My first checks used `ssh host 'bash -lc ...'` and pi reported *"No API key found"* and *"No models available."* The cause is Ubuntu's `.bashrc` early-return for non-interactive shells — **not** a config problem.

2. **Your keys only load in interactive shells.** I verified with `env -i`: a clean login shell has `DEEPSEEK=` **empty on both the source machine and the target**. So the target now matches your source behavior exactly. But anything non-interactive — `ssh 192.168.1.49 'pi ...'`, cron, systemd — will fail to authenticate. Tell me if you want these moved to `~/.profile` or a `BASH_ENV` file to cover that.

3. **`npm install -g` needs sudo on the target** (prefix is back to `/usr/local`). Your working convention is `npm install -g --prefix ~/.local`, which is how your pi got there. I could set `prefix=~/.local` in `~/.npmrc` to make plain `npm install -g` work without sudo — I left it alone deliberately, since it's your machine's default.

Still outstanding from the previous task: **mihomo is running (pid 7445) but is not a service**, so it and pi's setup won't survive a reboot. Want me to add a systemd user service for mihomo?
