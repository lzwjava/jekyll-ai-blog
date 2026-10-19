---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Newmine麦克风完全检测到
translated: true
type: note
---

已确认 — 你的 **Newmine** 麦克风已被完全检测到并可使用：

- **系统音频配置文件**：`Newmine`（MUSIC-BOOST），USB，48 kHz，1 声道
- **ffmpeg 输入设备**：在设备列表中显示为 `[1] Newmine`，与你的其他麦克风并列

它已经可以开始录音。例如，要从中录制 5 秒音频：

```bash
ffmpeg -f avfoundation -i ":1" -t 5 ~/test-newmine.wav
```

或者更长时间的测试：

```bash
ffmpeg -f avfoundation -video_size 1280x720 -i ":1" -t 10 ~/newmine-test.wav
```

需要我运行一次快速录音测试，以确认它能正常采集声音吗？
