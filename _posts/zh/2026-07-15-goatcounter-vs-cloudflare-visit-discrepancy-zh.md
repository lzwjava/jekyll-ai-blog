---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GoatCounter与Cloudflare访问量差异对比
translated: true
type: note
---

问题：为什么 lzwjava.github.io 在 Cloudflare 上显示每月约 6 万次点击（其中约一半是代理流量），但在 GoatCounter 上只有约 4000 次？GoatCounter 是否只统计了"第二次点击"，而跳过了第一次？

回答：

你的"第二次点击"理论反了——看看 GoatCounter 实际的访问逻辑：

```
session_key = site_id + user_agent + IP
if sessions[session_key] exists and < 8h old:
    if path not yet seen in this session:
        count_as_visit = true   # 该路径首次加载会计入
else:
    new session created
    count_as_visit = true       # 首次加载会计入
```

所以页面的**首次**加载正是被计为一次访问的内容。在 8 小时内重新加载或再次访问同一路径**不会**再次计数。并不存在第一次点击被丢弃、第二次点击才被记录这样的机制。

真正的差距来自一系列因素，大致按影响程度排序：

**1. GoatCounter 仅在浏览器中执行 JavaScript 时才触发。**
`count.js` 在 `DOMContentLoaded` 时运行，并通过 `fetch`/beacon POST 向计数端点发送请求。任何不运行 JS 的请求——`curl`、`GPTBot`、`ClaudeBot`、`Bytespider`、爬虫以及大多数执行原始 HTTP 请求的 AI 代理——都不会触及 GoatCounter。你的 Cloudflare 数据是原始边缘请求，因此它记录了所有这些请求。你已经提到约一半的 6 万流量是代理流量——这大约 3 万次就被直接排除了，GoatCounter 设计上就不会统计它们。

**2. Cloudflare 的数字很可能是原始请求，而非去重后的会话。**
如果你是从 Cloudflare 的区域级分析（而非基于 JS 的 Web Analytics 信标）中读取这个数字，它统计的是所有到达边缘的 HTTP 请求：HTML 页面、CSS、JS、图片、`robots.txt`、`sitemap.xml`、RSS 源、favicon 等等。一次人类"访问"加载了一个笔记页面及若干资源，就可能产生 5-10 个请求。GoatCounter 对同一事件只计 1 次访问。仅这一点就能在人类访问侧产生 5-10 倍的差距，甚至还没考虑机器人。

**3. GoatCounter 在上层还有自己的机器人过滤器（`isbot`）。**
即使对于运行了 JS 的请求，GoatCounter 也会在服务器端根据用户代理（user-agent）与机器人列表进行交叉检查，并丢弃任何被识别为机器人的数据，因此边缘自动化流量会被二次过滤。

**4. 广告拦截器/隐私工具会屏蔽第三方分析脚本。**
`*.goatcounter.com` 子域名出现在一些隐私拦截列表（如 EasyPrivacy 风格的列表）中，而你的受众（工程师，通常来自 Hacker News / lobste.rs 的引荐流量）倾向于使用 uBlock / Brave / Pi-hole / NextDNS 的用户。这会导致人类访问侧的真实低估，而 Cloudflare 不会漏掉这些，因为它是边缘层、在 JS 之前就统计了。

**5. 没有实际页面加载的客户端导航。**
如果网站的任何部分通过 `pushState` 进行了预取或导航而没有触发 `DOMContentLoaded`，GoatCounter 的默认脚本不会在该导航时触发，除非你在路由变化时手动调用 `goatcounter.count()`。值得检查你的网站是否有类似 SPA 的行为。

粗略估算供你参考：6 万请求 → 约 3 万代理/机器人（对 GC 不可见）→ 剩余约 3 万人类驱动请求，其中每次真实访问可能对应 3-6 个资源请求 → 最终约 4-5 千次实际独立访问会话。这与你看到的结果一致——不需要假设什么"首次点击遗漏"的 bug。

如果你想获得真实数据，可以查看 Cloudflare 自己在同一时期的**独立访客（Unique Visitors）**指标（而非总请求数）——这个数字才应该与 GoatCounter 的"访问次数"进行同类比较。

参考文献：
- [GoatCounter: 会话和访问如何工作](https://www.goatcounter.com/help/sessions)
- [goatcounter/isbot 机器人检测源码](https://github.com/zgoat/isbot/blob/master/isbot.go)
- [GoatCounter GitHub issue: 页面浏览量 vs 独立访客](https://github.com/arp242/goatcounter/issues/672)
- [GoatCounter GitHub issue: SPA 导航不计数](https://github.com/arp242/goatcounter/issues/482)