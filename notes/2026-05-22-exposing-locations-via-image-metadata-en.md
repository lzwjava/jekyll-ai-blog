---
audio: false
generated: true
image: false
lang: en
layout: post
title: Exposing Locations via Image Metadata
translated: false
type: note
---

**Question:** For anyone who publishes a blog or shares images online without stripping EXIF/GPS data, can a script like this trivially reveal their physical location?

**Answer:**

Yes, absolutely — and it's a well-known but underappreciated privacy vulnerability.

## How serious is this?

Your script is a clean implementation of what's essentially a one-liner threat. The EXIF GPS data embedded by smartphones is **precise to within a few meters** — enough to identify a home address, workplace, or daily routine. The metadata is invisible in the rendered image but fully readable by anyone who downloads the file.

```python
# What a smartphone typically embeds:
# GPSLatitude:  (37, 46, 29.4)   → 37.774833°
# GPSLongitude: (122, 25, 9.6)   → -122.419889°
# GPSAltitude:  15.3 meters
# GPSTimeStamp: 14:32:07 UTC
# GPSDateStamp: 2024:03:15
# GPSImgDirection: 247.5  (compass bearing the camera was pointing)
# GPSSpeed: 0.0 km/h  (you were stationary)
```

That's not just "somewhere in SF" — that's **your living room window, timestamped**.

## Attack surface

```
Blog/social post with embedded EXIF GPS
        ↓
curl -O https://example.com/photo.jpg
        ↓
python ww image exif ./downloads/
        ↓
Google Maps link → exact coordinates
```

At scale, you can crawl an entire blog's `<img>` tags, batch-download, and geolocate every photo in minutes. A motivated attacker can reconstruct a person's daily movement pattern from a year of blog posts.

## What platforms strip it, what don't

| Platform | Strips EXIF GPS? |
|---|---|
| Instagram | Yes (since ~2012) |
| Twitter/X | Yes |
| Facebook | Yes |
| WhatsApp | Yes (photos) |
| **Direct blog hosting (Jekyll, Hugo, etc.)** | **No — raw file served** |
| **GitHub Pages** | **No** |
| **Self-hosted WordPress (default)** | **No** |
| Imgur | Partially (strips on upload) |
| Flickr | Preserves by default (user opt-out) |

Your blog at `lzwjava.github.io` — if you've ever uploaded photos directly, those files are served raw. GitHub Pages is a static file server; it does zero metadata processing.

## How to defend

**Strip at upload time (ImageMagick):**

```bash
# Strip all metadata
mogrify -strip *.jpg

# Or with exiftool (more surgical)
exiftool -GPS:all= -overwrite_original *.jpg

# Strip GPS only, keep camera/copyright metadata
exiftool -GPSLatitude= -GPSLongitude= -GPSAltitude= -overwrite_original *.jpg
```

**Build it into your publishing pipeline:**

```bash
# Pre-commit hook or CI step
find ./static/images -name "*.jpg" -o -name "*.jpeg" | \
  xargs exiftool -GPS:all= -overwrite_original
```

**Or in Python, extend your own tool to also strip:**

```python
from PIL import Image
import piexif

def strip_gps(input_path, output_path):
    img = Image.open(input_path)
    exif_dict = piexif.load(img.info.get("exif", b""))
    exif_dict.pop("GPS", None)  # nuclear option for GPS IFD
    exif_bytes = piexif.dump(exif_dict)
    img.save(output_path, exif=exif_bytes)
```

## The subtler threat: metadata correlation

Even without GPS, EXIF contains:

- **Camera make/model** → narrows identity
- **Lens serial number** → unique identifier
- **Software version** → OS fingerprint
- **Timestamp** → timezone inference, routine mapping
- **Thumbnail** → sometimes retains original framing even after crop

Combined with other OSINT (writing style, domain registration, commit emails), EXIF is one more layer that makes full deanonymization easier.

## Bottom line

Your script is a legitimate OSINT tool. The privacy risk is real and systematic for anyone self-hosting a blog with photos taken on a smartphone. The fix is a one-time pipeline addition — `exiftool -GPS:all=` before publish — and it should be table stakes for any static site generator workflow.
