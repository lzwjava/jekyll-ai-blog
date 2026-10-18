---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英文英雄标题字号clamp
translated: true
type: note
---

完成。在 `style.css` 中添加了 `.hero__title:lang(en)` 规则，该规则仅在页面为英文时生效（i18n.js 设置 `html lang="en"`）：

```css
.hero__title:lang(en) {
  font-size: clamp(14px, 2.8vw, 30px);
  line-height: 1.3;
}
```

- **最大 30px**（桌面端）（中文为 56px）——约为 54%，不是 70%。我比你猜的 70% 调小了一些，因为在 39px（70%）时，第一行 "More than turning your ideas into shippable products —" 仍然约 1240px 宽，会换行成 3 行。在 30px 时，它可以在 1032px 的容器内一行放下，因此标题正好是 2 行。
- **`2.8vw`** 会在较小屏幕上按比例缩小，因此直到约 640px 宽度都能保持 2 行。
- 中文不受影响——它保留了大号的 `clamp(34px, 6vw, 56px)`。

如果你更想保留更大并接受 3 行，我可以把最大值调到约 39px。