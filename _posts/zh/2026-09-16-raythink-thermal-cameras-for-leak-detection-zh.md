---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Raythink热像仪用于泄漏检测
translated: true
type: note
---

问题：**RAYTHINK 睿创燧石手持热像仪用于地暖/漏水检测效果如何？**

回答：**看起来相当不错，尤其是如果你说的是 EX100/EX100 Pro 或 CX200 级别的型号。** Raythink 不是一个随机的白标热像仪品牌；它是一家真正的中国热成像公司，拥有自己的红外探测器技术和相当广泛的工业产品线。（[Raythink Tech][1]）

关键部分是**具体是哪个型号**。你粘贴的标题是电商风格的市场营销文案，没有标明具体型号。

### 关于查找漏水

热像仪之所以有用，是因为你实际上是在寻找**温度异常**，而不是"水"本身。

例如，对于地暖：

```text
热水管道
████████████████████
      ↓
    地板
────────────────────────
        ↓ 热量
     🌡️ 🌡️ 🌡️
────────────────────────
红外相机
     ↓
   [🔥🔥🔥]
```

健康的管道会产生相对连续的热线。泄漏/异常潮湿区域可能会产生较冷或其他异常区域，具体取决于地板结构和温度条件。

但**热成像并不能直接检测水**。它检测的是表面温度。因此：

* 地暖管道定位 → **极佳的应用场景**
* 查找疑似泄漏点 → **非常有用**
* 精确定位管道上的确切孔洞 → **不保证**
* 检测冷水管道泄漏 → **困难得多**
* 检测墙壁后面的潮湿 → **可能，但取决于条件**

### 有趣的部分：分辨率

例如，Raythink 的 **RM200A** 具有：

* 256×192 原生红外分辨率
* NETD <40 mK
* 25 Hz
* 56°×42° 视场角
* ±2°C 或 ±2% 测量精度
* 手动点/线/区域温度分析
* 可见光相机 + 热融合
* Wi-Fi / USB
* 双电池总续航约 8 小时
* IP54

这已经是一款合格的诊断仪器，而不仅仅是一个红外测温仪。（[Raythink Tech][2]）

相比之下，Raythink 更便宜的 **EX100** 系列专门定位于暖通空调、泄漏检测和维护。该公司于 2026 年发布了 EX100 SE，配备 128×128 探测器和 40 mK 灵敏度。（[Raythink Tech][3]）

### [Raythink EX100 手持热像仪](https://openelab.io/products/raythink-ex100-handheld-infrared-thermal-imager?utm_campaign=openai_catalog&utm_content=product_card&utm_medium=feed&variant=45704753610950&utm_source=chatgpt.com)

*$180.81*

### [Raythink EX100 Pro 手持热像仪](https://openelab.io/products/raythink-ex100-pro-handheld-infrared-thermal-imager?utm_campaign=openai_catalog&utm_content=product_card&utm_medium=feed&variant=45704753643718&utm_source=chatgpt.com)

*$242.26*

### [MILESEEY TR20 热成像相机](https://www.homedepot.com/p/MILESEEY-TR20-Infrared-Thermal-Imaging-Camera-Video-Recording-2-8-in-LCD-Display-4-to-1022-F-Range-Auto-Spot-Tracking-TR20/340302217?fp=oai&utm_source=chatgpt.com&utm_medium=feed)

*$279.99*

### [Teslong TTM260 热成像相机](https://www.bhphotovideo.com/c/product/1912221-REG/teslong_tsttm260_thermal_infrared_camera.html?BI=23971&kw=TETSTTM260&utm_source=chatgpt.com&utm_medium=feed)

*$319.99*

### 我的看法

如果你是买来用于**家装 / 暖通空调 / 地暖故障排查**，我大致按需求排序如下：

```text
原生红外分辨率        ██████████
NETD / 热灵敏度        █████████
视场角                ████████
手动对焦              ███████
温度精度              ███████
软件 / 图像导出        ██████
```

**256×192 + <40 mK** 对于这项工作来说已经是一个非常舒适的黄金配置。我不会仅仅为了获得 384×288 而支付高昂的溢价，除非你是做专业检测，需要在远距离分辨较小的热特征。

有一点我需要提醒：**不要把"超分辨率"和原生红外分辨率混为一谈。** 一个 256×192 的传感器通过 AI/TISR 输出 512×384，并不包含与原生 512×384 传感器相同的空间信息。

### 如果你看的是 ¥700–¥1,500 价位的产品

那其实是 Raythink 比较有吸引力的区间。目前国内电商平台上 EX100 大约在 **¥699** 左右，而 CX200 SE+ 大约在 **¥1,299** 左右；这些价格可能因卖家和配置而异。（[烟台 11467][4]）

对于**专门定位地暖问题**，我宁愿花 **¥1k–2k** 买一台 Raythink 的优质 256×192 热像仪，也不愿花几千块买一台工业级 384×288 型号。

如果你把**确切的商品链接或截图**发给我，我可以告诉你*那一款*是否值得买，并与同价位的 2–3 个替代品进行对比。

[1]: https://www.raythink-tech.cn/?utm_source=chatgpt.com "红外热像仪_热成像仪_红外热成像仪_燧石技术（烟台）有限公司"
[2]: https://www.raythink-tech.cn/uploadfile/202407/cc84b55e29471bd.pdf?utm_source=chatgpt.com "RM200A 手持测温热像仪 RM200A搭载自研12μm高热灵敏度256×192红外热成像核芯，"
[3]: https://www.raythink-tech.cn/index.php?c=show&id=522&utm_source=chatgpt.com "睿创燧石EX100 SE诚意登场，重塑热像仪入门高标准！_资讯中心_关于我们_燧石技术（烟台）有限公司"
[4]: https://yantai.11467.com/info/45208139.htm?utm_source=chatgpt.com "Raythink燧石技术EX100万用热像仪，暖通、漏水检测"
