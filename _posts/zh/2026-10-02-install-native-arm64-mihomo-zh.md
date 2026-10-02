---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 安装原生arm64 mihomo
translated: true
type: note
---

现在我清楚了。你的 Mac 是 **Apple Silicon (arm64)**，当前运行的二进制文件是旧的 amd64 alpha 版本，通过 Rosetta 转译运行。让我为你安装原生的 arm64 v1.19.32 版本。

以下是完整命令：

```bash
# 1. 停止当前的 mihomo
kill 17778

# 2. 下载并解压原生 arm64 二进制文件
cd /Users/lzwjava/bin
curl -L -o mihomo-darwin-arm64-v1.19.32.gz \
  https://github.com/MetaCubeX/mihomo/releases/download/v1.19.32/mihomo-darwin-arm64-v1.19.32.gz
gzip -d mihomo-darwin-arm64-v1.19.32.gz
chmod +x mihomo-darwin-arm64-v1.19.32

# 3. 删除旧的二进制文件（可选）
rm mihomo-darwin-amd64-v1-alpha-3035ae8

# 4. 使用现有配置启动新的 mihomo
./mihomo-darwin-arm64-v1.19.32 -d ~/.config/mihomo
```