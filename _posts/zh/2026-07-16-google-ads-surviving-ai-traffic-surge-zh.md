---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 谷歌广告应对AI流量激增
translated: true
type: note
---

问题：根据Cloudflare的报告，AI代理流量已超过网络流量的一半，那么现在Google Ads的收入情况如何？

回答：

有趣的是：**Google Ads的收入尚未崩溃。** AI代理/网络流量的转变确实存在，但Google的业务更具韧性，因为Google掌握的是**意图层**，而不仅仅是流量层。（[Cloudflare][1]）

当前情况：

| 领域                    | 状态         |
| ----------------------- | -------------- |
| Google搜索广告         | 仍在增长      |
| YouTube广告            | 仍在增长      |
| AdSense/展示网络       | 正在减弱      |
| 发布商流量             | 面临压力      |
| AI代理爬取网页         | 爆发式增长    |

Alphabet 2026年第一季度：

* 总收入：**1099亿美元**，同比增长22%
* Google服务收入：**896亿美元**，同比增长16%
* 搜索及其他广告收入：**同比增长19%**
* YouTube广告收入：**同比增长11%**

因此，短期答案是：

**Google Ads表现良好。**

但长期威胁是结构性的。

---

旧的网络循环：

```
人类
  ↓
Google搜索
  ↓
点击网站
  ↓
发布商获得广告收入
  ↓
Google获得广告收入
```

AI代理的未来：

```
人类
  ↓
AI代理
  ↓
生成答案
  ↓
可能不会访问网站
```

Cloudflare报告称，自动化代理/机器人现在产生的网络请求超过一半，与AI相关的爬取已成为爬虫流量的主要部分。（[Cloudflare][2]）

这会对以下方面造成冲击：

* SEO网站
* 联盟营销网站
* AdSense发布商
* 内容农场

因为到达页面的用户减少了。

---

但Google有一个巨大优势：

### 1. 搜索意图比原始流量更有价值

一个搜索的人：

```
用于LLM训练的最佳GPU
```

具有购买意图。

一个AI爬虫请求：

```
爬取所有GPU文章
```

几乎没有任何即时商业价值。

广告依附于**商业意图**，而非页面浏览量。

---

### 2. Google正在将广告融入AI答案中

当前的竞争格局是：

旧模式：

```
搜索页面
  |
  +-- 自然链接
  +-- 广告
```

新模式：

```
AI答案
  |
  +-- 赞助推荐
  +-- 交易
```

Google希望掌握代理界面。

他们已经在推出AI搜索产品的同时保持搜索收入增长。（[The Economic Times][3]）

---

### 3. 输家很可能是小型发布商

示例：

之前：

```
每月10万Google访客
每千次展示收入20美元

= 每月2000美元
```

AI摘要之后：

```
每月1万访客

= 每月200美元
```

但Google仍然可以展示：

```
用户：
"购买笔记本电脑"

Gemini/搜索AI：
"这里有3款笔记本电脑"

赞助：
戴尔
联想
亚马逊
```

Google捕获了收入。

---

我的预期：

**2026-2028年**

* Google搜索广告：可能稳定/增长
* AdSense生态系统：下滑
* SEO业务：重大颠覆
* AI商业代理：新的广告市场

打个比方：

> Google杀死了黄页。
> AI代理可能会杀死"10个蓝色链接"的网络。

但Google正在努力不成为受害者，它希望成为**代理操作系统 + 广告市场**。

参考文献：

* Alphabet 2026年第一季度财报
* Cloudflare代理互联网报告（[Cloudflare博客][4]）
* Google AI搜索广告策略（[The Economic Times][3]）

[1]: https://www.cloudflare.net/news/news-details/2026/Cloudflare-Allows-the-Agentic-Internet-to-Flourish-with-a-Simple-Philosophy-Your-Content-Your-Rules/default.aspx?utm_source=chatgpt.com "Cloudflare, Inc. - Cloudflare允许代理互联网蓬勃发展，核心理念：你的内容，你做主"
[2]: https://www.cloudflare.com/press/press-releases/2026/cloudflare-allows-the-agentic-internet-to-flourish-with-a-simple-philosophy-your-content-your-rules/?utm_source=chatgpt.com "Cloudflare允许代理互联网蓬勃发展，核心理念：你的内容，你做主 | Cloudflare"
[3]: https://m.economictimes.com/industry/services/advertising/google-bets-on-conversational-ai-to-drive-the-next-phase-of-search-advertising/articleshow/132394349.cms?utm_source=chatgpt.com "Google押注对话式AI，推动搜索广告下一阶段发展"
[4]: https://blog.cloudflare.com/agentic-internet-bot-report/?utm_source=chatgpt.com "内容独立日一周年：构建代理互联网的商业模式"