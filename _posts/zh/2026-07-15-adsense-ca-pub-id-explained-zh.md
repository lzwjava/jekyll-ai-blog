---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AdSense ca-pub ID 详解
translated: true
type: note
---

**问题：** 那个带有 `ca-pub-6168351539440296` 的 `adsbygoogle.js` 脚本是什么？

**答案：**

没错——这是 **AdSense**，与我们刚才讨论的正好相反：

- `ca-pub-6168351539440296` = 你的 **AdSense 发布商 ID**。
- 该脚本加载广告投放库，让 Google 将*其他广告主*的广告展示在你的页面上。你根据这些广告的展示/点击获得收入。
- 单独使用（就像 `gtag` 代码段一样），它只是加载库——并不会立即渲染广告。你仍然需要将一个**广告单元**放置在 HTML 中广告实际显示的位置：

```html
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-6168351539440296"
     data-ad-slot="<AD_SLOT_ID>"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
```

`data-ad-slot` 的值来自在 AdSense 后台创建“广告单元”（广告 → 按广告单元 → 展示广告 → 获取代码）。

**因此，现在你的网站上同时拥有这两个部分：**

| 标签 | 前缀 | 作用 | 资金流向 |
|---|---|---|---|
| `AW-18324816389` | Google Ads | 追踪你**购买**的广告带来的转化 | 你向 Google 付费 → 期望从你的产品中获得收入 |
| `ca-pub-6168351539440296` | AdSense | 展示你**获得报酬**托管的广告 | Google 向你支付分成 |

这两者是独立的，并不互斥——许多网站同时运行两者（通过 Ads 付费获取流量，通过 AdSense 将*其他*流量变现）。但请确认这确实是你的意图，因为在同一域名上同时运行两者意味着：有些访问者是你付费吸引来的（通过 Ads），然后你向他们展示*别人的*广告（AdSense），而不是将他们转化为你自己的客户——这通常是一种漏洞，而非策略，除非网站的整个商业模式是内容加广告收入（例如一个同时有自然流量和付费流量的博客/工具）。

这是哪个域名？是你的咨询网站，还是一个独立的内容资产（博客、笔记站、工具），其商业模式本身就是广告收入？