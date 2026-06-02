---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 热门手机游戏背后的游戏引擎
translated: true
type: note
---

**问题：PUBG Mobile、《王者荣耀》和《原神》背后的底层技术（特别是游戏引擎）是什么？它们是否使用了虚幻引擎？**

**回答：**

这些热门手机游戏的核心开发、渲染、物理和跨平台支持主要依赖于成熟的游戏引擎。以下是详细分类：

| 游戏              | 游戏引擎     | 主要说明 |
|-------------------|-----------------|-----------|
| **PUBG Mobile**  | Unreal Engine 4 | 是的，基于虚幻引擎4的移动优化版本（约4.18版）。由光子工作室群（腾讯）和PUBG Studios（Krafton）开发。PUBG PC版正在过渡到Unreal Engine 5，但移动版为了在移动硬件上的性能仍保留在UE4上。 |
| **Honor of Kings** (王者荣耀) | Unity          | 未使用虚幻引擎。其客户端开发使用Unity 3D引擎。这与其国际版Arena of Valor使用相同的引擎。衍生作品《王者荣耀：世界》使用Unreal Engine 5，但核心MOBA手机游戏没有。 |
| **Genshin Impact** | Unity         | 未使用虚幻引擎。由米哈游（HoYoverse）使用高度定制的Unity引擎开发。这使其能够在移动、PC和主机平台上实现开放世界功能。米哈游未来的项目可能会转向Unreal Engine 5，但《原神》仍保留在Unity上。 |

**底层技术总结：**
- **Unreal Engine**：非常适合高保真图形和射击游戏，例如PUBG Mobile，具有强大的移动优化能力。
- **Unity**：由于其轻量级、易于进行跨平台部署（Android/iOS）和资源生态系统，非常适合像《王者荣耀》和《原神》这样的移动MOBA和开放世界游戏。

截至2025年末，暂无重大引擎变更报告。

**参考资料：**
- [PUBG Mobile - Wikipedia](https://en.wikipedia.org/wiki/PUBG_Mobile)
- [PUBG MOBILE \| LIGHTSPEED STUDIOS](https://www.lightspeed-studios.com/gamedetail/pubg-mobile.html)
- [Arena of Valor - Official Arena of Valor Wiki](https://arenaofvalor.fandom.com/wiki/Arena_of_Valor)
- [王者荣耀采用了一些什么技术开发的？ - 知乎](https://zhuanlan.zhihu.com/p/566696979)
- [《王者荣耀》背后的游戏引擎不简单 - 界面新闻](https://www.jiemian.com/article/2142239.html)
- [Genshin Impact - Wikipedia](https://en.wikipedia.org/wiki/Genshin_Impact)
