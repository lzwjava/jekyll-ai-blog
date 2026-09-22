---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 帧提取并保存
translated: true
type: note
---

帧图像已提取并保存到磁盘。✅

## 结果

从 `IMG_2506.MOV` 中提取了 **13 帧**（约每 3 秒一帧，宽度缩小至 1280 像素）：

```
frames/
├── frame_001.jpg   (t = 0 s)
├── frame_002.jpg   (t = 3 s)
├── frame_003.jpg   (t = 6 s)
├── frame_004.jpg   (t = 9 s)
├── frame_005.jpg   (t = 12 s)
├── frame_006.jpg   (t = 15 s)
├── frame_007.jpg   (t = 18 s)
├── frame_008.jpg   (t = 21 s)
├── frame_009.jpg   (t = 24 s)
├── frame_010.jpg   (t = 27 s)
├── frame_011.jpg   (t = 30 s)
├── frame_012.jpg   (t = 33 s)
└── frame_013.jpg   (t = 36 s)
```

- 完整路径：`/mnt/data/gpu-diagonalize/frames/`
- 竖屏 1280×2276（手机垂直视频）

⚠️ 注意：我当前的模型无法在此会话中直接查看图像，但 **DeepSeek vision API 已经分析了这些帧**（报告中万用表的读数正是来自那里）。

如果需要，我可以对这 13 个已保存的帧重新运行视觉分析（而不是从视频中重新提取）——或者如果您告诉我需要查看哪些帧，我可以只将这些帧发送给 vision API 并提供聚焦读数。
