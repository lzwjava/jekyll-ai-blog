---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Transfer Photos from Mac to External Disk
translated: false
type: note
---

Here are the safest and most efficient ways to move (or copy) a large number of photos from the Photos app on macOS to an external/portable disk — especially when they’re synced from your iPhone via iCloud Photos.

### Method 1: Export originals (recommended – keeps full quality and metadata)

1. Connect your portable disk and make sure it has enough free space.
2. Open **Photos** app on your Mac.
3. Select the photos you want to move:
   - To select all: Press `Cmd + A`
   - To select many at once: Click the first photo → hold `Shift` → click the last (for a range) or hold `Cmd` and click individually.
   - Or go to Photos → All Photos (in the sidebar) to see everything in one list.
4. Go to the menu bar → **File → Export → Export Photos…** (not “Export Unmodified Originals” yet).
5. In the export dialog:
   - Choose **Photo Kind: JPEG** (or Current if you want the exact format)
   - Subfolder Format: **None** or **Moment Name** (optional)
   - File Name: **Use File Name** or **Sequential**
   - Check **Include Location Information**, **Include Keywords**, etc. if you want to keep metadata.
6. Click **Export**.
7. Choose your portable disk (or a folder on it) as the destination → **Export Originals** wait, no — actually for the absolute best quality and all metadata (including Live Photos, edits, etc.):

Better version → Use “Export Unmodified Originals” instead:

### Method 2: Export Unmodified Originals (best for full-resolution, untouched files)

1. Select all the photos you want (Cmd+A for everything).
2. Go to **File → Export → Export Unmodified Originals…**
3. Choose your external disk/folder.
4. Optionally check:
   - Include videos
   - Export IPTC as XMP (for metadata)
5. Click **Export Originals**.

This gives you the exact files that came from your iPhone, including HEIC/HEIF, ProRAW, Live Photo pairs (.mov + .jpg/heic), etc.

### After exporting — optional: delete from Photos library to free up Mac space

If you want to remove them from your Mac (but keep them in iCloud/iPhone):

1. After confirming everything is safely on the external disk,
2. Select the same photos in Photos app → right-click → **Delete Photos**
3. Then go to **Photos → Recently Deleted** → Delete All (or wait 30 days).

Because you’re using iCloud Photos, deleting them from your Mac only removes them from that Mac — they stay in iCloud and on your iPhone unless you delete them there too.

### Bonus: Drag-and-drop from Photos (quick but loses some organization)

You can also just select photos → drag them directly from Photos app to a folder on your external disk in Finder.
This creates copies with sequential names (IMG_0001, etc.) and keeps edits, but splits Live Photos and may not preserve all metadata perfectly.

### Summary – Recommended workflow

1. Connect external disk.
2. In Photos → Cmd+A (or select what you want).
3. File → Export → Export Unmodified Originals…
4. Export to a folder on the external disk.
5. Verify a few files open correctly.
6. (Optional) Delete the photos from your Mac’s library if you need the space.

That’s it — you now have all your original iPhone photos safely on the portable disk without losing quality or metadata.
