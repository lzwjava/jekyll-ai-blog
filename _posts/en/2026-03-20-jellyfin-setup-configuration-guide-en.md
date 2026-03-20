---
audio: false
generated: true
image: false
lang: en
layout: post
title: Jellyfin Setup and Configuration Guide
translated: false
type: note
---

## 🎬 Jellyfin Setup Guide

### 1. Access the Web UI

- **LAN:** `http://192.168.1.36:8096`

Open it in your browser — the setup wizard will launch automatically.

### 2. First-Run Wizard

1. **Language & Region** — pick your preferred display language
2. **Create Admin Account** — set a username and strong password
3. **Add Media Libraries** — click **+ Add Media Library**, choose the content type:
   - 🎥 **Movies** → point to your movies folder (e.g. `/data/movies`)
   - 📺 **Shows** → point to your TV shows folder (e.g. `/data/tv`)
   - 🎵 **Music** → point to your music folder (e.g. `/data/music`)
4. **Metadata Language** — pick for matching posters/descriptions
5. **Remote Access** — keep "Allow remote connections" enabled
6. Done!

### 3. Key Settings to Check

| Setting | Location | Recommendation |
|---------|----------|----------------|
| **Hardware Transcoding** | Dashboard → Playback | Enable NVIDIA NVENC or VAAPI (your GPU is detected ✅) |
| **Library Scan** | Dashboard → Libraries | Set to auto-scan on changes |
| **User Profiles** | Dashboard → Users | Create separate users for family members |

### 4. Client Apps

Install on any device:
- **Android/Android TV** → [Jellyfin on Play Store](https://play.google.com/store/apps/details?id=org.jellyfin.mobile)
- **iOS/Apple TV** → [Jellyfin on App Store](https://apps.apple.com/app/jellyfin-mobile/id1480192618)
- **Desktop** → [Jellyfin Media Player](https://github.com/jellyfin/jellyfin-media-player)
- **Smart TV (Samsung/LG)** → Search "Jellyfin" in your TV's app store
- **Browser** → Just use `http://192.168.1.36:8096`

### 5. Useful Commands

```bash
# Check status
sudo systemctl status jellyfin

# Restart
sudo systemctl restart jellyfin

# View logs
journalctl -u jellyfin -f

# Config & data directory
ls /var/lib/jellyfin/

# Update
sudo apt update && sudo apt upgrade jellyfin
```

### 6. Quick Checklist

- [ ] Complete first-run wizard
- [ ] Add media libraries pointing to your content folders
- [ ] Enable hardware acceleration in Playback settings
- [ ] Install the app on your phone/TV
- [ ] Set up remote access (consider nginx reverse proxy if you want a clean domain)

---

⚠️ Port 8096 is currently open to the internet. Make sure you set a strong admin password. Want me to lock it to LAN only, or set up nginx with HTTPS?