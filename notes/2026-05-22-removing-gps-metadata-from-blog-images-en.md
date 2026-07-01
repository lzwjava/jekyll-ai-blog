---
audio: false
generated: true
image: false
lang: en
layout: post
title: Removing GPS Metadata from Blog Images
translated: false
type: note
---

Here's a summary of what happened, with locations generalized:

---

## EXIF GPS Cleanup — jekyll-ai-blog assets

**Problem:** 48 out of 614 images in the blog assets tree contained embedded GPS coordinates in their EXIF metadata — revealing exact home address, frequent cooking locations, a north Guangdong road trip route, a Tibet/Lhasa visit, and a Shanghai trip.

**Root cause:** Smartphones tag every photo with GPS by default. When you run `magick -strip -quality 70` to compress, `-strip` removes EXIF — but only if you remember to include it. Many of these images were converted without `-strip`, or were original phone photos placed directly into the repo.

**What was done:**

1. Built `ww image exif` — a CLI scanner that reads EXIF GPS tags from images and reports coordinates + Google Maps links. Supports recursive scanning (`-r`) and listing all files (`--all`).

2. Added `--clean` mode that strips GPS EXIF in-place without re-encoding pixel data (uses `piexif` for JPEG byte-level surgery; Pillow fallback for other formats). All other EXIF (camera, orientation, date) is preserved.

3. Ran the full recursive scan + clean across `assets/`:

   | Metric | Value |
   | --- | --- |
   | Images scanned | 614 |
   | With GPS | 48 |
   | Cleaned | 48 |
   | Remaining GPS | 0 |

   **Locations found (generalized):**
   - ~22 images at home / apartment interior
   - ~16 images at a frequent cooking/kitchen location
   - 7 images along a north Guangdong highway route
   - 1 image in Lhasa, Tibet
   - 1 image in Shanghai
   - 3 images near an EV charging station

**Why this matters when sharing images online:**

- **Home address leak:** Every photo taken at home embeds your exact coordinates. Post a photo of your desk setup or a purchase unboxing, and anyone can find your apartment door.
- **Routine exposure:** Cooking photos, equipment photos, repair photos — all timestamped and geotagged, building a pattern of where you are and when.
- **Travel tracking:** Road trip photos create a precise itinerary with timestamps and coordinates. Vacation photos tell people exactly when your home is empty.
- **Platforms don't always strip EXIF:** Some do (Twitter/X strips it, WhatsApp strips it on send), but many don't — especially self-hosted blogs, forums, GitHub repos, and direct file uploads. Never rely on the platform to protect you.
- **Metadata is invisible to the naked eye:** You see a photo of food. The file carries your kitchen's latitude/longitude, device model, and the exact second you pressed the shutter.

**What to do:**

1. **Check before sharing:** `ww image exif /path/to/images -r` scans everything.
2. **Strip GPS:** `ww image exif /path/to/images -r --clean` removes it.
3. **Batch workflow:** Run `magick input.heic -strip -quality 70 output.jpg` when converting phone photos — `-strip` drops all metadata at conversion time.
4. **Verify:** Always run the exif scan again after processing to confirm zero GPS hits.

The 48 images in this repo are now clean.
