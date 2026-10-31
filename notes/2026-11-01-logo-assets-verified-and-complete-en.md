---
audio: false
generated: true
image: false
lang: en
layout: post
title: Logo Assets Verified and Complete
translated: false
type: note
---

Everything checks out:
- **Icon PNGs**: content is perfectly centered (bbox 228×202 at offset +14,+27 inside 256×256 → center 128,128), with transparent frame around the near-white box — ideal for favicons/app icons.
- **Full logo PNGs**: proper aspect ratio, transparent outside the design.

Final result in `/Users/lzwjava/projects/employment-files/logo_deepcompute/`:

```
├── full/  (full logo with Chinese + English text)
│   ├── zhiwei_deepcompute_logo_256px.png   256×80
│   ├── zhiwei_deepcompute_logo_512px.png   512×161
│   ├── zhiwei_deepcompute_logo_1024px.png  1024×323
│   └── zhiwei_deepcompute_logo_2048px.png  2048×647
├── icon/  (left neural-network logo only, square)
│   ├── zhiwei_deepcompute_logo_icon_64px.png    64×64
│   ├── zhiwei_deepcompute_logo_icon_128px.png  128×128
│   ├── zhiwei_deepcompute_logo_icon_256px.png  256×256
│   ├── zhiwei_deepcompute_logo_icon_512px.png  512×512
│   └── zhiwei_deepcompute_logo_icon_1024px.png 1024×1024
├── zhiwei_deepcompute_logo_icon.svg  (icon-only source, viewBox "30 13 180 180")
├── full_clean.svg  (metadata-stripped full source for future renders)
├── zhiwei_deepcompute_logo.svg   (original)
└── zhiwei_deepcompute_logo.png   (original 2720×860)
```

The icon-only PNGs are square (64–1024px) so they work well for app icons, favicons, and avatars. Rendered from a dedicated icon SVG (left box + 3-node network with highlighted attention paths), not a crop, so line weights scale cleanly at every size.
