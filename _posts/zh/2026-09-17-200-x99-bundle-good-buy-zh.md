---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 200元X99套装：值得购买吗？
translated: true
type: note
---

问题：200元的二手华南金牌X99-AD4 + Xeon E5-2680 v4板U套装值得买吗？

答案：**是的——200元我认为是个好价，前提是你能确认它点亮且主板没问题。** 这个价格足够低，主要风险在于二手主板，而非CPU。

重要规格：

*   **E5-2680 v4：** 14核/28线程，基础频率2.4 GHz，睿频最高3.3 GHz，35 MB缓存，120 W TDP。（[英特尔][1]）
*   **X99-AD4：** LGA2011-3接口，4× DDR4内存插槽，四通道内存，最高128 GB；配备PCIe 3.0 x16插槽和M.2支持。（[Scribd][2]）
*   该商品标价**230元板U套装**，如果属实，卖家200元的报价尤其划算。
*   近期有相同CPU + AD4组合的二手在售，但那些都附带测试/保修，所以不要直接拿它们的要价和这个**“不退不换”**的件对比。（[露天][3]）

### 注意点

卖家说：

> 无挡板，二手成色，不退不换，建议自取。

这个**“不退不换”比缺挡板更关键**。

200元的价格，我不会**盲买然后让人发货**。如果你在广州能自取，那就划算多了，因为你可以付钱前先测试。

我会测试：

```text
1. CPU-Z → CPU识别为E5-2680 v4 / 14C28T
2. BIOS → CPU及所有4个内存插槽均识别
3. MemTest86 / 内存测试 → 最好快速通过
4. Linux:
   lscpu
   free -h
   lspci
5. 压力测试CPU 5–10分钟
6. 检查所有PCIe插槽
7. 检查M.2/SATA
8. 检查USB和网口
9. 重启2–3次
```

**尤其要测试内存插槽。** 廉价X99主板的内存通道/插槽出问题的概率比Xeon本身坏掉要烦人得多。

### 200元到底买了什么？

可以这样看：

```text
E5-2680 v4        ~便宜的普通Xeon
X99-AD4            ~值钱的部分
六热管散热         免费
----------------------------
总计               ¥200
```

这颗**14C/28T的CPU对于CPU并行负载仍然有用**，尤其是编译、虚拟机、批处理、渲染以及大量轻量级进程。但别指望现代单核性能：2.4 GHz基础/3.3 GHz睿频是非常老派的Xeon路子。（[英特尔][1]）

对于**AI工作站**，我会把这颗CPU当作GPU的平台而非算力引擎。现代GPU在实际模型推理/训练上会远超这颗CPU。

### 我能接受的价格

对于测试过的自取件：

```text
¥150       捡漏
¥200       划算
¥230       还算合理
¥250–300   仅限成色很好、已测试、带配件
>¥300      我会开始考虑更新的平台
```

所以 **¥200 + 自取 + 付款前测试 = 我会拿下**。

去之前我会和卖家确认一件事：**200元是否包含E5-2680 v4 + X99-AD4 + 六热管散热器，还是说200元只是板U，散热器只有230元才包含？** 商品描述有点模糊。

如果你需要，我也可以将这套200元的X99配置与**300-500元价位的二手AM4 / Xeon W / 更新的Intel平台**进行对比，并估算CPU/内存/GPU扩展价值。

[1]: https://www.intel.com/content/www/us/en/ark/products/series/91287/intel-xeon-processor-e5-v4-family.html?utm_source=chatgpt.com "Intel® Xeon® Processor E5 v4 Family"
[2]: https://www.scribd.com/document/744700977/HUANANZHI-X99-AD4-User-Manual?utm_source=chatgpt.com "HUANANZHI X99-AD4 User Manual | PDF"
[3]: https://www.ruten.com.tw/item/22518360627327/?utm_source=chatgpt.com "E5-2680 V4 ( 14C28T) CPU+華南金牌 X99-AD4 主機板/ DDR4/M.2/外觀品項新 | 露天市集 | 全台最大的網路購物市集"