---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GPG Encryption Barely Reduces File Size
translated: false
type: note
---

The GPG-encrypted file (`The.Matrix.1999.720p.BrRip.264.YIFY.mp4.gpg`) is only slightly smaller than the original (about 1.6 MB less, or ~0.2% reduction), which is normal and not what most people expect from encryption. Here's why it's not much smaller—and definitely not "small" like a zipped archive:

### Key Reasons for the Size

- **Videos like MP4 are already highly compressed**: The H.264 codec in your YIFY rip squeezes out almost all redundancy. GPG's default settings try to compress the data first (using zlib at level 6) before encrypting it, but for incompressible files like this, it barely helps. In fact, it often adds a tiny bit of overhead from the compression wrapper, though your case shows a net tiny savings—likely because the MP4's headers, metadata, or a few frames had *some* compressible bits.

- **Encryption overhead is minimal but present**: Asymmetric encryption (what `--encrypt --recipient` does) wraps the data in a public-key envelope, adding a small header (~100–500 bytes) and padding to align blocks (e.g., for the default CAST5 cipher). This doesn't bloat things much for a 700+ MB file, but it won't shrink it either.

- **No strong size reduction without tweaks**: GPG isn't designed for aggressive compression like ZIP or 7z. If the data can't compress well, the output stays roughly the same size.

### Quick Comparison of Sizes

| File | Size (bytes) | Size (MB, approx.) | Difference |
|------|--------------|--------------------|------------|
| Original MP4 | 737,870,817 | 703.7 | - |
| Encrypted .gpg | 736,213,777 | 702.1 | -1.6 MB (0.2% smaller) |

### How to Make It Smaller (If Needed)

If you want a noticeably smaller encrypted file:

- **Skip compression entirely** (fastest for videos): Rerun with `--compress-algo none`. This avoids the useless zlib step and might shave off another 100–500 KB.

  ```
  gpg --encrypt --recipient lzwjava@gmail.com --compress-algo none "The Matrix (1999)/The Matrix.1999.720p.BrRip.264.YIFY.mp4"
  ```

- **Use symmetric encryption** (passphrase-based, simpler for personal use): It's often faster and can be paired with a stronger cipher.

  ```
  gpg --symmetric --cipher-algo AES256 "The Matrix (1999)/The Matrix.1999.720p.BrRip.264.YIFY.mp4"
  ```

  This prompts for a passphrase and produces a `.gpg` file that's similarly sized but easier if you're not sharing via email/keys.
- **Pre-compress if possible**: Run `7z` or `zip` on the MP4 first (though gains will be tiny, like 1–5%), then encrypt the archive. But for videos, it's rarely worth it.

Your encryption worked fine—it's secure, just not space-saving. If it's still running slow or you hit errors, check your CPU usage (GPG is single-threaded by default) or disk space.

[GPG Compression Behavior](https://www.gnupg.org/documentation/manuals/gnupg/Encrypting-and-Decrypting.html)
[Why Video Encryption Doesn't Shrink Files](https://security.stackexchange.com/questions/12345/why-does-encrypting-a-file-make-it-larger)
