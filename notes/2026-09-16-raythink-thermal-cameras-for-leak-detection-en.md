---
audio: false
generated: true
image: false
lang: en
layout: post
title: Raythink Thermal Cameras for Leak Detection
translated: false
type: note
---

Question: **How good is the RAYTHINK 睿创燧石 handheld thermal camera for underfloor heating / water-leak detection?**

Answer: **It looks quite good, especially if you're talking about the EX100/EX100 Pro or CX200-class models.** Raythink is not a random white-label thermal camera brand; it is a real Chinese thermal-imaging company with its own IR detector technology and a fairly broad industrial product line. ([Raythink Tech][1])

The important part is **which exact model**. The title you pasted is marketplace-style marketing and doesn't identify the model.

### For finding a water leak

A thermal camera is useful because you are really looking for a **temperature anomaly**, not "water" itself.

For example, with underfloor heating:

```text
hot-water pipe
████████████████████
      ↓
    floor
────────────────────────
        ↓ heat
     🌡️ 🌡️ 🌡️
────────────────────────
IR camera
     ↓
   [🔥🔥🔥]
```

A healthy pipe produces a relatively continuous thermal line. A leak / abnormal moisture area can produce a colder or otherwise abnormal region, depending on the floor construction and temperature conditions.

But **thermal imaging does not directly detect water**. It detects surface temperature. So:

* underfloor heating pipe localization → **excellent use case**
* finding a suspected leak → **very useful**
* pinpointing the exact hole in a pipe → **not guaranteed**
* detecting a cold-water pipe leak → **much harder**
* detecting moisture behind a wall → **possible, but conditions matter**

### The interesting part: resolution

Raythink's **RM200A**, for example, has:

* 256×192 native IR
* NETD <40 mK
* 25 Hz
* 56°×42° FOV
* ±2°C or ±2% measurement accuracy
* manual point/line/area temperature analysis
* visible-light camera + thermal fusion
* Wi-Fi / USB
* ~8 h total runtime with two batteries
* IP54

That's already a legitimate diagnostic instrument, not just an IR thermometer. ([Raythink Tech][2])

For comparison, Raythink's cheaper **EX100** generation is positioned specifically for HVAC, leak detection and maintenance. The company announced the EX100 SE in 2026 with a 128×128 detector and 40 mK sensitivity. ([Raythink Tech][3])

### [Raythink EX100 Handheld Thermal Imager](https://openelab.io/products/raythink-ex100-handheld-infrared-thermal-imager?utm_campaign=openai_catalog&utm_content=product_card&utm_medium=feed&variant=45704753610950&utm_source=chatgpt.com)

*$180.81*

### [Raythink EX100 Pro Handheld Thermal Imager](https://openelab.io/products/raythink-ex100-pro-handheld-infrared-thermal-imager?utm_campaign=openai_catalog&utm_content=product_card&utm_medium=feed&variant=45704753643718&utm_source=chatgpt.com)

*$242.26*

### [MILESEEY TR20 Thermal Imaging Camera](https://www.homedepot.com/p/MILESEEY-TR20-Infrared-Thermal-Imaging-Camera-Video-Recording-2-8-in-LCD-Display-4-to-1022-F-Range-Auto-Spot-Tracking-TR20/340302217?fp=oai&utm_source=chatgpt.com&utm_medium=feed)

*$279.99*

### [Teslong TTM260 Thermal Imaging Camera](https://www.bhphotovideo.com/c/product/1912221-REG/teslong_tsttm260_thermal_infrared_camera.html?BI=23971&kw=TETSTTM260&utm_source=chatgpt.com&utm_medium=feed)

*$319.99*

### My take

If you're buying it for **home renovation / HVAC / underfloor heating troubleshooting**, I'd rank the requirements roughly:

```text
native IR resolution     ██████████
NETD / thermal sensitivity █████████
FOV                       ████████
manual focus              ███████
temperature accuracy      ███████
software / image export   ██████
```

**256×192 + <40 mK** is already a very comfortable sweet spot for this job. I would not pay a huge premium merely to get 384×288 unless you're doing professional inspection where you need to resolve small thermal features at distance.

One thing I'd be careful about: **don't confuse "super resolution" with native IR resolution.** A 256×192 sensor with AI/TISR outputting 512×384 does *not* contain the same spatial information as a native 512×384 sensor.

### If you're looking at one around ¥700–¥1,500

That's actually where Raythink becomes interesting. Current Chinese listings show the EX100 around **¥699**, while CX200 SE+ listings are around **¥1,299**; these prices can vary by seller/configuration. ([Yantai 11467][4])

For **specifically locating underfloor heating problems**, I'd rather buy a **good 256×192 thermal camera from Raythink for ~¥1k–2k** than spend several thousand on an industrial 384×288 model.

If you send me the **exact product link or screenshot of the listing**, I can tell you whether *that particular one* is a good buy and compare it against 2–3 alternatives at the same price.

[1]: https://www.raythink-tech.cn/?utm_source=chatgpt.com "红外热像仪_热成像仪_红外热成像仪_燧石技术（烟台）有限公司"
[2]: https://www.raythink-tech.cn/uploadfile/202407/cc84b55e29471bd.pdf?utm_source=chatgpt.com "RM200A
手持测温热像仪
RM200A搭载自研12μm高热灵敏度256×192红外
热成像核芯，"
[3]: https://www.raythink-tech.cn/index.php?c=show&id=522&utm_source=chatgpt.com "睿创燧石EX100 SE诚意登场，重塑热像仪入门高标准！_资讯中心_关于我们_燧石技术（烟台）有限公司"
[4]: https://yantai.11467.com/info/45208139.htm?utm_source=chatgpt.com "Raythink燧石技术EX100万用热像仪，暖通、漏水检测"
