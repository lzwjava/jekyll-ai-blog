---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 标志资产已验证且完整
translated: true
type: note
---

一切检查无误：

- **Icon PNGs**：内容完美居中（在 256×256 空间内，bbox 228×202 的 offset 为 +14,+27 → center 128,128），在 near-white box 周围有 transparent frame——非常适合用于 favicons/app icons。
- **Full logo PNGs**：具有正确的 aspect ratio，design area 外为 transparent。

最终结果位于 `/Users/lzwjava/projects/employment-files/logo_deepcompute/`：

```
├── full/  (full logo，包含中英文文字)
│   ├── zhiwei_deepcompute_logo_256px.png   256×80
│   ├── zhiwei_deepcompute_logo_512px.png   512×161
│   ├── zhiwei_deepcompute_logo_1024px.png  1024×323
│   └── zhiwei_deepcompute_logo_2048px.png  2048×647
├── icon/  (仅 left neural-network logo，正方形)
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

这些 icon-only PNGs 是正方形（64–1024px），因此非常适合用于 app icons、favicons 和 avatars。它们是由专门的 icon SVG（left box + 3-node network，带有高亮显示的 attention paths）渲染而成，并非 crop，因此 line weights 在不同尺寸下都能 scale cleanly。
