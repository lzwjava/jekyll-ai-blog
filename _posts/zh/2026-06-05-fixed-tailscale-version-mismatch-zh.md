---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Tailscale版本不匹配
translated: true
type: note
---

```
══════════════════════════════════════════
  Tailscale — 清理完毕
══════════════════════════════════════════

之前：
  Homebrew CLI:   v1.96.4  (旧版本，不匹配)
  GUI 应用:       v1.98.5  (运行中的 tailscaled)
  警告:          每次命令都显示版本不匹配

之后：
  单一安装:      v1.98.5  (GUI 应用 + 包装脚本)
  二进制文件:    /opt/homebrew/bin/tailscale → 包装脚本
                  → /Applications/Tailscale.app/Contents/MacOS/Tailscale
  守护进程:      GUI 应用的系统扩展 (无需 sudo)
  警告:         已消失 ✓

状态：
  lzw-mac → to:   8ms, 直连局域网, WireGuard 加密
  SSH:            公钥认证, 正常工作
══════════════════════════════════════════
```

位于 `/opt/homebrew/bin/tailscale` 的包装脚本会将所有参数转发至 GUI 应用的二进制文件，因此 `tailscale status`、`tailscale ping` 等命令均可正常使用——版本一致且无警告。