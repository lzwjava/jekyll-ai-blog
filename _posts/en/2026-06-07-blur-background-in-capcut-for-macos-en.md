---
audio: false
generated: true
image: false
lang: en
layout: post
title: Blur Background in CapCut for macOS
translated: false
type: note
---

Question: How do I set a blurred background/canvas in CapCut on macOS when my image doesn't fill the 4:3 aspect ratio?

Answer:

In CapCut macOS, when your media doesn't fill the canvas, you get letterboxing (black bars). To blur the background instead:

**Direct workflow:**

1. **Import your media** into a 4:3 project
2. **Select the video/image track** in the timeline
3. **Right-click** → look for **"Canvas"** or **"Background"** options (or check the Inspector panel on the right)
4. **Apply blur to background:**
   - Look for **Background Blur** or **Canvas Fill** option
   - Choose **Blur** as the fill type
   - Adjust blur intensity (usually a slider 0-100)

**Alternative if you don't see a direct option:**

1. Duplicate your image/video on a layer below
2. Scale it up to fill the entire 4:3 canvas (it will blur/deform, but that's fine)
3. Apply a **Gaussian Blur** filter to that layer (Effects → Blur → Gaussian Blur)
4. Set your original image on top with proper aspect ratio

**If CapCut doesn't expose this cleanly:**

The most reliable workaround — use **FFmpeg on your MacBook Air** to pre-process:

```bash
ffmpeg -i input.mp4 -vf "scale=640:480:force_original_aspect_ratio=decrease,pad=640:480:(ow-iw)/2:(oh-ih)/2,boxblur=10" output.mp4
```

This scales to fit 4:3, pads the sides, and applies a 10-strength blur. Adjust `boxblur=10` for intensity.

Then import the processed video into CapCut.

**CapCut version matters** — newer macOS builds have better canvas controls. Check **CapCut menu → About** to see your version. If you're on an older version, the FFmpeg path is faster than hunting UI.

---

Which approach matches your workflow better — using CapCut's native canvas blur, or preprocessing with FFmpeg?
