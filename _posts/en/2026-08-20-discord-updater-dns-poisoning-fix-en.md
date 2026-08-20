---
audio: false
generated: true
image: false
lang: en
layout: post
title: Discord Updater DNS Poisoning Fix
translated: false
type: note
---

Everything checks out now. Final confirmation:

- **Manifest fetch** over raw TUN (no proxy env, exactly Discord's updater behavior): `HTTP 200` from fake-IP `198.18.0.4`
- **Full 171 MB update download** from Discord's CDN (`stable.dl2.discordapp.net` → `198.18.0.13`): `HTTP 200`

The updater log shows only old failures (timestamps **20:39–20:40**, before the DNS fix). It isn't retrying anymore — but note those are all *pre-fix* entries.

## What was wrong (it took two layers)

1. **Root cause:** Discord's updater (`updater.node`) is a **raw socket** that ignores the macOS proxy → it needed TUN.
2. **Second layer (found after TUN):** The system router DNS (`192.168.1.1`) was **poisoning** `updates.discord.com` → **Meta IP `157.240.6.35`**. Because mihomo got a *real* poisoned IP instead of its own fake-IP, TUN couldn't map the connection back to the hostname, so it never routed through your Hysteria2 node. Connection terminated with `-9806 (connection closed via error)`.

## Fixes applied

1. **TUN enabled** in `~/.config/mihomo/config.yaml` (`tun.enable: true`, `stack: gvisor`, `any:53` DNS hijack) — you restarted mihomo, and it's now **`enable: True` on `utun4`**, with traffic correctly hitting your **`My Hysteria2 2`** node.
2. **System DNS → `127.0.0.1`** (mihomo) on the **Wi-Fi** service (was set to router handling DNS):

   ```
   networksetup -setdnsservers Wi-Fi 127.0.0.1
   ```

   Now `updates.discord.com` resolves to mihomo's **fake-IP** (`198.18.0.4`) instead of the poisoned Meta IP.

## Next step for you

Those `-9806` errors are all from **before** the DNS fix. Now that resolution goes through mihomo, **fully quit Discord and relaunch it** (⌘Q, not just close the window) so its updater issues a fresh check. It should now complete and download the update.

Caveat: pointing Wi-Fi DNS to `127.0.0.1` makes **everything depend on mihomo being up** for name resolution. That's the intended trade-off for reliable proxying; just restart mihomo before using the network. If you'd rather scope it, I can leave it as-is (recommended for your setup) — let me know once you've relaunched Discord and whether the update completes.
