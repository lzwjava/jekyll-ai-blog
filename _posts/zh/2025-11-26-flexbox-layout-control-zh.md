---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 响应式弹性盒布局控制
translated: true
type: note
---

正确答案是 **A. flex-direction**

要让弹性容器在大屏幕上采用行布局，在小屏幕上切换为列布局，您需要在**媒体查询**中更改 `flex-direction` 属性。

示例：

```css
.container {
  display: flex;
  flex-direction: row; /* 大屏幕上的默认值 */
}

@media (max-width: 768px) {
  .container {
    flex-direction: column; /* 在小屏幕上切换为列布局 */
  }
}
```

其他选项错误的原因说明：
- **B. flex-wrap** – 控制项目是否换行，而不是主轴方向（行与列）
- **C. media query** – 这是在不同屏幕尺寸下应用更改的*技术*，但它不是 CSS *属性*。实际更改的属性是 `flex-direction`
- **D. grid-template** – 这属于 CSS Grid 布局，而非 Flexbox

因此，虽然您需要媒体查询（C）来触发更改，但实际控制项目按行或列排列的**属性**是 **flex-direction (A)**。

正确答案：**A**
