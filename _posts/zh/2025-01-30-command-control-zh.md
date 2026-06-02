---
audio: false
generated: false
image: false
lang: zh
layout: post
title: macOS 命令与控制
translated: true
type: post
---

## WiFi

```
networksetup -listallhardwareports
sudo networksetup -setairportpower en0 on
sudo networksetup -setairportpower en0 off
```

## 蓝牙

```
brew install blueutil
blueutil --power 0
blueutil --power 1
```

## 音量

```
# 将音量设置为 50%
osascript -e 'set volume output volume 50'

# 静音
osascript -e 'set volume with output muted'

# 取消静音
osascript -e 'set volume without output muted'
```
