---
audio: false
generated: true
image: false
lang: en
layout: post
title: Frames Extracted and Saved
translated: false
type: note
---

Frame images are extracted and saved on disk. ✅

## Result

**13 frames** extracted from `IMG_2506.MOV` (one every ~3 s, downscaled to 1280 px wide):

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

- Full path: `/mnt/data/gpu-diagonalize/frames/`
- Portrait 1280×2276 (phone vertical video)

⚠️ One note: my current model can't *view* images directly in this session, but the **DeepSeek vision API already analyzed these frames** earlier (that's where the multimeter readings in the report came from).

If you want, I can re-run the vision analysis on these exact 13 saved frames (instead of re-extracting from the video) — or if you tell me which frames to look at, I can send just those to the vision API and give you a focused readout.
