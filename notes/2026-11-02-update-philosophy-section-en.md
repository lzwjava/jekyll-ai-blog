---
audio: false
generated: true
image: false
lang: en
layout: post
title: Update Philosophy Section
translated: false
type: note
---

Done. Changes made:

**`index.html`** — Replaced the company philosophy block:

- Removed the `公司哲学` tag and `又快又好 —— 快，绝不牺牲质量` headline
- Replaced the 3 original cards (快是承诺 / 好是底线 / 自动化与AI的杠杆) with the 6 cards you provided (🧭 求真 · 随时协作, 👥 为真实用户而建, 🙌 尊重已有的成果, 🌱 以年为单位思考, 🤝 把客户当作协作者, 🤍 透明是产品的一部分)
- Kept the `philosophy__cards` class on the grid so the band's padding/alignment styling stays intact

**`i18n.js`** — Removed the now-unused translations for the deleted strings (`公司哲学`, `又快又好`, and the 3 old card headings/texts). The 6 new cards already had English translations in the dictionary.

⚠️ Note: the 6 cards now appear twice on the page — they're already in the "我们信奉什么" section above, and are now duplicated inside the philosophy band. If you'd rather not duplicate them, let me know and I can remove the original grid or delete the philosophy band entirely.
