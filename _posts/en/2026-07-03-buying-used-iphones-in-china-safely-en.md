---
audio: false
generated: true
image: false
lang: en
layout: post
title: Buying Used iPhones in China Safely
translated: false
type: note
---

**Question:** How do I buy a second-hand iPhone in China — on Zhuanzhuan (转转) and similar platforms — without getting scammed?

**Answer:**

## Platform choice

The main online channels are Zhuanzhuan and Xianyu (闲鱼); most people buying Apple devices pick Zhuanzhuan because its 官方验 (official inspection) listings come with a free, detailed inspection report covering appearance, functionality, and battery. Rough tiering:

1. **转转官方验 (Zhuanzhuan official-inspected)** — safest default. Every phone has been through their QC center with a report on the listing page; slightly pricier but very hard to get burned. One buyer who bought 5 phones on Zhuanzhuan to compare found the phones matched the inspection reports well.
2. **转转自由市场 (free market, individual sellers)** — prices vary more and you can find deals, but quality isn't guaranteed like official-inspected. If you buy here, pay the ~¥30–60 for 转转验机 (Zhuanzhuan's inspection-as-middleman service) — the phone routes through their QC center before reaching you.
3. **Xianyu** — best prices, zero curation. Fine if you can verify in person (Guangzhou has plenty of local sellers — 华强北 supply is nearby, which cuts both ways). Ship-only from strangers = highest risk.
4. **JD 拍拍 / Apple 官翻** — Apple's official refurbs are returned/display units refurbished and resold at ~85% of new price; boring but safe. Note one Zhihu comparison found JD units with "100% new original batteries" actually drained twice as fast as an untouched 86% original battery from Zhuanzhuan — replaced batteries are often not what they claim.

## The kill-list — reject immediately if any of these fail

**1. iCloud activation lock / hidden ID.** The #1 scam. If the iPhone has an activation lock, you can't confirm the seller is the real owner, and it can be remotely locked into a brick at any time. Test: Settings → Erase iPhone, do a full factory reset, and go through activation — if it asks for someone else's Apple ID during setup, there's a hidden ID lock. Some shady sellers use software to hide the ID lock, so a full erase-and-reactivate is the only reliable test. Do this before the return window closes, always.

**2. Serial number / GSX check.** GSX queries pull directly from Apple's database and are very hard for scammers to fake, though they won't show unofficial repairs or physical condition. Serial numbers can be spoofed on the software side, so cross-check the serial in Settings → About against the box/report and the GSX result. Watch for US/Japan/Korea-version boards rewritten with 国行 serials.

**3. 爱思助手 (i4/Aisi) full-green.** Plug into a computer, run the verification. Aisi compares hardware component IDs against factory values and flags mismatches in red. All-green doesn't guarantee clean (爱思改绿 exists — scammers can spoof green), but any red is definitely a problem. On your Mac you can also sanity-check from the terminal:

```bash
brew install libimobiledevice
ideviceinfo | grep -E 'SerialNumber|ModelNumber|ProductType|RegionInfo'
# BatteryHealth-ish via diagnostics:
idevicediagnostics ioregentry AppleSmartBattery
```

**4. Battery.** Settings → Battery → Battery Health. Prefer original untouched batteries over replacements — Zhuanzhuan's replacements are typically Pisen third-party cells with a reputation for swelling within months. An original at 85–88% beats a "new" third-party 100%.

**5. Non-original parts / repairs.** iOS itself helps now: Settings → General → About shows "Unknown Part" warnings for non-genuine display/battery/camera on recent models. A replaced battery is acceptable; a replaced motherboard, camera, or screen is not. Dust inside the camera lens on modern iPhones means it's been opened up — likely hidden problems.

**6. 扩容机 / 合约机 / 有锁机.** Storage-expanded phones (hard drive swapped) have worse stability than stock. Carrier-contract phones sell suspiciously cheap (e.g. ¥2000+ iPhone 14 Pro Max) but are SIM-restricted. If a deal looks 30%+ below market, it's one of these or stolen.

## On-arrival protocol (free-market purchases especially)

Record an unboxing video, inspect on delivery if possible (refuse in person if there's a problem), or open within 12 hours; check cosmetic condition and battery health against the listing, then connect to a computer and verify 沙漏/爱思 all-green. Then: full erase → reactivate (ID lock test) → screen check with pure white/black/red/green wallpapers at max brightness for dead pixels, backlight bleed, and viewing angles → test every button, Face ID, both cameras, speakers, mic, WiFi, GPS. The video is your evidence for the dispute process — Zhuanzhuan sides with buyers who have unboxing footage.

## Practical strategy for you

Given your risk tolerance is probably "don't waste my time," the optimal play is: **Zhuanzhuan 官方验, 95新 (95% new), original battery ≥85%, no replaced parts in the report**. You pay maybe ¥100–300 over free-market price and skip the entire adversarial game. Reserve Xianyu/free-market hunting for when you enjoy it as a sport. Also don't buy the absolute latest generation used — the discount vs. new is thin; the sweet spot is 1–2 generations back where you get ~50% off with years of iOS support left.

**References:**

- [转转买二手iPhone验机攻略 — 知乎](https://zhuanlan.zhihu.com/p/482350026)
- [2026年二手iPhone如何验机 — 知乎](https://zhuanlan.zhihu.com/p/1995071021464699932)
- [含所有经验贴！二手苹果验机流程 — 知乎](https://zhuanlan.zhihu.com/p/1935085612613997534)
- [二手iPhone验机指南 — 爱思助手](https://m.i4.cn/article/11992.html)
- [转转验机报告怎么样 — 知乎](https://zhuanlan.zhihu.com/p/685731834)
