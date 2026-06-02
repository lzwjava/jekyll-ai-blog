---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 优化GFW穿透与网络延迟
translated: true
type: note
---

感谢分享你的设置和经验——从最初的代理脚本与VPN组合，演进到使用澳门SIM卡直连蜂窝网络的方案，听起来是经过深思熟虑的优化。很高兴得知这个方案在过去几个月运行良好，特别是用Python脚本自动选择代理（优先新加坡节点访问AI工具），并在笔记本电脑上持续使用zhs.cloud的VPN服务。每月150元享20GB流量及附加服务的澳门SIM卡，确实是个绕过防火墙限制且无需持续依赖应用的移动端解决方案。

关于澳门SIM卡在访问被墙网站时速度最快的发现很合理——来自澳门的直连蜂窝IP通常比香港或内地节点更能规避地缘封锁，尤其对ChatGPT、Claude等存在区域限制的服务更为明显。在Shadowrocket中为特定服务（如ChatGPT指向美国代理）设置路由规则是巧妙的调整，但iOS系统上全局代理导致的每个网络请求延迟确实是普遍痛点。当Shadowrocket（或Surge）拦截过多流量时，即使像Twitter/X这类未被完全封锁的应用也会出现较高延迟。

根据你的使用笔记，以下是一些注重实用性的优化建议：

### Shadowrocket 优化方案
- **精准规则降低延迟**：建议用精细化规则替代全局代理。例如在Shadowrocket配置中采用以下流控逻辑：
  - **直连模式**：本地及区域流量（如微信、百度）默认直连
  - **代理/拒绝**：仅将高优先级被墙域名加入白名单（如ChatGPT、Claude、Google等路由至美国代理）
  - 规则示例（写入`.conf`文件）：
    ```
    [Rule]
    DOMAIN-KEYWORD,chatgpt.com,PROXY
    DOMAIN-KEYWORD,claude.ai,PROXY
    DOMAIN-KEYWORD,google.com,PROXY
    DOMAIN-KEYWORD,twitter.com,PROXY  # 仅当ChatGPT等服务依赖时启用
    MATCH,DIRECT  # 未匹配流量全部直连
    ```
  这样仅特定网站经过代理链路，可显著降低延迟。可通过Clash或Stash、Quantumult X等管理器快速生成规则。
- **延迟测试**：配置后使用Fast.com或Ookla进行速度测试。若延迟仍较高，可尝试缩减代理链路层级——单跳美国代理可能比多级中转更高效。

### 轻量级iOS替代方案
若Shadowrocket开销过大（你曾提及一日后即停用），以下方案更贴近澳门SIM卡的直连理念：
- **按需启动的VPN应用**：ExpressVPN或NordVPN等支持按应用路由（仅对ChatGPT、Mistral等启用VPN），无需全局代理且兼容蜂窝数据
- **Clash移植iOS**：若欣赏桌面端Python脚本的逻辑，可将简化版Clash配置移植至Surge或Stash。创建以"DIRECT"为首选、仅代理特定域名的规则集，延迟远低于全局代理
- **SIM卡直连代理**：既然已倾向用澳门SIM卡访问Mistral和Grok，建议检查这些AI服务是否支持澳门IP直连，或尝试无痕模式访问以避免应用级路由

### 综合建议
- **iOS电量与延迟**：长期代理会加速耗电，可通过系统工具监控并设置定时开关（如仅在高峰时段启用代理）
- **服务稳定性**：zhs.cloud作为笔记本电脑VPN方案表现可靠，若扩展至iOS需确认其客户端兼容性。澳门CTM等运营商信号稳定，但需留意流量限额
- **长期适用性**：离境后的备用方案值得考虑，建议搭配全球eSIM或漫游套餐。同时注意政策变动可能影响访问工具的有效性

若遇到具体配置问题（如分享Shadowrocket规则文件）或需要Clash脚本调整，欢迎提供更多细节——我会在保持简洁的前提下协助排查。祝使用顺利！🚀
