---
audio: false
generated: true
image: false
lang: en
layout: post
title: Head-Mounted Camera Travel Use Case
translated: false
type: note
---

**Question:** Should I get a head-mounted camera (like action camera or headwear with built-in camera) for travel? Is it good for taking lots of pictures and collecting data?

**Answer:**

It depends on your actual use case — let me be direct:

**If you mean action cameras (GoPro, DJI Osmo Action, Insta360):**
- **Good for:** Video-first workflows, hands-free vlogging, underwater/extreme sports, consistent stabilization
- **Bad for:** High-resolution stills, selective framing, bulk image collection for ML datasets
- Video codecs eat storage fast (100 Mbps = 45 GB/hour). If you're collecting images for training data, you'd need to extract frames, which degrades quality

**If you mean AR glasses or phone headmounts:**
- Gimmicky. Your smartphone takes better photos anyway. Headmounts = awkward viewing, limited battery, expensive for what you get

**For what you actually want (collect data + lots of pictures):**

1. **Smartphone (best for data collection)**
   - Better optics than action cameras
   - Pocket-sized, always with you
   - Easy batch processing: `exiftool`, `imagemagick`, Python scripts
   - Storage: 1TB external SSD, $50
   - Workflow: take 1000 photos → filter bad ones locally → upload compressed for training

2. **Mirrorless camera + fast lens** (if quality matters)
   - Sony A6400 (~$600) + 16mm lens
   - RAW + JPEG simultaneously for fast filtering later
   - Better resolution for fine details
   - Heavier, requires conscious framing (which is good for curating datasets)

3. **Head-mounted GoPro** (only if you want hands-free video)
   - Frame rate ≠ image diversity. Same angle = redundant training data
   - Extract frames → many duplicates → waste storage

**My take:** If you're collecting images for ML, a smartphone + external SSD + a simple Python script to batch-process/resize/filter is 10x more efficient than a head camera. You get better optics, flexibility, and your hands free to actually *navigate* new places.

What's the actual data collection goal? Are you training a vision model, building a map dataset, or just documenting travel?
