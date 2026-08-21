---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 多模光纤简单解释
translated: true
type: note
---

问题：在光纤背景下，“multimode”（多模）是什么意思？

回答：

“Multimode”（多模）指的是能够同时承载**多条光线（模式）**的光纤，每条光线以略微不同的角度在纤芯中传输。

**主要特点：**

- **大纤芯直径** — 通常为 50 µm 或 62.5 µm，使光更容易耦合进光纤
- **短距离** — 最适合 2 公里以内的距离（通常在建筑物或园区内）
- **光源** — 使用 LED 或短波长激光（850 nm），成本较低
- **模式色散** — 由于不同模式到达时间略有差异，信号在长距离传输时会劣化

**与单模光纤对比：**

| 特性 | 多模 | 单模 |
| --- | --- | --- |
| 纤芯直径 | 50 / 62.5 µm | 8–10 µm |
| 光源 | LED / 850nm 激光 | 1300–1550nm 激光 |
| 最大距离 | ~550m（千兆） | 可达 100+ 公里 |
| 成本 | 较低 | 较高 |
| 应用场景 | 局域网、数据中心 | 广域网、长距离传输 |

**简单类比：** 可以将多模光纤想象成一条宽阔的高速公路，多辆汽车（光线）同时在不同的车道上行驶——短途出行效率高，但长途行驶容易出现拥堵（信号色散）。单模光纤则像一条狭窄的单车道，每次只能通行一辆车，但长距离行驶不会出现拥堵。

参考资料：

- [多模光纤 – Fiber Optic Association](https://www.thefoa.org/tech/ref/fiber/multimode.html)
- [多模与单模光纤对比 – FS.com](https://community.fs.com/article/single-mode-cabling-cost-vs-multimode-cabling-cost.html)
