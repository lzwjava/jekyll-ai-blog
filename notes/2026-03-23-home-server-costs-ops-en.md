---
audio: false
generated: true
image: false
lang: en
layout: post
title: Home Server 24/7 Operation and Costs
translated: false
type: note
---

**Question:** Should I keep my home server (i9-13900KF + RTX 4070 Ti, running Gitea, Jellyfin, LibreChat, Nextcloud, SearXNG, etc.) on 24/7 or shut it down daily? Will electricity really only be ~100 CNY/year in Guangzhou? And does frequent shutting down shorten the machine's lifespan compared to leaving it on?

---

**Answer:**

## Your Situation Is Perfect for 24/7 Operation

You're not just running a gaming PC — you're running a **home server** with 7+ active services (Gitea, Jellyfin, LibreChat, Nextcloud, SearXNG, etc.). This is exactly the use case where leaving it on permanently makes sense. Shutting it down daily would break all those services every night.

---

## Electricity Cost Reality Check — Your 100 CNY Estimate Is **Wrong**

Let's do the real math for Guangzhou.

China's residential electricity price is approximately **¥0.53 per kWh**.

Now estimate your server's idle power draw:

| Component | Idle Power |
|---|---|
| i9-13900KF (idle) | ~30–50W |
| RTX 4070 Ti (idle) | ~16–18W at true idle |
| 62 GB RAM + NVMe + motherboard | ~30–40W |
| **Total system idle** | **~80–110W** |

The RTX 40 Series GPUs have architectural enhancements that make idle/desktop power consumption barely register. So your GPU is not the problem at idle.

**Annual cost calculation:**

- 100W average × 24h × 365 days = **876 kWh/year**
- 876 × ¥0.53 = **≈ ¥464/year**

So **100 CNY/year is too optimistic by roughly 4–5×**. A more realistic estimate is **¥400–600 CNY/year** depending on actual load. Still cheap — but not 100.

---

## Does 24/7 Shorten Hardware Lifespan? The Answer Is Nuanced

For electronic parts, startup surges at power-on are a real concern, so leaving the machine on minimizes those events. Desktop and home servers are designed for continuous running — unlike laptops, which are built for regular power cycling.

Extended operation does cause wear on mechanical components like fans and drives. Without regular restarts, memory leaks can accumulate over time, causing slowdowns or crashes — the fix is simply scheduling a weekly reboot, not daily shutdowns.

Modern computers use "thermal cycling" during manufacturing — repeated heating and cooling during production eliminates small cracks and flaws most likely to cause failure. This means today's components are engineered to handle power cycles, making it completely fine to power on and off.

So the truth is:

- **Daily hard shutdowns** = small wear from power cycles + startup surges
- **24/7 operation** = fan wear over time, but avoids surge stress
- **Neither meaningfully kills a ¥14,000 machine** within any normal timeframe

For a machine this beefy, the difference in lifespan from shutdown habits is negligible compared to factors like dust buildup, cooling quality, and power surges.

---

## My Recommendation: Leave It On 24/7, With Smart Practices

Given that you're running a full home server stack, the right choice is clear:

1. **Leave it on 24/7.** Shutting it down nightly breaks Gitea, Nextcloud, Jellyfin, and LibreChat for anyone (or any scheduled task) trying to reach them.
2. **Schedule a weekly automatic reboot** (e.g., Sunday 4am) to clear memory leaks and apply pending updates — this is what real servers do.
3. **Set power-saving on the GPU** — enable NVIDIA's "desktop performance" or "adaptive" power mode so the 4070 Ti truly idles at 16–18W instead of staying at higher clocks unnecessarily.
4. **Monitor temps and clean dust** every 3–6 months — Guangzhou's humid climate accelerates dust accumulation.
5. **Budget ¥400–600/year for electricity**, not 100.

The machine cost ¥14,000. Even at ¥500/year in electricity, that's only **3.5% of hardware cost per year** — a completely worthwhile trade for the convenience of always-on services. Shutting it down daily saves maybe ¥200–300/year at the cost of breaking your entire self-hosted stack nightly. Not worth it.

---

References:

- [China Residential Electricity Price](https://www.globalpetrolprices.com/China/electricity_prices/)
- [RTX 4070 Ti Idle Power - Guru3D](https://www.guru3d.com/review/undervolting-the-yeston-geforce-rtx-4070-ti/page-6/)
- [NVIDIA RTX 4070 Ti Official Page](https://www.nvidia.com/en-us/geforce/news/geforce-rtx-4070-ti/)
- [Is it OK to Keep a PC Running 24/7 - MyComputerWorks](https://mycomputerworks.com/is-it-okay-to-keep-a-pc-running-24-7/)
- [Computers & Electricity Myths - IGS](https://www.igs.com/energy-resource-center/blog/3-myths-about-computers-and-electricity)
- [PC 24/7 Hardware Lifespan Discussion - TenForums](https://www.tenforums.com/performance-maintenance/128668-7-24-computer-power-bad-hardwares-lifespan.html)
