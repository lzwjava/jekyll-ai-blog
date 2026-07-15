---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI爬虫扼杀开源收入
translated: true
type: note
---

**问题：** 开源项目因文档访问量减少而收入下降，这一新闻内容是什么？它又如何与Cloudflare声称的代理流量巨大这一说法相关联？

**回答：**

是的，这是AI代理引发的最大经济变革之一。

核心问题：

**在AI代理出现之前：**

```
开发者
   |
谷歌搜索
   |
文档网站
   |
阅读文档
   |
可能点击：
- GitHub 星标
- 赞助
- 云服务
- 付费产品
```

网站会获得：

* 页面浏览量
* 广告收入
* 赞助
* 转化率
* 社区增长

---

**在AI编码代理出现之后：**

```
开发者
   |
Claude Code / Cursor / ChatGPT
   |
代理直接读取文档
   |
返回答案
   |
开发者再也不打开文档网站
```

文档依然被大量使用，但**人类访问消失了**。

Cloudflare的数据及相关文档分析都显示了这种转变。例如，Mintlify分析文档流量后发现，AI编码代理占到了约**45%的请求**，几乎与传统浏览器流量持平。（[Mintlify][1]）Cloudflare也报告称， AI相关的爬取和非人类流量正在改变开放网络的经济模式，AI爬虫消耗内容但并未将用户引导回来。（[Cloudflare博客][2]）

---

一个简单的例子：

旧的开源项目：

```
10万月访问量

10% 点击 GitHub Sponsors
1% 购买企业支持

有收入
```

新世界：

```
10万AI代理请求

0次人类页面浏览

0美元赞助转化
```

项目变成了：

```
有价值的数据源
        ↓
被AI使用
        ↓
创作者获得极少回报
```

这与以下情形类似：

* 搜索引擎出现后的报纸
* Stack Overflow出现后的论坛
* 谷歌摘要出现后的小博客

---

有趣的部分：

AI代理在技术上其实是**更有价值的用户**，但在经济上却更糟糕。

人类用户：

```
访问10个页面
慢慢阅读
可能购买
```

AI代理：

```
下载整个文档库
提取API细节
回答用户
离开
```

从服务器角度看：

```
请求数量 ↑
带宽消耗 ↑
获取的价值 ↓
```

Cloudflare明确将这种旧的交换模式描述为一种断裂：搜索引擎爬取内容并回馈访问者，而AI系统可以消费内容并回答用户，却不回馈任何流量。（[Cloudflare][3]）

---

这催生了新的商业模式：

### 1. 文档变成机器可读的API

公司不再提供：

```
docs.example.com
```

而是提供：

```
文档API
MCP服务器
代理端点
```

例子：

```
人类用户：
"如何使用Stripe webhook？"

AI代理：
调用Stripe MCP服务器

获取结构化答案

```

---

### 2. 按爬取付费

Cloudflare一直在推动一种模式，让内容所有者可以控制AI爬虫的访问权限，并可能需要获得补偿。（[Cloudflare][3]）

未来可能变成：

```
AI代理
    |
    | 支付小额费用
    ↓
文档提供方
```

类似于：

```
API调用
=
支付
```

---

### 3. 开源项目变现方式改变

项目可能会从：

```
GitHub星标
+
广告
+
文档流量
```

转向：

```
AI代理采用
+
企业许可证
+
托管服务
+
使用量API
```

例如：

```
Postgres扩展

以前：
人们阅读文档

以后：
代理推荐它

赢家：
提供托管版本的公司
```

---

更深层的意义：

互联网正在从：

```
人类可读的网络
```

转向：

```
机器可消费的网络

赢家可能不再是流量最大的网站。

他们可能是：
```

```
结构最优的知识
+
最佳的API
+
最好的代理集成
+
强大的品牌信任
```

对于开源开发者而言，这既是危险也是机遇：

危险：

```
AI蚕食你的文档流量
```

机遇：

```
数百万代理知道你的项目
```

下一个问题是：谁能捕获经济价值？是模型提供商，是基础设施层，还是原创作者。

参考文献：

* Cloudflare — 内容独立日 / 代理互联网经济学（[Cloudflare博客][2]）
* Cloudflare — AI爬虫与断裂的引荐经济学（[Cloudflare][3]）
* Mintlify — 文档流量中的AI代理分析（[Mintlify][1]）
* Cloudflare — 爬取到点击的差距分析（[Cloudflare博客][4]）

[1]: https://www.mintlify.com/blog/state-of-ai?utm_source=chatgpt.com "文档中代理流量的状态（2026年3月）"
[2]: https://blog.cloudflare.com/agentic-internet-bot-report/?utm_source=chatgpt.com "内容独立日，一年后：为代理互联网构建商业模式"
[3]: https://www.cloudflare.com/press/press-releases/2025/cloudflare-just-changed-how-ai-crawlers-scrape-the-internet-at-large/?utm_source=chatgpt.com "Cloudflare刚刚改变了AI爬虫大规模抓取互联网的方式；基于许可的方法为新的商业模式铺平了道路 | Cloudflare"
[4]: https://blog.cloudflare.com/crawlers-click-ai-bots-training/?utm_source=chatgpt.com "爬取到点击的差距：Cloudflare关于AI机器人、训练和引荐的数据"
