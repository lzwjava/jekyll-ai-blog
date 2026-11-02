---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复TruthSoft i18n品牌标识回归问题
translated: true
type: note
---

已完成。之前的 commit 直接在 HTML 中把品牌替换成了字面文本“TruthSoft”，这破坏了 i18n：中文站点是 source-first，而 `i18n.js` 在切换到英文时会精确替换“求真软件” → “TruthSoft”。由于这次字面替换，中文模式显示的是“TruthSoft”，并且 translation key 不再匹配。

我修正了：

- **index.html / portfolio.html** — 在中文源位置（页面 `<title>`、nav brand、footer）恢复了求真软件。i18n.js 已经将求真软件映射为 TruthSoft，因此英文模式会正确渲染英文名称。
- **TruthSoft** 现在只出现在真正面向英文的位置，这是正确的：
  - i18n EN dictionary（求真软件 → TruthSoft）、EN_TITLE、EN_META
  - portfolio 上逐页的 `i18nTitleEn` / `i18nMetaEn`
  - 装饰性的英文 about-section kicker（`TruthSoft · Think clearly. ...`）
  - meta description 保留两者：求真软件（TruthSoft）
- **scripts/build_cases.py** — 修复了生成的 portfolio EN meta 中过时的“Truth Software” → “TruthSoft”，然后重新生成了所有 cases/portfolio
- **README.md** — 将 header 和 about section 更新为 TruthSoft

已验证：任何地方都不再有“Truth Software”，并且中文源中的每个 nav/footer 在 index、portfolio 以及全部 12 个 case 页面中现在都显示为求真软件。

为新改动已提交为 `5b8b3b8`。
