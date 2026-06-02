---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 家庭服务器 24/7 运行与成本
translated: true
type: note
---

**Question:** 我应该让我的 home server（i9-13900KF + RTX 4070 Ti，运行 Gitea, Jellyfin, LibreChat, Nextcloud, SearXNG 等）24/7 全天候运行，还是每天关机？在广州，一年的电费真的只要 100 元左右吗？频繁关机与一直开机相比，是否会缩短机器寿命？

---

**Answer:**

## 你的情况非常适合 24/7 全天候运行

你运行的不仅仅是一台 gaming PC —— 你是在运行一台部署了 7 个以上活跃服务（Gitea, Jellyfin, LibreChat, Nextcloud, SearXNG 等）的 **home server**。在这种使用场景下，保持常开是有意义的。每天关机会导致这些服务在每晚都处于中断状态。

---

## 电费考量 —— 你 100 元的估算是有误的

让我们按照广州的实际情况计算一下。

中国居民用电价格大约为 **¥0.53/kWh**。

现在估算你服务器的 idle 功耗：

| Component | Idle Power |
|---|---|
| i9-13900KF (idle) | ~30–50W |
| RTX 4070 Ti (idle) | 在真正待机时 ~16–18W |
| 62 GB RAM + NVMe + motherboard | ~30–40W |
| **Total system idle (系统总待机)** | **~80–110W** |

RTX 40 Series GPU 在架构上进行了增强，使得 idle/desktop 功耗几乎可以忽略不计。因此在待机状态下，你的 GPU 并不是问题所在。

**年电费计算：**

- 平均 100W × 24h × 365 days = **876 kWh/year**
- 876 × ¥0.53 = **≈ ¥464/year**

因此，**每年 100 元的估算过于乐观了，大约低估了 4-5 倍**。更现实的估算是在 **¥400–600/year** 之间，具体取决于实际负载。虽然依然便宜，但绝不是 100 元。

---

## 24/7 运行会缩短硬件寿命吗？答案很微妙

对于电子元件，开机时的电流浪涌（startup surges）确实是一个值得关注的问题，因此保持机器开启可以减少这类事件。Desktop 和 home servers 本就是为持续运行而设计的 —— 而不像 laptops 主要是为了频繁的电源循环而构造。

长时间运行确实会对风扇和硬盘等机械部件造成磨损。如果不定期重启，memory leaks 会随着时间积累，导致系统变慢或崩溃 —— 解决办法是设定每周重启一次，而不是每天关机。

现代计算机在制造过程中会经历“热循环”（thermal cycling）测试 —— 生产过程中的反复加热和冷却已经排除了最可能导致故障的微小裂纹。这意味着今天的组件在工程设计上足以应对电源循环，正常开关机完全没有问题。

所以事实是：

- **每日硬关机 (Daily hard shutdowns)** = 电源循环带来的微量磨损 + 开机浪涌压力
- **24/7 运行** = 随时间产生的风扇磨损，但避免了浪涌压力
- **两者都不会在正常使用周期内显著损坏一台价值 ¥14,000 的机器**

对于这样一台高性能机器，开关机习惯对寿命的影响，与积灰、散热质量和电压波动等因素相比微乎其微。

---

## 我的建议：保持 24/7 运行，并采取科学管理

鉴于你运行着完整的 home server stack，正确的选择很明确：

1. **保持 24/7 开启。** 每晚关机会中断 Gitea, Nextcloud, Jellyfin 和 LibreChat，影响用户或计划任务的访问。
2. **设置每周自动重启**（例如：周日凌晨 4 点）以清理 memory leaks 并应用挂起的更新 —— 这是专业服务器的常规操作。
3. **设置 GPU 节能模式** —— 开启 NVIDIA 的 "desktop performance" 或 "adaptive" 电源模式，确保 4070 Ti 在待机时真正保持在 16–18W，而不是维持在高频率。
4. **监控温度并清理积灰**，每 3–6 个月一次 —— 广州潮湿的气候会加速灰尘堆积。
5. **准备每年 ¥400-600 的电费预算**，而不是 100 元。

这台机器价值 ¥14,000。即使每年电费 ¥500，也仅占 **硬件成本的 3.5%** —— 为了享受服务常驻带来的便利，这完全是值得的交易。每天关机或许能省下 ¥200-300，但代价是每晚都要关停你的 self-hosted 栈。这不值得。

---

References:

- [China Residential Electricity Price](https://www.globalpetrolprices.com/China/electricity_prices/)
- [RTX 4070 Ti Idle Power - Guru3D](https://www.guru3d.com/review/undervolting-the-yeston-geforce-rtx-4070-ti/page-6/)
- [NVIDIA RTX 4070 Ti Official Page](https://www.nvidia.com/en-us/geforce/news/geforce-rtx-4070-ti/)
- [Is it OK to Keep a PC Running 24/7 - MyComputerWorks](https://mycomputerworks.com/is-it-okay-to-keep-a-pc-running-24-7/)
- [Computers & Electricity Myths - IGS](https://www.igs.com/energy-resource-center/blog/3-myths-about-computers-and-electricity)
- [PC 24/7 Hardware Lifespan Discussion - TenForums](https://www.tenforums.com/performance-maintenance/128668-7-24-computer-power-bad-hardwares-lifespan.html)
