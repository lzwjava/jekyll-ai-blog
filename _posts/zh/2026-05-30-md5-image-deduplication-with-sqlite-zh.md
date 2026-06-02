---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于SQLite的MD5图像去重
translated: true
type: note
---

**问题：** 能否通过内容哈希使用MD5检测重复的JPEG图像，并在SQLite中添加去重表？

**回答：**

可以，MD5用于去重完全可行——它虽然不具备密码学安全性，但在此场景下速度快且碰撞概率极低。对于JPEG文件有一个注意点：原始字节包含EXIF元数据，因此两张像素相同但元数据不同的照片会产生不同的MD5值。这通常正是*你想要的*（相同文件=相同字节），但值得了解。

以下是完整的实现模式：

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

用法：

```python
conn = sqlite3.connect("mydb.sqlite")
init_images_table(conn)

try:
    image_id = add_image(conn, "/path/to/photo.jpg")
    print(f"Added image id={image_id}")
except ValueError as e:
    print(f"Error: {e}")
```

**关键设计决策：**

- `md5` 列设为 `UNIQUE NOT NULL` —— 数据库强制执行约束，无需预检+插入的竞态条件
- 分块读取（`65536` 字节） —— 处理大图像时不占用内存
- 捕获 `IntegrityError` —— 比先 `SELECT` 再 `INSERT` 更简洁（避免TOCTOU）
- 在图像表中存储 `path`，以便引用原始文件

**如果希望进行像素级去重（忽略EXIF）：**

```python
from PIL import Image
import io

def md5_of_pixels(path: str) -> str:
    img = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")  # lossless, strips EXIF
    return hashlib.md5(buf.getvalue()).hexdigest()
```

当同一张照片被重新导出或重新拍摄但带有不同EXIF时，使用 `md5_of_pixels` 仍能将其识别为重复。

**对于你的记录表**，只需使用外键引用 `images` 表：

```sql
CREATE TABLE records (
    id INTEGER PRIMARY KEY,
    image_id INTEGER REFERENCES images(id),
    -- other fields
);
```
