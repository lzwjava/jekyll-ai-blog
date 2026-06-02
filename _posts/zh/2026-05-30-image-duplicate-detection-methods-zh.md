---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 图像重复检测方法
translated: true
type: note
---

**问题：** 像腾讯电脑管家、Google Photos 或 Apple Photos 这类工具是否使用像素级 MD5（如 `md5_of_pixels`）来检测重复照片？

**答案：**

不——它们都不使用原始像素 MD5。这种方法对于现实中的照片去重来说过于脆弱。以下是它们实际采用的方法：

---

## MD5（甚至像素级）存在的问题

| 场景 | 字节 MD5 | 像素 MD5 | 感知哈希 |
|---|---|---|---|
| 完全相同的文件 | ✅ 匹配 | ✅ 匹配 | ✅ 匹配 |
| 重新导出的 JPEG（重新压缩） | ❌ 错过 | ❌ 错过 | ✅ 匹配 |
| 轻微裁剪 | ❌ 错过 | ❌ 错过 | ✅ 匹配 |
| 缩放后的缩略图 vs 原图 | ❌ 错过 | ❌ 错过 | ✅ 匹配 |
| 照片的屏幕截图 | ❌ 错过 | ❌ 错过 | ✅ 匹配 |
| 不同光照、相同场景 | ❌ 错过 | ❌ 错过 | ~匹配（可调） |

JPEG 是**有损**的——即使以相同质量设置重新保存，也会产生不同的字节*和*不同的像素。因此，`md5_of_pixels` 对于最常见的现实重复情况仍然失败。

---

## 它们实际使用的方法

### Google Photos
使用**感知哈希 + 神经网络嵌入**：
- 感知哈希（pHash）用于近乎相同的检测
- CNN 嵌入向量用于聚类视觉上相似的照片（例如相同场景、连拍）
- 去重基于**视觉相似度分数**，而非精确哈希

### Apple Photos
使用 **pHash + 元数据信号**：
- 自 iOS 16+ 起通过 `PHAssetCollectionSubtypeSmartAlbumDuplicates` 检测重复项
- 将感知哈希与时间戳、GPS 和相机型号结合
- 单独分组连拍照片

### 腾讯电脑管家 / 类似工具
更简单、以文件为中心的方法：
- 对**原始字节**进行 MD5 以查找精确重复
- 使用 pHash 检测相似图像
- 部分工具在哈希前先用文件大小 + 尺寸作为预过滤器（廉价提前退出）

---

## 感知哈希——它究竟是什么

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
    distance = h1 - h2  # 汉明距离
    print(f"Hamming distance: {distance}")
    return distance <= threshold  # 0=完全相同, <10=非常相似
```

**pHash 内部工作原理：**
1. 将图像缩放到 32×32
2. 转换为灰度图
3. 应用 DCT（离散余弦变换）——与 JPEG 压缩原理相同
4. 取 DCT 左上角 8×8 区域（低频 = 结构，而非噪声）
5. 二值化：64 位中的每一位 = 高于/低于均值
6. 通过汉明距离比较

这就是为什么它能承受 JPEG 重新压缩、轻微裁剪和缩放——低频结构得以保留。

---

## 你的 SQLite 工具应使用什么

对于个人重复检测器，两阶段方法是正确的选择：

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
    return str(imagehash.phash(img))  # 例如 "f8e0c0a0b0d0e0f0"

def hamming_distance(h1: str, h2: str) -> int:
    # pHash 字符串是十六进制；逐位比较
    i1 = int(h1, 16)
    i2 = int(h2, 16)
    return bin(i1 ^ i2).count('1')
```

SQLite 模式：

```sql
CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    md5 TEXT UNIQUE,          -- 精确去重闸门
    phash TEXT NOT NULL,      -- 感知去重
    path TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_phash ON images(phash);
```

插入逻辑：

```python
def add_image(conn, path, phash_threshold=10):
    md5 = md5_bytes(path)
    ph = phash_str(path)

    # 阶段 1：精确重复
    if conn.execute("SELECT 1 FROM images WHERE md5=?", (md5,)).fetchone():
        raise ValueError(f"Exact duplicate (md5={md5})")

    # 阶段 2：感知重复（扫描所有 phash）
    for row in conn.execute("SELECT id, phash, path FROM images"):
        dist = hamming_distance(ph, row[1])
        if dist <= phash_threshold:
            raise ValueError(
                f"Similar image found (Hamming={dist}): id={row[0]} at {row[2]}"
            )

    conn.execute("INSERT INTO images (md5, phash, path) VALUES (?,?,?)", (md5, ph, path))
    conn.commit()
```

> 对于大型集合，线性 phash 扫描较慢——可使用 vantage-point 树或将 phash 存储为 64 位整数，并使用 BK 树进行次线性搜索。但对于少于 10k 张图片，线性扫描已经足够。

---

## 总结

| 方法 | 精确副本 | 重新导出的 JPEG | 缩放 | 裁剪 |
|---|---|---|---|---|
| MD5 字节 | ✅ | ❌ | ❌ | ❌ |
| MD5 像素 | ✅ | ❌ | ❌ | ❌ |
| pHash | ✅ | ✅ | ✅ | ~✅ |
| CNN 嵌入 | ✅ | ✅ | ✅ | ✅ |

针对你的用例（基于 SQLite 的工具，个人照片）：**精确重复使用 MD5 字节，相似重复使用 pHash** 是合适的两阶段方法，与腾讯类工具底层的做法一致。
