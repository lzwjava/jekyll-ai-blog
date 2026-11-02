---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更新哲学部分
translated: true
type: note
---

完成。更改如下：

**`index.html`** —— 替换了公司理念区块：

- 移除了 `公司哲学` 标签和 `又快又好 —— 快，绝不牺牲质量` 标题
- 用你提供的 6 张卡片（🧭 求真 · 随时协作, 👥 为真实用户而建, 🙌 尊重已有的成果, 🌱 以年为单位思考, 🤝 把客户当作协作者, 🤍 透明是产品的一部分）替换了原来的 3 张卡片（快是承诺 / 好是底线 / 自动化与AI的杠杆）
- 在 grid 上保留了 `philosophy__cards` class，以便 band 的 padding/alignment 样式保持不变

**`i18n.js`** —— 移除了已删除的 strings（`公司哲学`、`又快又好` 以及 3 个旧卡片标题/文本）对应的、现已不再使用的翻译。这 6 张新卡片在 dictionary 中已有英文翻译。

⚠️ 注意：这 6 张卡片现在在页面上出现了两次——它们已经在上面的“我们信奉什么”区块中，现在又在 philosophy band 内重复出现。如果你不想让它们重复，请告诉我，我可以移除原来的 grid，或者完全删除 philosophy band。
