---
audio: false
generated: true
image: false
lang: en
layout: post
title: RAYTHINK CX200S vs EX100 for PCB
translated: false
type: note
---

Question: **Should I buy the RAYTHINK 睿创燧石 thermal camera instead of the FeelElec FR03D?**

Answer: **Yes — but only if the RAYTHINK model you're looking at is the CX200S / CX200S Ultra.** If the listing is actually the cheap **EX100**, I'd take the **FR03D + macro lens** for PCB work.

The title you pasted is too generic to identify the exact RAYTHINK model. RAYTHINK has several handheld cameras with radically different sensors.

### My ranking for your use case

Assuming your main purpose is **electronics/PCB debugging**:

|                    | FeelElec FR03D | RAYTHINK EX100 | RAYTHINK CX200S |
| ------------------ | -------------: | -------------: | --------------: |
| Native IR          |       240×240* |    **160×120** |     **256×192** |
| NETD               |          ~40mK |           40mK |    better class |
| Focus              |   fixed/varies |          fixed |   better optics |
| PCB                |            ⭐⭐⭐ |             ⭐⭐ |        **⭐⭐⭐⭐** |
| General inspection |           ⭐⭐⭐⭐ |            ⭐⭐⭐ |       **⭐⭐⭐⭐⭐** |
| Build/ecosystem    |         budget |           good | **much better** |

*Be careful with marketplace listings: "240×240" can sometimes refer to display/super-resolution rather than the native detector.

RAYTHINK's official EX100 specification is actually **160×120 native**, 40mK, 4.62 mrad IFOV, and 11 cm minimum imaging distance. ([Raythink Tech][1])

Their newer **CX200S** uses a **256×192 detector**, with AI super-resolution to 512×384. RAYTHINK specifically lists electronics repair as a use case. ([Raythink Tech][2])

### Why I'd prefer CX200S

For PCB debugging, this matters much more:

```text
native pixels
      ↓
spatial resolution
      ↓
can I distinguish component A from component B?
      ↓
can I locate the actual failing component?
```

A 256×192 sensor has **49,152 native thermal pixels**.

160×120 has only:

```text
19,200
```

That's ~**2.56× fewer thermal pixels**.

AI upscaling doesn't create missing thermal information. So:

```text
160×120 → AI → 320×240
```

doesn't become equivalent to a real 320×240 detector.

That's why I'd prioritize **native detector resolution + IFOV + optics**.

### But there's an even more important point

For your specific use case, **macro capability beats almost everything else once you're looking at tiny SMDs**.

RAYTHINK's high-end RT630 is a good illustration: its official documentation specifies dedicated macro optics, down to **30–60 µm per pixel**, with minimum imaging distances of 19–39 mm. ([Raythink Tech][3])

That's the kind of optics that makes thermal imaging genuinely interesting for:

```text
phone PCB
    ↓
PMIC
    ↓
0.5 mm capacitor
    ↓
find the exact hot component
```

A generic 256×192 thermal camera without good close-focus optics can still be disappointing here.

## What I'd buy

**If the RAYTHINK listing is CX200S:**
→ **Buy RAYTHINK CX200S.**

### [Raythink CX200S Handheld Thermal Imaging Temperature Meter](https://openelab.io/products/raythink-cx200s-handheld-thermal-imaging?utm_campaign=openai_catalog&utm_content=product_card&utm_medium=feed&variant=45715511181510&utm_source=chatgpt.com)

*$464.00*

**If it's EX100:**
→ **I'd buy FR03D + macro lens instead**, assuming the price is similar.

**If you can spend ~$400–700:**
→ I'd skip both and look for a **native 256×192 or 384×288 camera with manual focus + macro/close-focus capability**. That's where the experience starts getting substantially better for board repair.

If you send me the **RAYTHINK listing screenshot or exact model number + price**, I can tell you **"buy this / don't buy this"** rather than guessing which RAYTHINK model the listing refers to.

References:

* [RAYTHINK official EX100 specifications](https://raythink-tech.cn/index.php?c=show&id=448&utm_source=chatgpt.com)
* [RAYTHINK official CX200S information](https://www.raythink-tech.cn/index.php?c=show&id=527&utm_source=chatgpt.com)
* [RAYTHINK official RT630 specifications](https://www.raythink-tech.cn/index.php?c=show&id=48&utm_source=chatgpt.com)

[1]: https://raythink-tech.cn/index.php?c=show&id=448&utm_source=chatgpt.com "EX100_手持测温热像仪_温度检测_工业监测_产品中心_燧石技术（烟台）有限公司"
[2]: https://www.raythink-tech.cn/index.php?c=show&id=527&utm_source=chatgpt.com "Raythink睿创燧石CX200S系列手持红外热像仪荣获2026国际CMF最佳CMF设计奖！_资讯中心_关于我们_燧石技术（烟台）有限公司"
[3]: https://www.raythink-tech.cn/index.php?c=show&id=48&utm_source=chatgpt.com "RT630_手持测温热像仪_温度检测_工业监测_产品中心_燧石技术（烟台）有限公司"
