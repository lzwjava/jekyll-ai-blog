---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 机器人集群虚增网站分析
translated: true
type: note
---

**问题：** 以下是我实际的 Cloudflare Web Analytics 仪表盘（Core Web Vitals、按国家/地区/引荐来源/浏览器/操作系统/设备划分的页面浏览量），显示同一 30 天窗口期内总页面浏览量为 61.37k，而 GoatCounter 显示约 3.8k–4k。实际情况到底是什么？

**回答：**

这改变了我之前的判断，我应当直接说明：Core Web Vitals（LCP/INP/CLS）的存在确认这**是** JS 信标（beacon）的 Web Analytics 产品，而非我上次指出的原始服务器端边缘日志产品。因此，“选错了 Cloudflare 面板”并非这里的原因——这个信标确实触发了 61k 次。更具体且更有趣的解释是：**你遇到了一个几乎完全集中在单一地理区域/操作系统/浏览器/设备组合上的执行 JS 的机器人集群。**

## 叠加主要数据——它们是同一类流量

看看这些百分比是如何相互叠加的，而不是将其视为五个独立的事实：

| 维度 | 主导桶 | 占 60.95k 的比例 |
| --- | --- | --- |
| 国家/地区 | 新加坡 | 46.28k → **76%** |
| 操作系统 | Windows | 48.48k → **79.5%** |
| 浏览器 | Chrome | 48.89k → **80.2%** |
| 设备 | 桌面端 | 54.24k → **89%** |
| 引荐来源 | 无（直接访问） | 54.87k → **90%** |

一个个人广州工程师的博客，其读者群中自然不可能有 76% 来自新加坡。新加坡是**亚洲密度最高的数据中心/云区域之一**（AWS ap-southeast-1、GCP asia-southeast1、阿里云、腾讯云、DigitalOcean SGP1，同时也是常见的 VPN/住宅代理出口节点）。结合“Windows + Chrome + 桌面端 + 无引荐来源”——这是**无头 Chrome 自动化**（Playwright/Puppeteer 默认启动参数会伪装成普通 Windows Chrome 桌面端用户代理，除非特意随机化）大规模运行在云 VM 上时最常产生的签名。

关键点：这是一个**执行 JavaScript** 的机器人——正因如此，它能触发 Cloudflare 信标，甚至报告真实的 Core Web Vitals（LCP/INP/CLS 数值），而简单的 `curl`/`requests` 抓取工具绝对做不到。这正好属于 Cloudflare 自己的机器人文档中所指出的类别：启用后，Bot Fight Mode 会识别匹配已知机器人模式的流量并发出计算密集型挑战；此外，还可以单独启用 JavaScript 检测来识别无头浏览器及其他网络参与者——之所以特意提供此选项，正是因为执行 JS 的无头浏览器是一个独特且更难捕捉的类别，不同于经典的非 JS 抓取工具。

## 另外两个支持性异常

- **`/error-en` 获得了 1,040 次点击**——真实用户不会访问你的错误页面 1,040 次。这与自动化爬虫频繁探测大量 URL 猜测/幻觉路径并反复落在你的 404/错误路由上的行为一致。
- **真正的人类信号规模较小且独立**: `weixin110.qq.com`（600）、`yandex.ru`+`yandex.com`（470）——合计约 1,070，占总量的不到 2%。这正是我从你 GoatCounter 数据中指出的相同的自然微信分享/Yandex 搜索模式，只是按比例缩放而已。它被自动层覆盖，而非与之矛盾。

## 反推真实数字

从 61k 中剔除约 55k 的新加坡/Windows/Chrome/桌面端/直接访问集群，剩余大约 **5-6k**——这与 GoatCounter 的约 3.8-4k 高度吻合（剩余差距是我之前提到的 GoatCounter 自身的盲点：其脚本域名被广告拦截列表过滤，或更严格的机器人 UA 过滤）。**GoatCounter 的数字自始至终都是可信的。** 60k 从来就不是你的真实读者数。

## 修复它，而非仅绕开测量

1. **开启 Bot Fight Mode**（免费套餐，Security > Settings > 筛选“Bot traffic”）——Bot Fight Mode 包含在免费套餐中，会自动强制启用 JavaScript 检测以识别无头浏览器，而这正是导致你数字膨胀的流量类型。
2. **检查 Security > Analytics > Bot Analysis**（如果你的套餐可见的话）——在开启 Bot Fight Mode 前后查看。Cloudflare 为每个入站请求分配机器人评分，分为自动、可能自动、可能人类三类，并且可以按国家、浏览器、操作系统筛选，以确认新加坡/Windows/Chrome 集群被评分为自动。
3. 等待几天，然后重新查看 Web Analytics 中的国家/操作系统细分——如果这个诊断正确，新加坡的占比应大幅下降，与你真实的亚洲读者群成比例（香港、中国、日本已经显示出合理且小得多的数字）。
4. 为了你的品牌指标目的（AI · Live），**今后将 GoatCounter 作为真实数据使用**，而非原始的 Cloudflare Web Analytics 总量——它也是一个 JS 信标，但显然并非那个击中大量 Cloudflare 前端站点上普遍存在的自动注入信标的流量生成网络的具体目标。

**参考文献：**

- [开始使用 Bot Fight Mode · Cloudflare 机器人解决方案文档](https://developers.cloudflare.com/bots/get-started/bot-fight-mode/)
- [在允许合法流量的同时阻止恶意机器人 · Cloudflare 用例](https://developers.cloudflare.com/use-cases/solutions/stop-malicious-bots/)
- [如何利用 Cloudflare 保护网站免受不必要的机器人流量侵扰 — Kinsta](https://kinsta.com/blog/block-bots-wordpress-cloudflare/)
