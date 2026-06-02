---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: CSS垂直居中如今很简单
translated: true
type: note
---

这其实已经*不算*难事了（大约从2015年起），但人们仍**感觉**困难，因为在提供优秀解决方案之前，CSS经历了一段漫长而痛苦的发展史，期间充斥着各种半成品方案。这就是为什么大家对垂直居中都有心理阴影。

### 黑暗时代（Flexbox/Grid出现前）

1. **块级元素缺乏原生垂直居中能力**
   `margin: auto` 仅支持水平居中。垂直方向？毫无办法。当时的盒模型根本没有内置这种机制。

2. **那些年实际投入生产的糟糕方案：**

   ```css
   /* 1. 表格布局法（有效但语义糟糕） */
   .parent { display: table; }
   .child { display: table-cell; vertical-align: middle; }

   /* 2. 绝对定位+负边距（需固定高度） */
   .child {
     position: absolute;
     top: 50%;
     margin-top: -50px; /* 固定高度的一半 */
   }

   /* 3. 绝对定位+变形变换（2010-2015年最流行） */
   .child {
     position: absolute;
     top: 50%;
     left: 50%;
     transform: translate(-50%, -50%);
   }

   /* 4. 幽灵元素法（是的，有人真这么干） */
   .parent:before {
     content: '';
     height: 100%;
     display: inline-block;
     vertical-align: middle;
   }
   ```

这些方案都存在缺陷：或需要冗余标签，或无法适应动态内容，或如同黑魔法般难以维护。

### 现代纪元（2015年至今）——如今只需一两行代码

**Flexbox（2016年后的首选方案）：**

```css
.parent {
  display: flex;
  justify-content: center;    /* 水平居中 */
  align-items: center;        /* 垂直居中 */
  min-height: 100vh;          /* 或其他所需高度 */
}
```

搞定！支持未知高度、响应式布局，无需任何黑科技。

**Grid（同样简单）：**

```css
.parent {
  display: grid;
  place-items: center;        /* align-items + justify-items 的简写 */
  min-height: 100vh;
}
```

**甚至最新方案（2023+）：**

```css
.parent {
  display: grid;
  grid-template-rows: 1fr auto 1fr;  /* 也可直接用 margin 居中 */
}
.child { margin: auto; }
```

### 为何到2025年仍*感觉*困难？

1. **旧教程永不消亡**——搜索引擎仍大量展示十年前那些充斥黑科技的《15种垂直居中方案》
2. **先入为主的思维定式**——肌肉记忆和心理阴影难以消除
3. **边界场景依然存在**——按钮内文本用`line-height`还是`padding`居中，`inline-block`内的居中等
4. **Tailwind/Bootstrap的样式冲突**——它们有时会以奇怪方式覆盖`display`或高度设置

### 终极指南——2025年的标准答案

直接使用Flexbox或Grid。99%的场景下：

```css
.center-everything {
  display: flex;
  align-items: center;
  justify-content: center;
}
```

或

```css
.center-everything {
  display: grid;
  place-items: center;
}
```

如果你现在仍在纠结垂直居中，可能是：

- 维护无法使用flexbox的遗留项目（IE11时代）
- 把简单问题复杂化
- 看了过时的教程

垂直居中早在多年前就已不再困难——只是我们仍带着历史伤痕。放下执念，拥抱flexbox，重获自由。😭
