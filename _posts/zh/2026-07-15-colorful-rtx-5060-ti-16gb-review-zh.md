---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 七彩虹 RTX 5060 Ti 16GB 评测
translated: true
type: note
---

问题：这张卡是什么——七彩虹（Colorful）iGame GeForce RTX 5060 Ti Ultra OC 16GB GDDR7？

答案：

这是七彩虹的中端Blackwell显卡，采用GB206核心，面向1440p游戏。请注意：它实际上是**DLSS 4**（多帧生成 + 基于Transformer模型的超分辨率/光线重建），而不是"DLSS 4.5"——列表中的那个数字只是营销噱头，官方并无此版本。

**核心**

- GPU：GB206（Blackwell 2.0），4N工艺，181mm²，219亿晶体管
- CUDA核心：4608，RT核心：36，Tensor核心：144
- 频率：基础2407MHz / 加速2572MHz（默认），一键超频2632MHz
- FP32性能：约24.3 TFLOPS

**显存**

- 16GB GDDR7，128位位宽，等效28Gbps，峰值带宽448 GB/s
- 这是与8GB版本的重要区别——128位位宽较窄，但GDDR7速度弥补了这一点

**功耗与散热**

- TDP 180W，单8-pin供电接口，建议电源600W（部分列表显示最低450W——600W是七彩虹的保守建议）
- 三风扇散热，2.5槽厚度，300.5×120×50mm，重0.97kg

**输出接口**

- 3×DisplayPort 2.1b + 1×HDMI 2.1b

**性能对比**——1440p下比RTX 3060快约75%，比RTX 4060 Ti快约26%，但仍不及RTX 4070，RTX 5070则快约27%。因此：这是一款扎实的1440p显卡，并非RTX 4070杀手。

对于你的使用场景——如果你打算将其作为廉价的本地推理设备：16GB显存搭配448GB/s带宽（128位位宽）对于小型量化模型（7B-13B Q4/Q5）是可以用的，但与二手3090（936GB/s，24GB）相比带宽明显不足。适合推理测试，不适合训练/微调的高吞吐量场景。

参考链接：

- [BenchGame — Colorful iGame RTX 5060 Ti Ultra W 16GB规格](https://benchgame.com/graphics-card/colorful-igame-rtx-5060-ti-ultra-w-16-gb)
- [TweakTown评测](https://www.tweaktown.com/reviews/11042/colorful-igame-geforce-rtx-5060-ti-ultra-oc-style-meets-great-performance/index.html)
- [DataBlitz产品页面 — 完整规格表](https://ecommerce.datablitz.com.ph/products/colorful-igame-geforce-rtx-5060-ti-ultra-w-oc-16gb-v-gddr7-graphics-card)
