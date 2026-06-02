---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Jellyfin 设置与配置指南
translated: true
type: note
---

## 🎬 Jellyfin 设置指南

### 1. 访问 Web UI

- **LAN：** `http://192.168.1.36:8096`

在浏览器中打开它 — 设置向导将自动启动。

### 2. 首次运行向导

1. **语言与区域** — 选择您偏好的显示语言
2. **创建管理员账户** — 设置用户名和强密码
3. **添加媒体库** — 点击 **+ Add Media Library**，选择内容类型：
   - 🎥 **Movies** → 指向您的电影文件夹（例如 `/data/movies`）
   - 📺 **Shows** → 指向您的电视剧文件夹（例如 `/data/tv`）
   - 🎵 **Music** → 指向您的音乐文件夹（例如 `/data/music`）
4. **元数据语言** — 选择用于匹配海报/描述的语言
5. **远程访问** — 保持“Allow remote connections”启用
6. 完成！

### 3. 要检查的关键设置

| 设置 | 位置 | 推荐 |
|------|------|------|
| **Hardware Transcoding** | Dashboard → Playback | 启用 NVIDIA NVENC 或 VAAPI（已检测到您的 GPU ✅） |
| **Library Scan** | Dashboard → Libraries | 设置为更改时自动扫描 |
| **User Profiles** | Dashboard → Users | 为家庭成员创建单独的用户 |

### 4. 客户端应用

在任何设备上安装：

- **Android/Android TV** → [Jellyfin on Play Store](https://play.google.com/store/apps/details?id=org.jellyfin.mobile)
- **iOS/Apple TV** → [Jellyfin on App Store](https://apps.apple.com/app/jellyfin-mobile/id1480192618)
- **Desktop** → [Jellyfin Media Player](https://github.com/jellyfin/jellyfin-media-player)
- **Smart TV (Samsung/LG)** → 在您的 TV 应用商店搜索“Jellyfin”
- **Browser** → 直接使用 `http://192.168.1.36:8096`

### 5. 实用命令

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

### 6. 快速检查清单

- [ ] 完成首次运行向导
- [ ] 添加指向您内容文件夹的媒体库
- [ ] 在 Playback 设置中启用硬件加速
- [ ] 在手机/TV 上安装应用
- [ ] 设置远程访问（如果想要干净的域名，考虑使用 nginx 反向代理）

---

⚠️ 端口 8096 当前对互联网开放。请确保设置强管理员密码。需要我将其锁定为仅 LAN 访问，或设置带 HTTPS 的 nginx 吗？
