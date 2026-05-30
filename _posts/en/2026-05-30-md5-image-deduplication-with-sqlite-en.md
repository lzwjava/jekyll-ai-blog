---
audio: false
generated: true
image: false
lang: en
layout: post
title: MD5 Image Deduplication with SQLite
translated: false
type: note
---

**Question:** Can we use MD5 to detect duplicate JPEG images by content hash, and add a deduplication table in SQLite?

**Answer:**

Yes, MD5 works fine for deduplication — it's not cryptographically secure but it's fast and collision-free enough for this use case. For JPEGs specifically, one gotcha: the raw bytes include EXIF metadata, so two photos with different metadata but identical pixels will have different MD5s. That's usually *what you want* (same file = same bytes), but worth knowing.

Here's the full implementation pattern:

```python
import hashlib
import sqlite3
from pathlib import Path

def md5_of_file(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def init_images_table(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            md5 TEXT UNIQUE NOT NULL,
            path TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def add_image(conn: sqlite3.Connection, image_path: str) -> int:
    md5 = md5_of_file(image_path)
    try:
        cursor = conn.execute(
            "INSERT INTO images (md5, path) VALUES (?, ?)",
            (md5, image_path)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        # UNIQUE constraint on md5 fired
        existing = conn.execute(
            "SELECT id, path FROM images WHERE md5 = ?", (md5,)
        ).fetchone()
        raise ValueError(
            f"Duplicate image: md5={md5} already exists as id={existing[0]} at {existing[1]}"
        )
```

Usage:

```python
conn = sqlite3.connect("mydb.sqlite")
init_images_table(conn)

try:
    image_id = add_image(conn, "/path/to/photo.jpg")
    print(f"Added image id={image_id}")
except ValueError as e:
    print(f"Error: {e}")
```

**Key design decisions:**

- `UNIQUE NOT NULL` on `md5` — the DB enforces the constraint, no need for a pre-check + insert race condition
- Chunked read (`65536` bytes) — handles large images without loading into RAM
- `IntegrityError` catch — cleaner than `SELECT` then `INSERT` (avoids TOCTOU)
- Store `path` in the images table so you can reference the original file

**If you want pixel-level dedup (ignoring EXIF):**

```python
from PIL import Image
import io

def md5_of_pixels(path: str) -> str:
    img = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")  # lossless, strips EXIF
    return hashlib.md5(buf.getvalue()).hexdigest()
```

Use `md5_of_pixels` when the same photo re-exported or re-shot with different EXIF should still be caught as a duplicate.

**For your records table**, just FK into images:

```sql
CREATE TABLE records (
    id INTEGER PRIMARY KEY,
    image_id INTEGER REFERENCES images(id),
    -- other fields
);
```