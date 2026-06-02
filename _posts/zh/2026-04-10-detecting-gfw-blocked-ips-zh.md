---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 探测被防火长城拦截的服务器IP地址
translated: true
type: note
---

当云服务器的IP被中国防火墙（GFW）屏蔽时，应如何检测？如何从全球多个地点测试其延迟或时延？需要使用哪些工具或网站？

**中国防火墙（GFW）** 是中国的互联网审查系统，它可以从中国大陆境内屏蔽特定IP地址（或域名）的访问。当云服务器的IP被GFW屏蔽时，中国大陆境内的用户通常无法访问该服务器（连接超时、被重置或失败），而服务器在世界其他地区仍可正常访问。由于屏蔽通常是基于IP的，因此该IP上的所有服务都可能受到影响。

### 如何检测IP是否被GFW屏蔽

仅从中国境外无法可靠地检测屏蔽情况，因为GFW主要作用于进出中国的流量。最有效的方法是**从中国境内或邻近地区测试可达性和响应**：

- 使用在线的 **中国防火墙测试** 工具，模拟从多个中国城市（如北京、上海、广州、深圳）访问。这些工具尝试通过位于GFW后的服务器连接您的域名或IP。
  - 推荐网站：
    - <https://www.chinafirewalltest.com/> （由ViewDNS.info支持）
    - <https://www.websitepulse.com/tools/china-firewall-test> （从上海、北京、广州和香港进行对比测试）
    - <https://en.greatfire.org/analyzer> （GreatFire分析器 – 支持IP和域名检查）
    - <https://www.comparitech.com/privacy-security-tools/blockedinchina/>
    - <https://www.dotcom-tools.com/china-firewall-test> （多个中国大陆地点）

- 对于直接IP测试，使用**包含中国境内探测点的多地ping工具**。如果来自中国探测点的ping或连接失败（高丢包率、超时或无响应），而其他全球地点正常，这通常表明存在GFW屏蔽。
  - 常用推荐工具是 **ping.pe**，它在中国境内设有测试点。

其他GFW屏蔽的迹象：

- 来自中国的连接出现TCP重置或超时，但在其他地区正常工作。
- 屏蔽可能是部分性的（仅某些城市受影响），或随时间演变。

注意：GFW屏蔽不受您的云服务商控制，可能发生在VPN/代理服务器或特定内容的网站上。

### 如何从全球多地测试延迟（时延）

要测量来自几十或数百个全球地点的延迟（ping/时延）、丢包率和可达性，可使用**免费的多地ping或时延测试网站**。这些工具并行从全球服务器运行测试，并以表格形式显示结果（最小/平均/最大延迟，丢包率）。

常用可靠工具包括：

- **<https://tools.keycdn.com/ping>** — 从多个全球地点并行ping。
- **<https://globalping.io/>** — 免费平台，支持从全球数千个探测点进行ping、traceroute、HTTP和DNS测试（非常灵活）。
- **<https://www.uptrends.com/tools/ping-test>** — 从40多个检查点进行测试，并提供traceroute数据。
- **<https://ping.pe>** — 从全球地点（包括中国）进行简单同步ping，可用于GFW检测。
- **<https://hostingchecker.com/tools/ping/>** — 从10多个地点快速ping。
- **<https://wondernetwork.com/pings>** — 主要城市之间的全球ping统计。
- 其他值得尝试的工具：Bunny Tools时延测试、LocaPing或Meter.net全球ping测试。

**使用这些工具的方法**：

1. 输入您服务器的IP地址（或域名）。
2. 运行测试 — 结果将显示每个地点的延迟。
3. 观察模式：如果全球延迟正常，但来自中国地点的延迟极高、丢包严重或完全失败，通常意味着GFW屏蔽。

对于更高级的诊断，某些工具还提供traceroute以查看连接在何处中断。

### 补充建议

- 结合两类测试：首先使用中国特定的防火墙测试工具，再通过包含中国探测点的全球延迟工具进行确认。
- 如果IP被屏蔽，常见的解决方法（长期不一定可靠）包括更换IP、使用其他云服务商/地区，或采用高级代理/VPN技术 – 但这些方法仍可能随时间推移被检测到。
- 测试是实时且免费的，但由于路由或临时网络问题，结果可能会有轻微波动。

这些方法可以帮助您清晰了解IP是否被GFW屏蔽，以及服务器在全球的性能表现。

参考资料：

- <https://www.chinafirewalltest.com/>
- <https://www.websitepulse.com/tools/china-firewall-test>
- <https://en.greatfire.org/analyzer>
- <https://tools.keycdn.com/ping>
- <https://globalping.io/>
- <https://www.iozoom.com/client/knowledgebase/127/China-Great-Firewall-GFW-block.html>
