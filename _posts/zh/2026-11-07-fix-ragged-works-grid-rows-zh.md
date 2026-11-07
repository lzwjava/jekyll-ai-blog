---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复参差不齐的网格行
translated: true
type: note
---

我现在看清真正的问题了。在这个三列的作品展示网格中，卡片是**不一致的**：大多数卡片顶部都有 `.work__thumb` 图片，但以下**五个是纯文本**，既没有缩略图也没有 `.work__body` 容器：

- 趣标注
- 拼我 PingWorld
- vToken
- 小猿题库 · 游戏系列
- FOMOO

这就是为什么网格看起来不对——纯文本卡片较矮，没有填充满行，导致卡片跨列不对齐，行看起来参差不齐。修复方案分为两部分：

**1. 让每张卡片高度一致且结构规范**（添加缺失的 `.work__body` 容器并进行标准化），以及

**2. 修复网格 CSS**，使纯文本卡片拉伸到与带缩略图的卡片一致。

以下是修正后的网格 CSS（这是你的 CSS 中“不对劲”的部分）：

```css
/* 网格 */
.grid--3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  align-items: stretch;   /* 关键：一行中的所有卡片都拉伸到最高卡片的高度 */
}

/* 卡片 */
.card.work {
  display: flex;
  flex-direction: column;
  height: 100%;           /* 填满网格单元格 */
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 14px rgba(0, 0, 0, .08);
}

/* 主体扩展 / 将元数据推到底部，让纯文本卡片看起来大小一致 */
.card.work .work__body {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
}
.card.work .work__meta {
  margin-top: auto;       /* 将元数据行固定在卡片底部 */
}
```

**2a. 修复 5 个纯文本卡片**，使其使用与其余卡片相同的容器结构（将内容包裹在 `<div class="work__body">` 中），例如 PingWorld：

```html
<article class="card work" data-platform="miniapp">
  <div class="work__body">
    <div class="work__head">
      <h3>拼我 PingWorld</h3>
      <span class="tag tag--miniapp">小程序</span>
    </div>
    <p>人才与时间共享平台，集中分发设计、法务、财税、开发等服务需求。</p>
    <ul class="work__meta">
      <li><b>负责</b>设计、开发、上线</li>
      <li><b>历时</b>2 个月</li>
    </ul>
  </div>
</article>
```

（对趣标注、vToken、小猿题库·游戏系列、FOMOO 应用相同的容器结构。）

然而，我在这个仓库中**仍然找不到实际的文件**——用 `grep` 搜索 `趣标注`、`PingWorld` 和 `work__head` 都没有结果，所以这些卡片目前还不存在于这里的任何文件中。

请提供文件路径（或者这个作品展示网格所在的位置），我会直接应用这些修改。是哪种情况——我应该把这些卡片/测试内容重写进这个仓库中的一个正式文件，还是说这个页面在别的地方？
