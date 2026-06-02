---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 月球引力产生海洋潮汐
translated: true
type: note
---

Question: 为什么会产生潮汐？根据 Richard Feynman 的书中所述，Moon 的 gravity 是如何导致潮汐的？

Answer:

潮汐是由于 Moon（以及较小程度上的 Sun）产生的 **gravitational forces** 导致的海平面周期性升降。其关键不在于对 Earth 的整体引力（整体引力使 Earth 绕着与 Moon 的共同中心运行），而是在于 Earth 直径范围内的引力强度**差异**——这被称为 **tidal force** 或 **differential gravity**。

### Tidal Force 的原理
Moon 的 gravity 对 Earth 朝向它的一侧（离 Moon 较近）的拉力比对 Earth 中心的拉力更强，而对背向它的一侧（离 Moon 较远）的拉力则更弱。

- **近月端 (Facing the Moon)** — 海水受到的拉力比固体 Earth 更强，从而形成一个隆起（high tide）。
- **远月端 (Opposite the Moon)** — 固体 Earth 受到的拉力比远端的海水更强，因此海水被“留在后面”，形成了另一个隆起（high tide）。
- **垂直的一侧** — Gravity 略微向内拉，形成了 low tides。

这导致在 Earth 相反的两侧产生了两个与 Moon 对齐的 **high-tide bulges**。

随着 Earth 每日自转，大多数地点会经过这两个隆起区域，大约每 24 小时 50 分钟（一个 lunar day）经历 **两次 high tides 和两次 low tides**。

### Richard Feynman 的解释
在 *The Feynman Lectures on Physics*（第一卷，第 7 章）及相关演讲中，Feynman 使用 gravitational gradient 解释了这一现象。

他指出了一些早期的误解：
- 有人认为只有一个潮汐（就在 Moon 下方）。
- 另一些人错误地认为 Earth 在远端被拉离了海水。

Feynman 澄清道，Moon 的拉力在 Earth 中心达到平衡，但在近月端更强，在远月端更弱，从而将 Earth 轻微拉伸成一个带有两个隆起的 ellipsoid。

Feynman 的一些诠释提到了旋转坐标系（Earth-Moon 绕共同中心运行）中的 centrifugal force，其中向外的 centrifugal force 是均匀的，与变化的 gravity 结合产生了同样的隆起。然而，根本原因还是 **differential gravitational pull**。

### Sun 的作用
Sun 也会引起潮汐，但其作用约为 Moon 的 45%，因为尽管 Sun 的质量更大，但它距离太远（tidal force 随着距离的立方而减小）。

当 Sun、Moon 和 Earth 连成一线（满月或新月）时，潮汐叠加形成 **spring tides**（更高的高潮，更低的低潮）。当它们处于垂直位置（弦月）时，作用部分抵消，形成 **neap tides**（潮差较小）。

在现实中，由于大陆分布、海洋深度和 Earth 自转，潮汐变得更加复杂，但基本机制就是这种引力拉伸作用。

References:

- [The Feynman Lectures on Physics, Vol. I, Ch. 7: The Theory of Gravitation](https://www.feynmanlectures.caltech.edu/I_07.html)
- [Tidal force - Wikipedia](https://en.wikipedia.org/wiki/Tidal_force)
- [Gravity, Inertia, and the Two Bulges - NOAA](https://oceanservice.noaa.gov/education/tutorial_tides/tides03_gravity.html)
- [Tides - NASA Science](https://science.nasa.gov/moon/tides/)
