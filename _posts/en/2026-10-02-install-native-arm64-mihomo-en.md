---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install native arm64 mihomo
translated: false
type: note
---

Now I have the full picture. Your Mac is **Apple Silicon (arm64)**, and the current binary is an old alpha amd64 version running through Rosetta. Let me install the native arm64 v1.19.32.

Here's the full command:

```bash
# 1. Stop current mihomo
kill 17778

# 2. Download and extract native arm64 binary
cd /Users/lzwjava/bin
curl -L -o mihomo-darwin-arm64-v1.19.32.gz \
  https://github.com/MetaCubeX/mihomo/releases/download/v1.19.32/mihomo-darwin-arm64-v1.19.32.gz
gzip -d mihomo-darwin-arm64-v1.19.32.gz
chmod +x mihomo-darwin-arm64-v1.19.32

# 3. Remove old binary (optional)
rm mihomo-darwin-amd64-v1-alpha-3035ae8

# 4. Start new mihomo with your existing config
./mihomo-darwin-arm64-v1.19.32 -d ~/.config/mihomo
```

Your config at `~/.config/mihomo/config.yaml` will be used as-is — nothing to change there. Want me to run these commands for you?
