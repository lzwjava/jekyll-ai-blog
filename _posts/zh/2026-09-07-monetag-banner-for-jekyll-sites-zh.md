---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Jekyll站点的Monetag横幅
translated: true
type: note
---

问题：我如何在我的网站上放置来自 Monetag 的**普通 Display Banner**？

答案：使用 Monetag 的 **Display Banner / Banner** 广告单元，并将生成的 JavaScript 片段嵌入到你的 Jekyll 布局中。

对于你的 Jekyll 站点，基本结构如下：

```html
<!-- Monetag display banner -->
<div class="ad-container">
  <script src="MONETAG_SCRIPT_URL"></script>
</div>
```

实际上，Monetag 会在你创建广告位后提供精确的 `<script>` 代码。你**不应该手动构造脚本 URL**。

### 对于 `lzwjava.com`

我会在文章中放置一个横幅，而不是让每次点击都变成广告：

```text
┌──────────────────────────────────────┐
│                                      │
│        Your article content          │
│                                      │
├──────────────────────────────────────┤
│             ADVERTISEMENT            │
│          [ Monetag banner ]          │
├──────────────────────────────────────┤
│                                      │
│        Continue reading...           │
│                                      │
└──────────────────────────────────────┘
```

对于 Jekyll，一种简洁的实现方式是：

```text
_includes/
    monetag-banner.html
```

```html
<div class="monetag-banner">
  <!-- paste Monetag's generated banner code here -->
</div>
```

然后在你想要展示广告的任何位置：

{% raw %}

```liquid
{% include monetag-banner.html %}
```

{% endraw %}

例如，在你的文章布局中：

{% raw %}

```text
_layouts/post.html

<header>...</header>

<article>
  {{ content }}
</article>

{% include monetag-banner.html %}
```

{% endraw %}

我**不**建议为此使用 OnClick/SmartLink。传统横幅的可预测性更强：用户看到广告，并且**只有有意的点击才会打开广告商页面**。

如果你给我看一张 Monetag 控制台 **Ad Formats / Create Zone** 页面的截图，我可以准确告诉你该选择哪个选项，以及将生成的代码放在哪里。
