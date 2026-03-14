---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 销售 Claude VPN 服务违反法律
translated: true
type: note
---

**问题：** 在闲鱼（Xianyu）上向中国个人用户销售 Claude/OpenClaw 部署服务——同时帮助用户安装 VPN/代理工具如 Clash 或 Hysteria——是否违反法律？

**回答：**

## 简短回答：是的——此商业模式同时违反多项法律

此场景将**至少三种独立的法律风险**叠加在一起。我们逐一分解。

---

## 风险层 1：销售 VPN/代理设置（Clash / Hysteria）

这是最严重且最直接可起诉的风险层。

根据现行法律，VPN 提供商可根据最高人民法院关于计算机犯罪的指导方针在中国被起诉。以严重扰乱电信市场的方式提供 VPN 属于非法经营罪。

即使是收费帮助个人用户安装未经授权的代理软件，也算作“提供”VPN 服务——这是非法的。确有此类规模的真实起诉案例：

- Wu Xiangyang 被罚款 50 万元（7.6 万美元）并判监 5 年半，因为未经适当许可运营 VPN 服务，他提供软件和修改路由器帮助人们访问中国受限的外国网站。他售卖给大约 8000–13000 名用户——但法律没有最低用户门槛。
- 一名上海开发者因向数百人销售 VPN 服务而被判缓刑，罪名与黑客相关。
- 另一名个人因专门销售 VPN 应用而被判监 9 个月。

**一个月 500 名用户并非小规模——这显然是商业活动**，中国法院已在远更小的规模上起诉过人员。

---

## 风险层 2：在闲鱼上转售 Claude/AI API 访问权

这是灰色市场活动，虽然已广泛存在，但也日益成为打击目标：

镜像站点（中转站）使用支持区域的电话号码和支付方式从 Anthropic 官方 API 平台采购模型访问权，然后转售给中国用户。从镜像站点获得的“直连”Claude Pro 账户每月低至 65 元人民币，而转售 API 通常以官方价格的 70–90% 折扣出售。

从 Anthropic 角度，这是明显的**服务条款违反**。Anthropic 的服务条款禁止在某些区域使用其服务，因为存在法律、监管和安全风险，受中国等专制区域控制的公司面临法律要求，可能被迫共享数据、配合情报机构或其他造成国家安全风险的行为。

Anthropic 已识别出行为者通过代理服务绕过地理围栏和业务限制，这些服务转售主要西方 AI 模型的访问权，从而限制 Claude 在中国的商业可用性。Anthropic 积极检测并封禁此类操作，并加强执法力度。

从中国国内角度，也存在日益增长的风险：在中国的 AI 应用几乎完全依赖本地模型，因为政府尚未批准任何外国大语言模型供中国用户使用。这意味着向公众分发未经批准的外国 AI 模型访问权本身可能引起国家互联网信息办公室（CAC）的监管关注。

---

## 风险层 3：平台风险——闲鱼（Xianyu）本身

闲鱼由阿里巴巴运营。在闲鱼上销售 VPN 工具、代理设置或受限外国服务访问权违反平台自身规则，并受到监控。Wu Xiangyang 最初在淘宝（闲鱼母生态）上建立其 VPN 业务——仍被起诉。在这些平台上销售并不提供掩护——反而会创建可追踪的商业记录，作为当局证据。

---

## 法律风险总结

## 法律风险总结

| 活动 | 法律风险 | 严重程度 |
|---|---|---|
| 收费为用户安装 Clash/Hysteria | 销售未经授权的 VPN 服务——刑法 §225 | **非常高——监禁 + 罚款** |
| 转售 Claude API 访问权 | 未经授权的电信运营 + Anthropic 服务条款违反 | **高——账户封禁 + 潜在起诉** |
| 向中国用户分发未经批准的外国 AI | CAC 外国 AI 内容法规 | **中高——罚款、平台关闭** |
| 在闲鱼公开销售 | 创建证据链；违反平台规则 | **放大上述所有风险** |

---

## 实际现实

此类业务在中国灰色市场中很常见——卖家使用各种策略吸引不同优先级的消费者：成本、便利性、隐私和技术需求。许多人运营数月或数年未被起诉。然而，执法**不可预测且选择性**——当局行动时，处罚严厉且追溯性。用户越多、收入越高、可见度越高——被针对的风险越大。

简而言之：**此商业模式在中国多方面违法**，每月 500 名用户已足够被视为严肃商业运营，而非个人使用灰色地带。

**参考资料：**

- [How US Models Are Sold in China's Grey Market — ChinaTalk](https://www.chinatalk.media/p/the-grey-market-for-american-llms)
- [Anthropic Updating Regional Restrictions](https://www.anthropic.com/news/updating-restrictions-of-sales-to-unsupported-regions)
- [Man Jailed 5½ Years for Selling VPN — SCMP](https://www.scmp.com/news/china/policies-politics/article/2125326/man-jailed-51/2-years-fined-us76000-selling-vpn)
- [Chinese Programmer Punished for Selling VPN — CNN](https://www.cnn.com/2018/10/10/asia/china-vpn-censorship-intl)
- [Internet Censorship in China — Wikipedia](https://en.wikipedia.org/wiki/Internet_censorship_in_China)
- [Anthropic's Impact on Chinese Claude Users — Yahoo/SCMP](https://www.yahoo.com/news/articles/impact-anthropics-china-ban-unlikely-093000589.html)