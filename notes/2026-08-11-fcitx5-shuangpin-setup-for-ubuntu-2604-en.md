---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fcitx5 Shuangpin Setup for Ubuntu 26.04
translated: false
type: note
---

## Your system

- **Ubuntu 26.04 LTS (Resolute Raccoon)**, GNOME on **Wayland**
- IBus installed as default but no `ibus-pinyin`
- Fcitx5 packages **are available** in the repos (5.1.19)
- ⚠️ Note: `fcitx5-configtool` no longer exists as a package on 26.04 — it's **`fcitx5-config-qt`** now (the GUI Config Tool is still launched via `fcitx5-configtool`)

## Install (Option 1: Fcitx5 + Shuangpin)

I wrote a script at `/tmp/install-fcitx5-shuangpin.sh`. Run it in your terminal:

```bash
bash /tmp/install-fcitx5-shuangpin.sh
```

Or manually:

```bash
sudo apt update
sudo apt install fcitx5 fcitx5-chinese-addons fcitx5-config-qt
im-config -n fcitx5
```

Then **log out and log back in** (required — Wayland sessions can't hot-swap input frameworks).

## Configure 双拼

1. Launch **Fcitx 5 Configuration** (app menu, or run `fcitx5-configtool`)
2. **Add Input Method → 汉语 → Pinyin**
3. Select the Pinyin entry → click the gear → **双拼 (Shuangpin)** tab
4. Pick your scheme — 小鹤双拼 (Xiaohe) is the most popular; 微软双拼 (Microsoft) and 自然码 (Ziranma) are also there
5. Toggle on **双拼模式** (Shuangpin mode); optionally keep 全拼 fallback

You'll get a tray icon; `Ctrl+Space` toggles Chinese/English. In Shuangpin mode `xiaoming` → `xm`.

## Notes / pitfalls on your setup

- **Wayland**: Fcitx5 works natively via `text-input-v3`. Skip the `GTK_IM_MODULE/QT_IM_MODULE` exports unless some app (rare) doesn't receive input — only add them if you hit issues.
- **IBus conflict**: I kept ibus installed (GNOME relies on it for its own shortcuts) but it's masked from autostart. If you see double preedit, `sudo apt remove ibus` fixes it definitively.
- **Rime (Option 3)**: available as `fcitx5-rime` — install later with `sudo apt install fcitx5-rime` if you want 小鹤双拼 with full custom dictionaries.

Need help with a specific 双拼 scheme layout (小鹤 vs 微软 key mapping), or want me to pre-configure `~/.config/fcitx5/conf/pinyin.conf` after you've logged in once?