---
audio: false
generated: true
image: false
lang: en
layout: post
title: Image Duplicate Detection Methods
translated: false
type: note
---

**Question:** Do tools like Tencent PC Manager, Google Photos, or Apple Photos use pixel-level MD5 (like `md5_of_pixels`) to detect duplicate photos?

**Answer:**

No — none of them use raw MD5 of pixels. That approach is too brittle for real-world photo deduplication. Here's what they actually do:

---

## The Problem with MD5 (even pixel-level)

| Scenario | MD5 of bytes | MD5 of pixels | Perceptual hash |
|---|---|---|---|
| Exact same file | ✅ match | ✅ match | ✅ match |
| Re-exported JPEG (recompressed) | ❌ miss | ❌ miss | ✅ match |
| Cropped slightly | ❌ miss | ❌ miss | ✅ match |
| Resized thumbnail vs original | ❌ miss | ❌ miss | ✅ match |
| Screenshot of a photo | ❌ miss | ❌ miss | ✅ match |
| Different lighting, same scene | ❌ miss | ❌ miss | ~match (tunable) |

JPEG is **lossy** — re-saving at even the same quality setting produces different bytes *and* different pixels. So `md5_of_pixels` still fails for the most common real-world duplicate case.

---

## What They Actually Use

### Google Photos
Uses **perceptual hashing + neural embeddings**:
- Perceptual hash (pHash) for near-identical detection
- CNN embedding vectors to cluster visually similar photos (e.g. same scene, burst shots)
- Deduplication is based on **visual similarity score**, not exact hash

### Apple Photos
Uses **pHash + metadata signals**:
- Detects duplicates introduced in iOS 16+ via `PHAssetCollectionSubtypeSmartAlbumDuplicates`
- Combines perceptual hash with timestamp, GPS, and camera model
- Groups burst photos separately

### Tencent PC Manager (腾讯管家) / similar tools
Simpler, file-focused approach:
- MD5 of **raw bytes** for exact duplicates
- pHash for similar image detection
- Some use file size + dimensions as a pre-filter before hashing (cheap early exit)

---

## Perceptual Hash — What It Actually Is

```python
# pip install imagehash pillow
import imagehash
from PIL import Image

def phash_of_image(path: str) -> imagehash.ImageHash:
    img = Image.open(path).convert("RGB")
    return imagehash.phash(img)  # 64-bit hash

def are_duplicates(path1: str, path2: str, threshold: int = 10) -> bool:
    h1 = phash_of_image(path1)
    h2 = phash_of_image(path2)
    distance = h1 - h2  # Hamming distance
    print(f"Hamming distance: {distance}")
    return distance <= threshold  # 0=identical, <10=very similar
```

**How pHash works internally:**
1. Resize image to 32×32
2. Convert to grayscale
3. Apply DCT (Discrete Cosine Transform) — same idea as JPEG compression
4. Take top-left 8×8 of DCT (low frequencies = structure, not noise)
5. Binarize: each of 64 bits = above/below mean
6. Compare with Hamming distance

This is why it survives JPEG recompression, mild crops, and resizes — the low-frequency structure is preserved.

---

## What to Use for Your SQLite Tool

For a personal duplicate detector, a two-stage approach is the right call:

```python
import hashlib
import imagehash
from PIL import Image

def md5_bytes(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def phash_str(path):
    img = Image.open(path).convert("RGB")
    return str(imagehash.phash(img))  # e.g. "f8e0c0a0b0d0e0f0"

def hamming_distance(h1: str, h2: str) -> int:
    # pHash strings are hex; compare bit by bit
    i1 = int(h1, 16)
    i2 = int(h2, 16)
    return bin(i1 ^ i2).count('1')
```

SQLite schema:

```sql
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    md5 TEXT UNIQUE,          -- exact dedup gate
    phash TEXT NOT NULL,      -- perceptual dedup
    path TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_phash ON images(phash);
```

Insert logic:

```python
def add_image(conn, path, phash_threshold=10):
    md5 = md5_bytes(path)
    ph = phash_str(path)

    # Stage 1: exact duplicate
    if conn.execute("SELECT 1 FROM images WHERE md5=?", (md5,)).fetchone():
        raise ValueError(f"Exact duplicate (md5={md5})")

    # Stage 2: perceptual duplicate (scan all phashes)
    for row in conn.execute("SELECT id, phash, path FROM images"):
        dist = hamming_distance(ph, row[1])
        if dist <= phash_threshold:
            raise ValueError(
                f"Similar image found (Hamming={dist}): id={row[0]} at {row[2]}"
            )

    conn.execute("INSERT INTO images (md5, phash, path) VALUES (?,?,?)", (md5, ph, path))
    conn.commit()
```

> For large collections, the linear phash scan is slow — use a vantage-point tree or store phash as a 64-bit integer and use BK-tree for sublinear search. But for <10k images, linear is fine.

---

## Summary

| Method | Exact copy | Re-exported JPEG | Resized | Cropped |
|---|---|---|---|---|
| MD5 bytes | ✅ | ❌ | ❌ | ❌ |
| MD5 pixels | ✅ | ❌ | ❌ | ❌ |
| pHash | ✅ | ✅ | ✅ | ~✅ |
| CNN embedding | ✅ | ✅ | ✅ | ✅ |

For your use case (SQLite-backed tool, personal photos): **MD5 bytes for exact + pHash for similar** is the right two-stage approach, same as what Tencent-style tools do under the hood.