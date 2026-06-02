---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 小马智行：从“观察”到“实践”
translated: true
type: note
---

问题：楼天城如何带领小马智行团队从“观察式学习”转向“实践式学习”？

回答：

小马智行（Pony.ai）联合创始人兼首席技术官楼天城在2019年前后主导了公司自动驾驶开发方法上的转型。最初，小马智行的策略与行业规范类似，严重依赖真实世界的数据收集和模仿学习——本质上是“观察式学习”，即AI系统被动地观察并复制人类驾驶员在海量数据集中的行为。这种方法在早期的自动驾驶项目中很常见，将驾驶视为一种模式匹配练习，但随着数据量的增长，性能提升却不成比例，回报逐渐递减。

楼天城认识到这一瓶颈，将其描述为一道“无形之墙”，即额外的真实世界数据无法带来突破。为此，他做出了一个大胆的领导决策：舍弃三年积累的技术，从头开始重建核心框架。这一转变引入了“世界模型”（world model）架构，强调高保真虚拟仿真。在这种架构下，AI智能体可以在可控、可扩展的环境中无休止地“练习”驾驶场景，通过在模拟世界中主动强化和试错，迭代出超越人类极限的最佳行为——从而转向“实践式学习”。

在楼天城的指导下，团队将这一方法与先进的强化学习技术相结合，使系统能够自主生成合成数据并优化策略。这不仅加速了开发进程，还提高了安全性和效率，使小马智行能够实现L4级自动驾驶出租车（robotaxi）运营等里程碑，累计无干预驾驶时数超过10,000小时。他多年的竞技编程背景——通过在编程挑战中快速迭代而磨练出来——影响了这种亲力亲为、实验至上的精神，培养了一种团队优先考虑可衡量结果而非理论积累的文化。

参考文献：
- [Inside Pony.ai’s staying power and the mindset of its CTO, Lou Tiancheng](https://kr-asia.com/inside-pony-ais-staying-power-and-the-mindset-of-its-cto-lou-tiancheng)
- [Tiancheng Lou - Wikipedia](https://en.wikipedia.org/wiki/Tiancheng_Lou)
