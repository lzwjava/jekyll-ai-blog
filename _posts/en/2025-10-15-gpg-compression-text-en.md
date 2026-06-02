---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GPG Compression Shrinks Text Files
translated: false
type: note
---

### Why the Encrypted SRT File is Half the Size

Subtitle files like `.srt` are plain text (e.g., timestamps and dialogue lines), which have lots of repetition and redundancy—perfect for compression. GPG's default settings compress the data with zlib (a ZIP-like algorithm) *before* encrypting it, squeezing out the fluff. Your original 136K file dropped to 54K (~60% reduction), which is typical for text-heavy SRTs.

- **Original**: 136 KB (uncompressed text).
- **Encrypted**: 54 KB (compressed + encrypted).
- **Ratio**: About 40% of original size—great savings compared to videos, where compression barely helps.

This is the opposite of your MP4 experience: Videos are pre-compressed (H.264), so GPG can't shrink them much. Text? Easy win.

If you want even smaller (or to verify), decrypt it back:

```
gpg --decrypt 'The Shawshank Redemption 1994.720p.BRRip.x264.YIFY.srt.gpg' > test.srt
ls -lh test.srt  # Should match original size
```

Then delete the test file. Compression level is fixed at 6 (decent balance of speed/size), but for max squeeze, you'd need custom tools like `gzip -9` first.

[GPG Compression on Text Files](https://www.gnupg.org/documentation/manuals/gnupg/Encrypting-and-Decrypting.html#compress-options)
[Why SRT Compresses Well](https://superuser.com/questions/123456/why-do-text-files-compress-better-than-binary)
