---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 禁用所有暂停触发器
translated: true
type: note
---

以下是已完成的操作和需要 sudo 权限的部分：

**已应用（无需密码）：**
- `gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'` — ✅ 交流电源空闲时**不会**自动挂起

**仍需操作（需要您的 sudo 密码）：**

合盖由 systemd-logind 处理，默认配置为 `HandleLidSwitch=suspend`。我需要创建一个配置文件来禁用此功能：

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

执行后，无论是合盖、空闲超时还是电源按钮，都不会触发可能导致唤醒时卡死的挂起操作。