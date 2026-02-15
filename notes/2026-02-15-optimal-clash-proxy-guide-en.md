---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimal Clash Proxy Selector Guide
translated: false
type: note
---

**Question:** In mainland China using Clash with these rule provider groups (like 节点选择, 谷歌FCM, OpenAI, 漏网之鱼, GitHub, 全球直连, 微软服务, 全球拦截, YouTube, 应用净化, Google, 国外媒体, 苹果服务, 电报信息), which selector group should be chosen as the main proxy selector, considering Hong Kong proxies are not acceptable but Singapore (新加坡), Japan (日本), Taiwan (台湾), US, etc., are okay?

**Answer:**

In mainland China, when using a typical Clash configuration with these common Chinese rule sets (often from Loyalsoldier, blackmatrix7, or similar popular providers), the **main selector group you should usually choose / set as your default proxy policy group** is:

**🚀 节点选择** (or similar name containing "节点选择")

### Why 节点选择 is the best main choice
- This group is specifically designed as the **user-facing proxy selector** for foreign / non-China traffic in most popular rule sets used in China.
- It normally includes a mix of good nodes (often filtered for low latency or high speed to China).
- Other groups are more specialized:
  - **国外媒体** → overseas streaming / media sites (Netflix, Disney+, HBO, etc.)
  - **YouTube** → YouTube only
  - **Google** / **OpenAI** / **电报信息** / **GitHub** → specific services, usually point to fast nodes for that service
  - **🍎 苹果服务** / **Ⓜ️ 微软服务** → Apple / Microsoft services (often better with certain regions or even DIRECT in some rules)
  - **🌍 国外媒体** (sometimes overlaps with 国外媒体)
  - **漏网之鱼** → final catch-all for foreign IPs/domains that didn't match earlier rules (very important fallback)

**Recommended priority order for choosing a selector (in mainland China, 2026 context):**

1. **🚀 节点选择**  
   → Most common and recommended default/global selector for general browsing, almost all foreign traffic goes here in well-configured rules.

2. **漏网之鱼**  
   → If you want stricter / more conservative routing (everything not explicitly matched goes through proxy). Very popular second choice.

3. **国外媒体** or **YouTube**  
   → Only if your main usage is streaming (Netflix, YouTube, etc.) and you want dedicated nodes for them (sometimes these have better unlocking ability).

### Quick mapping of common behavior in mainland China rule sets

| Group name          | Typical purpose                          | Recommended for main selector? | Notes (China usage)                  |
|---------------------|------------------------------------------|--------------------------------|--------------------------------------|
| 🚀 节点选择        | General foreign traffic selector        | **Yes – best default**        | Usually contains SG/JP/US/etc.      |
| 漏网之鱼            | Catch-all foreign traffic               | Yes (alternative default)     | Safe and comprehensive               |
| 国外媒体            | Streaming/media unlock                  | Sometimes                     | Good for Netflix/Disney if unlocking issues |
| YouTube             | YouTube-specific                        | No (unless heavy YouTube)     | Often proxies through fast nodes     |
| Google / OpenAI     | Specific service optimization           | No                            | Usually subset of 节点选择          |
| 苹果服务 / 微软服务 | Better compatibility for CN-App Store   | No (often DIRECT)             | Many rules set these to DIRECT       |
| 全球直连            | Domestic / direct traffic               | No                            | Must stay DIRECT                     |
| 全球拦截            | Ad/tracker blocking                     | No                            | Set to REJECT                        |

### Practical advice given your proxy list
- Your available good nodes are mainly **新加坡 (SG)**, **日本 (JP)**, **台湾 (TW)**, **美国 (US)** etc. (Hong Kong is bad/unusable).
- In **节点选择** group → manually select or use **url-test / fallback / load-balance** strategy and choose the best performing SG/JP/US node (ignore HK ones).
- If **节点选择** contains too many HK nodes and latency is poor → switch main policy to **漏网之鱼** instead (it usually inherits similar proxies but is less pre-filtered).

**Most people in mainland China in 2025–2026 set:**

GLOBAL / FINAL policy group → **🚀 节点选择**

That's the safest and most common recommendation.

**References:**

- https://docs.reiz.link/%E9%99%84%E5%BD%95/clash-advanced-usage
- Common Clash rule discussions on GitHub (Loyalsoldier/clash-rules patterns)