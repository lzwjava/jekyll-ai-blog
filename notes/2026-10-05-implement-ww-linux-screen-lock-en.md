---
audio: false
generated: true
image: false
lang: en
layout: post
title: Implement ww linux screen-lock
translated: false
type: note
---

Done. The `ww linux screen-lock` command is implemented and tested on this Ubuntu/GNOME machine (original settings were restored after testing).

## Changes

**New: `ww/linux/screen_lock.py`** — GNOME `gsettings`-backed screen-lock control:

| Command | Effect |
|---|---|
| `ww linux screen-lock` / `status` | Show lock-enabled, lock delay, blank delay, suspend password, lockdown + warnings |
| `ww linux screen-lock delay` | Lock **2h** after the screen blanks (default), enables `lock-enabled` |
| `ww linux screen-lock delay 30m` | Any time: `2h`, `1h30m`, `45s`, plain seconds `7200` |
| `ww linux screen-lock off` | `lock-enabled false` — no idle lock (prints hints for suspend/login passwords) |
| `ww linux screen-lock on` | Re-enable automatic lock, shows current delay |
| `ww linux screen-lock blank [time\|never]` | Set/show `idle-delay` (blank time) |
| `ww linux screen-lock suspend-pw on\|off` | `ubuntu-lock-on-suspend` — password after wake |
| `ww linux screen-lock lockdown on\|off` | `org.gnome.desktop.lockdown disable-lock-screen` (drastic) |

Behavior details:
- Time parser accepts `2h` / `30m` / `45s` / `1h30m` / plain seconds / `never`; invalid input → error + exit 1
- Warns when `idle-delay` is 0 (screen never blanks → idle lock never triggers), and explains that `lock-delay` counts from blank, with the "N hours after idle" recipe from your answer
- Gracefully handles missing keys (`ubuntu-lock-on-suspend` absent on non-Ubuntu GNOME) and exits with a clear error when `gsettings`/GNOME schemas are unavailable

**Wired in:**
- `ww/linux/main.py` — `elif subcmd == "screen-lock":` dispatch + help line
- `ww/main.py` — help line in the `Linux:` section of `ww --help`
- `completions/_ww` — added `screen-lock` (plus previously stale `setup`, `switch-keys`, `pinyin`, `check-fan`) to `linux_cmds`, new `screen_lock_cmds` array, and a `subcmd2` case so `ww linux screen-lock <TAB>` completes actions

Note: `~/.zsh/completions/_ww` doesn't exist on this machine — the completion source lives at `completions/_ww` in the repo, so that's the file I updated (copy it to a dir in `$fpath` and rerun `compinit` to activate).

Not committed — say the word if you want a `feat: add ww linux screen-lock command` commit.