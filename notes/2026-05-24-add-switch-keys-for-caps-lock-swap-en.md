---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add switch-keys for Caps Lock swap
translated: false
type: note
---

Here's a full breakdown of the commit:

**Commit:** `cf64c23` — `feat: add ww linux switch-keys — swap Caps Lock and Left Ctrl on X11`

---

**New file: `ww/linux/switch_keys.py`** (260 lines)

Core module with 3 responsibilities:

- **State detection** — checks 3 sources to determine whether the swap is active:
  - `setxkbmap -query` for the `ctrl:swapcaps` option
  - Live `xmodmap -pke` output to see if keycodes 37/66 are remapped
  - `~/.Xmodmap` file on disk for persistent config

- **Runtime apply/revert:**
  - `on` → runs `setxkbmap -option ctrl:swapcaps`
  - `off` → clears all options (`setxkbmap -option`), re-adds `terminate:ctrl_alt_bksp`, and resets xmodmap for keycodes 37 and 66

- **Persistence management:**
  - `--persist` on `on`: writes `~/.Xmodmap` with keycode-based swap (`keycode 66 = Control_L`, `keycode 37 = Caps_Lock`, clear/add Lock/Control) and appends the xmodmap load line to `~/.xprofile`
  - `--persist` on `off`: removes `~/.Xmodmap` and strips the swap-related lines from `~/.xprofile`
  - Without `--persist`, prompts interactively: "Also persist this setting across reboots?"

- **Argument parsing** via argparse with one optional positional arg (`on`/`off`) and a `--persist` flag

**Modified: `ww/linux/main.py`** (+3 lines)

- Added `switch-keys` to the help listing
- Added the import-and-call route: `elif subcmd == "switch-keys"` → `from ww.linux.switch_keys import run; run()`

**Modified: `ww/main.py`** (+1 line)

- Added `"  ww linux switch-keys  Swap Caps Lock and Left Control keys"` to the top-level help output

**Design choices:**
- Targets X11 only (errors out if `DISPLAY` or `XDG_SESSION_TYPE=x11` isn't set)
- Uses `setxkbmap` for runtime (lightweight, no Xmodmap reset needed) and `~/.Xmodmap` for persistence (autoloaded by most X11 display managers)
- Tracks both the `setxkbmap -query` option AND live `xmodmap` state, because the two can independently set the swap