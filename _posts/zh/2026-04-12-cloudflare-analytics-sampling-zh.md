---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cloudflare分析采样机制解析
translated: true
type: note
---

问题：Cloudflare 中的“按请求的 10% 采样”是什么意思？为什么所有路径计数都以 0 结尾？

答案：

当 Cloudflare 显示 **“按请求的 10% 采样”** 时，意味着：

* Cloudflare **不会统计每个请求**
* 它只**记录大约 10% 的流量**
* 然后**将数字按比例放大**以估算总量

示例：

* 实际请求数 = 53,270
* Cloudflare 采样 10% → 收集 ≈ 5,327 个请求
* 然后乘以 10 → 报告 **≈ 53,270 (估算值)**

Cloudflare 明确指出，当采样率为 10% 时，它**对一部分数据进行采样并乘以相应倍数以估算完整数据集**。 ([Cloudflare 文档][1])

---

## 为什么所有数字都以 0 结尾

没错 —— 这正是因为 **10% 采样**。

如果 Cloudflare：

* 每 10 个请求中采样 1 个
* 然后将结果乘以 **10**

返回的所有数值通常会是：

* **10** 的倍数
* 有时会**进行舍入**
* 有时略有偏差

因此你会看到：

```
430
290
210
170
150
130
120
```

而不是：

```
427
291
213
168
152
131
119
```

因为**实际计数是估算值**，而非精确值。

---

## 重要提示：你的数据是近似值

这会影响：

* 来源网站 (Referers)
* 路径
* 国家/地区
* 用户代理
* 爬虫程序
* 等

但通常不影响：

* 总请求数
* 带宽
* 顶级指标

Cloudflare 这样做是因为你的站点可能拥有**数百万个事件**，采样能让分析数据快速加载。 ([Cloudflare 文档][2])

---

## 如何解读你的截图

你的数据意味着：

* `None (direct)` → 约 53k 次直接访问 (估算值)
* `cn.bing.com` → 约 750 次访问 (实际可能约 734–766)
* `/upgrade-claude-code-en` → 约 430 次访问 (估算值)

这些数据**趋势上是准确的**，而非精确。

---

## 何时会发生采样

Cloudflare 在以下情况使用采样：

* 流量很高时
* 查询很复杂时
* 选择了较长时间范围时
* 涉及多个维度时 (来源 + 路径 + 用户代理)

然后它会切换到：

* 100% 数据 (流量较小)
* 10% 数据 (中等流量)
* 1% 数据 (流量非常大)

---

## 总结

是的：

* "sample by 10%" → Cloudflare 仅查看 1/10 的流量
* 数字是**估算值**
* 数值通常**以 0 结尾**
* 你的理解是正确的

你的分析数据**方向上是正确的**，但并不精确。

[1]: https://developers.cloudflare.com/analytics/graphql-api/sampling/?utm_source=chatgpt.com "Sampling · Cloudflare Analytics docs"
[2]: https://developers.cloudflare.com/analytics/sampling/?utm_source=chatgpt.com "Understanding sampling in Cloudflare Analytics · Cloudflare Analytics docs"
