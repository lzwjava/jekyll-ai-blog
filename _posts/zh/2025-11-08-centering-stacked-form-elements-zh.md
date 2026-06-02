---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 使用Flexbox居中堆叠表单元素
translated: true
type: note
---

```css
.sort-container {
    display: flex;
    flex-direction: column; /* 改为垂直排列子元素 */
    align-items: center; /* 在垂直布局中水平居中子元素 */
    justify-content: center; /* 垂直居中整个容器 */
    gap: 10px;
    margin-bottom: 1rem;
}

.sort-container select {
    padding: 5px;
    font-size: 16px;
}

.sort-container .post-number {
    font-size: 16px;
}
```

### 实现原理

- **flex-direction: column**：将主轴方向从水平（行排列）改为垂直，使选择器和文章数量元素从上到下垂直堆叠
- **align-items: center**：保持子元素在水平方向居中对齐
- **justify-content: center**：使整个垂直堆叠的容器在父元素内垂直居中
- 同时优化了嵌套选择器语法（将选择器和文章数量选择器移出主代码块，假设它们是直接子元素——如需调整请根据实际情况修改）。现在垂直间距属性会在子元素之间创建垂直间隔。
