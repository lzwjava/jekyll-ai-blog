---
audio: false
generated: true
image: false
lang: en
layout: post
title: WhatsApp Web Image Downloader
translated: false
type: note
---

Done. Here's a summary of what was built:

---

## `ww image whatsapp` — created and ready

**Two files touched:**

1. `/Users/lzwjava/projects/ww/ww/image/whatsapp.py` (new, 195 lines)
2. `/Users/lzwjava/projects/ww/ww/main.py` (2 additions: help text + subcommand dispatch)

**How it works:**

- Runs AppleScript `do JavaScript` in Safari's front tab
- Finds the last `[data-testid="msg-container"]` on WhatsApp Web
- Grabs all `<img>` elements inside it
- Draws each onto a fresh `<canvas>`, then calls `canvas.toDataURL('image/jpeg')`
- This works for both `data:image/jpeg;base64,...` and `blob:https://...` sources because the blobs live on the same origin
- Returns the base64 data back through AppleScript
- Decodes and writes `.jpg` files to the output directory

**Usage:**

```
# Download images from the last message (saves to assets/images/cooking/)
ww image whatsapp

# Custom output directory
ww image whatsapp --dir ~/Desktop/wa-pics

# Open Safari and navigate to WhatsApp Web first (waits 8s for load)
ww image whatsapp --open
```

**Now you run it.** Make sure WhatsApp Web is open in Safari with the message visible, then:

```
ww image whatsapp
```

It will extract all images from the message you showed me — the 4 side-by-side images in the image album — and save them as `whatsapp-1.jpg` through `whatsapp-N.jpg` in `assets/images/cooking/`.
