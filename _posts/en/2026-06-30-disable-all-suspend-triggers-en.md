---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disable All Suspend Triggers
translated: false
type: note
---

Here's what's been done and what needs sudo access:

**Applied (no password needed):**
- `gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'` — ✅ AC idle will **not** auto-suspend

**Still needed (needs your sudo password):**

Lid close is handled by systemd-logind, which defaults to `HandleLidSwitch=suspend`. I need to create a config file to disable it:

```bash
sudo mkdir -p /etc/systemd/logind.conf.d
sudo tee /etc/systemd/logind.conf.d/disable-lid-suspend.conf > /dev/null <<'EOF'
[Login]
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
EOF
sudo systemctl restart systemd-logind
```

After that, neither lid close, idle timeout, nor power button will trigger a suspend that could hang on wake.