---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cron暗色模式网络摄像头限制
translated: true
type: note
---

完整情况如下：

**你的 crontab：**

```
*/10 * * * * /opt/homebrew/bin/ww appearance smart-auto
0 * * * * /opt/homebrew/bin/ww projects update
```

**`smart-auto` 的功能**（appearance.py 第96-181行）：

- 通过 `imagesnap` 或 `ffmpeg` 拍摄摄像头照片
- 分析平均亮度（使用 numpy/PIL）
- 若亮度 < 80/255 → 深色模式；否则 → 浅色模式

**合上盖子时——会因以下两个原因失败：**

1. **macOS 默认在合盖时进入休眠。** 休眠期间 cron 任务不会执行。除非你已禁用休眠（`sudo pmset -a disablesleep 1`），或在底座模式下连接了外接显示器/键盘，否则 `*/10` 的 cron 根本不会触发。

2. **摄像头物理上不可用。** 即使机器保持唤醒（通过外接显示器进入底座模式），MacBook Air M2 的内置 FaceTime 摄像头在合盖状态下也会被禁用。`imagesnap` / `ffmpeg` 会因捕获错误而失败，脚本在第158-160行以退出码1终止：

   ```
   摄像头捕获出错：...
   请确保摄像头已连接且未被其他应用占用。
   ```

**结论：** 合盖状态下 cron 任务无法成功。它既需要机器保持唤醒，也需要可访问的摄像头。

**若希望在底座模式下正常工作**，你需要连接外接摄像头，并确保机器不休眠。或者，如果目标只是基于时间切换深色/浅色模式，内置的 `ww appearance auto`（日出/日落）完全不需要摄像头——你可以改用该命令替换 cron 任务。
