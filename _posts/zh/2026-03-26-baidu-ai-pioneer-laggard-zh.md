---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 百度：从人工智能先驱到落后者
translated: true
type: note
---

**Question:** 为什么百度在 AI 和 deep learning 领域起步如此之早（2014 年就拥有大量的 GPU 和人才，处于全球领先地位，甚至曾与 Google 竞购 Geoffrey Hinton 的公司），但现在却落后于 Minimax、Kimi (Moonshot AI) 和 Qwen (Alibaba) 等中国新兴玩家？

**Answer:**

百度在 2010 年代初确实是全球 AI 先驱，这归功于其远见卓识的领导层和对 deep learning 的激进早期投资。然而，由于业务重心的偏移、数据优势的更迭、执行速度以及激烈的市场竞争，百度在生成式 AI 时代难以维持其统治地位。

### 早期的 AI 领导地位 (2012–2017)
- **李彦宏对 deep learning 的豪赌**：百度的 CEO 李彦宏很早就意识到了 deep learning 的潜力。2013 年，百度成立了 Institute of Deep Learning。他们聘请了余凯等顶尖人才，并建立了全球首批大规模 GPU 集群之一用于 deep learning 研究。
- **Andrew Ng 时代 (2014–2017)**：百度挖来了 Google Brain 的联合创始人 Andrew Ng 担任首席科学家。Ng 在 24 小时内就订购并收到了 1,000 块 GPU —— 这比在 Google 的速度快得多 —— 并将 AI 团队扩大到约 1,300 人（包括 300 名研究人员）。百度将 AI 应用于 search、语音识别 (Deep Speech)、图像识别、地图等领域。他们将自己定位为中国 AI 的领导者，甚至在全求范围内展开竞争。
- **竞购 Geoffrey Hinton**：2012–2013 年，在 Hinton 突破性的 AlexNet 论文发表后，百度（与 Google、Microsoft 和 DeepMind 一起）在一场秘密拍卖中竞购 Hinton 及其学生的专业知识（通过一家名为 DNNresearch 的壳公司）。据报道，百度最初出价约 1200 万美元；Google 最终以约 4400 万美元获胜，但百度曾是一个强有力的竞争者，这彰显了百度的雄心。
- **其他优势**：百度在硬件（早期 GPU 集群）上投入巨资，并在硅谷开设了 AI 实验室。他们在语音和 computer vision 等领域处于领先地位，部分项目在当时甚至优于许多西方同行。

百度的优势包括快速反应的企业文化（采购速度快于 Google）、CEO 对 AI 的大力支持，以及中国日益增长的人才库和来自 search 的数据。

### 为什么百度掉队了（尤其是 2022 年生成式 AI 爆发后）
几个结构性和战略性因素解释了这种相对衰落：

1. **核心业务依赖与错过移动/社交转型**：
   - 百度的收入长期由 search 广告主导（约 80-90%）。随着中国互联网转向 mobile apps、社交媒体（微信、抖音）、e-commerce (Alibaba) 和超级应用 (Tencent)，百度的 search 流量和广告业务增长放缓。竞争对手如 Alibaba 和 Tencent 构建了更丰富、更多样化的数据生态系统（电商交易、社交图谱、即时通讯），事实证明这些数据对于训练现代 AI models 更有价值。

2. **对生成式 AI 和 LLMs 的适应较慢**：
   - 百度很早就发布了 Ernie Bot（2023 年 3 月，ChatGPT 发布后不久），声称在中国处于领先地位。然而，它在用户采用率和性能 benchmark 上屡次落后。Ernie Bot 的月活跃用户数远落后于字节跳动的豆包、DeepSeek 等。批评者指出其创新步伐较慢、战略波动（从闭源转向 2025 年开源 Ernie 4.5），以及低估了市场的快速变化。
   - Minimax、Moonshot AI (Kimi)、智谱 AI 和阿里巴巴的 Qwen 系列等新兴玩家凭借敏捷的团队、更好的 product-market fit（例如 Kimi 的长文本推理、Qwen/DeepSeek 强大的开源发布）以及对应用或成本效率的高度专注，移动速度更快。

3. **人才和执行力挑战**：
   - 虽然百度吸引了像 Ng（2017 年离职）这样的明星人才，但在竞争极其激烈的中国 AI 环境中留住顶尖人才一直很困难。许多研究人员流向了 startup 或其他 BAT 公司。监管压力和经济放缓也影响了招聘和士气。
   - 百度强调全栈控制（PaddlePaddle 框架、Kunlun 芯片、Ernie models、Qianfan 平台），但这种闭源/专有方法有时会比竞争对手更开放或应用优先的策略导致迭代变慢。

4. **算力、资金和生态系统动态**：
   - 2014 年，早期的 GPU 获取是一个巨大的优势。今天，由于出口管制限制了 Nvidia GPU 进入中国，迫使企业依赖国产芯片（如百度的 Kunlun）或替代方案。虽然百度投资了自己的芯片并拥有规模化集群，但新兴 startup 获得了巨额融资并采用了更高效的 training 方法（例如据报道 DeepSeek 用更少的资源训练出了强大的模型）。
   - 中国的 AI 热潮催生了数十个资金充足的模型；百度 CEO 甚至警告 LLM 数量“太多”，呼吁关注应用而非原生模型。百度拥有强大的 cloud/AI 基础设施和多模态进展（2025 年的 ERNIE 5.0 是具有强推理能力的原生全模态模型），但变现滞后 —— AI 虽有贡献，但尚未完全抵消广告业务的疲软。

5. **宏观市场压力**：
   - 疫情后的经济放缓影响了广告支出。尽管百度在 AI 方面做出了努力，但其股价表现逊于同行。Search 结果也因 AI 生成的垃圾内容而受到批评，侵蚀了用户信任。
   - 竞争对手：字节跳动利用短视频数据和规模优势；阿里巴巴将 AI 与 cloud/e-commerce 绑定；纯 AI startup 则背负较少的历史包袱。

### 现状 (2025–2026)
百度远未出局。它继续进行大额投资：
- ERNIE 系列（最高 5.0版本）具备多模态能力、agent 特性，并集成了 search、cloud (Qianfan)、Apollo Go (robotaxis) 和数字人。
- 开源了部分 Ernie 以提高采用率。
- 拥有自研 AI 芯片 (Kunlun M 系列) 和全栈生态系统 (PaddlePaddle)。
- AI 现已驱动 cloud 收入的增长和 API 调用（每日达数十亿次），尽管广告业务导致整体收入有所下降。

从技术角度看，百度仍是中国最强大的 AI 公司之一，拥有深厚的专利和基础设施沉淀。然而，在超高速的生成式 AI 竞赛中，敏捷性、数据护城河、产品执行力和专注度让新进入者（Minimax, Kimi, Qwen, DeepSeek）在人气和 benchmark 上实现了赶超。

**简而言之**：百度的早期领先源于“前 LLM”深度学习时代的宏伟愿景、人才挖掘和硬件速度。目前的滞后源于对 search 的过度依赖、向面向消费者的生成式 AI 转型较慢、对手拥有更丰富的数据生态，以及一个 startup 迭代更快的碎片化且竞争极其激烈的中国 AI 市场。百度正在通过应用和多模态模型追赶，但在经济和监管挑战中重新夺回绝对领导地位仍需要持续的执行力。

**References:**
- [Andrew Ng on Baidu AI investments and GPU cluster](https://medium.com/machine-learnings/interview-with-andrew-ng-many-leading-ai-technologies-were-first-deployed-in-china-c5e9f196bb9f)
- [VentureBeat on Ng joining Baidu and early GPU advantage](https://venturebeat.com/business/andrew-ng-baidu)
- [Wired on Hinton auction involving Baidu](https://www.wired.com/story/secret-auction-race-ai-supremacy-google-microsoft-baidu/)
- [CNBC on Baidu's generative AI struggles and competition](https://www.cnbc.com/2025/03/18/baidu-once-chinas-generative-ai-leader-is-battling-to-regain-its-position.html)
- [Baidu's own updates on ERNIE 5.0 and AI strategy](https://www.prnewswire.com/news-releases/baidu-unveils-ernie-5.0-and-a-series-of-ai-applications-at-baidu-world-2025--ramps-up-global-push-302614531.html)