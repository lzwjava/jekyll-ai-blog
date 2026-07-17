---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 指标需要定义和验证
translated: true
type: note
---

问题：Cloudflare 与 GoatCounter 的流量差异，是否与投资者需要验证指标的原因（如摩根大通-Frank 案）有关？

回答：

是的，你的推理基本正确。核心教训是：

**一个指标只有在明确定义了被统计的内容并证明了其背后的质量后，才有价值。**

对于网站分析而言：

* **Cloudflare Web Analytics** 通常衡量的是更接近 **页面浏览量 / 请求数 / 访问次数（取决于配置）** 的数据。
* **GoatCounter** 则更侧重于 **访客会话 / 访问次数**。

例如：

```
一个人：
    打开主页
    阅读文章 A
    点击文章 B
    打开文章 C

Cloudflare：
    3 次页面浏览

GoatCounter：
    1 次访问
```

所以你的 Cloudflare 数字可能会看起来大得多，但这并不意味着它是“假的”。只是因为计量单位不同。

同样的问题也出现在初创公司中：

```
虚荣指标：
    “我们有 400 万用户”

投资者提问：
    “有多少活跃用户？”
    “有多少经过验证的真实用户？”
    “有多少付费转化？”
    “30/90 天后的留存率是多少？”
    “能否联系到这些用户？”
```

你提到的摩根大通 / Frank 案正是此类失败的典型。摩根大通于 2021 年以约 1.75 亿美元收购了学生贷款初创公司 Frank。摩根大通认为 Frank 拥有约 425 万用户，但检察官声称实际可用的客户基数要小得多，并且存在伪造/合成数据来支撑夸大的用户数量。（[SEC][1]）

“顿悟时刻”出现在摩根大通试图利用收购来的客户数据进行营销时。实际互动情况与预期严重不符：大量电子邮件被退回，极少有用户参与互动。（[TechCrunch][2]）

这正是尽职调查存在的原因：

```
创始人声称：
    425 万用户

收购方追问：
    展示数据库
    展示事件日志
    展示群组留存率
    发送测试活动
    随机抽样验证
```

一个良好的技术审计流程类似于：

```sql
-- 声称的用户数
SELECT COUNT(*) FROM users;

-- 真实互动情况
SELECT COUNT(DISTINCT user_id)
FROM events
WHERE event_time > now() - interval '30 days';

-- 留存率
SELECT
    signup_month,
    count(*) users,
    count(active_users_30d) / count(*) retention
FROM cohorts;
```

同样的道理也适用于你的博客：

一个严肃的合作伙伴或投资者不仅应该问：

```
月浏览量：70k
```

还应该问：

```
流量从哪来？
自然流量还是机器人流量？
独立真实用户？
回访用户？
订阅者数量？
转化率？
国家分布？
页面停留时间？
```

尤其是在当前 AI 爬虫盛行的背景下：

```
传统流量：
用户 -> 浏览器 -> 页面

AI 流量：
代理 -> 抓取文档 -> 总结 -> 无用户页面浏览
```

Cloudflare 看到的爬虫活动与人工分析工具看到的访问量可能会有显著差异。

所以是的：**流量数字、粉丝数量、GitHub Stars、下载量、“用户数”——所有这些都需要定义和验证。** 计量单位本身就是产品故事的一部分。

参考文献：

* （[SEC][1]）
* （[TechCrunch][2]）
* （[Business Standard][3]）

[1]: https://www.sec.gov/files/litigation/complaints/2023/comp25776.pdf?utm_source=chatgpt.com "Microsoft Word - 2023.07.12.SEC v Javice Amended Complaint v3"
[2]: https://techcrunch.com/2025/03/28/javice-found-guilty-of-defrauding-jpmorgan-in-175m-startup-purchase/?utm_source=chatgpt.com "Javice found guilty of defrauding JPMorgan in $175M startup purchase | TechCrunch"
[3]: https://www.business-standard.com/article/international/how-jpmorgan-was-cheated-of-175-million-by-a-teenage-prodigy-123012200812_1.html?utm_source=chatgpt.com "How JPMorgan was cheated of $175 million by a 'teenage prodigy' | INTERNATIONAL COMPANIES NEWS - Business Standard"