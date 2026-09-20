---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 近期量化交易演变
translated: true
type: note
---

**问题：** 近年来人们如何进行量化交易？像 Jane Street 和 Citadel 这样的公司是否改进了他们的方法？

**答案：**

是的，而且改进显著。过去几年是量化交易在规模和 methodology 上具有里程碑意义的时期。以下是详细分析：

---

### 📈 规模与主导地位

截至 2024 年，算法交易和高频策略已占美国股票交易量的近 65%，而 2010 年这一比例约为 45%。领先公司的规模已增长到几乎难以理解的程度：

- Jane Street 在 2024 年创下 205 亿美元的净交易收入纪录——超过美国银行或花旗集团——其约 3000 名员工实现了 130 亿美元的净利润。Citadel Securities 收入 97 亿美元，增长 55%。
- 2025 年，Jane Street 净交易收入达到 396 亿美元，Hudson River Trading (HRT) 约为 123 亿美元。

---

### 🏦 Jane Street 实际如何盈利

Jane Street 的核心优势在于 **ETF 做市**。2024 年，Jane Street 月均 ETF 交易量达到 7070 亿美元，占据了美国一级市场 24%、美国上市基金二级市场 16% 以及欧洲二级市场活动 17% 的份额。他们还占所有 OCC 期权交易量的 8%。

近期的一大驱动力：2024 年初美国推出现货比特币 ETF，创造了需要 sophisticated 做市商的全新大市场，Jane Street 将自己定位为贝莱德等产品的授权参与方——每当 ETF 价格偏离资产净值时，便捕捉套利机会。

---

### 🤖 方法改进：人工智能与机器学习

这是最大变革正在发生的领域：

**1. LLM 用于 Alpha 发现**
基于提示的 LLM 现被用于自动化 alpha 生成过程——接收特定金融提示，生成与预期预测任务相匹配的公式化信号。这结合了特定领域的金融知识与语言模型的生成能力。

**2. 强化学习 (RL) 用于执行与投资组合优化**
强化学习、预测建模和执行算法正在推动投资组合执行效率的 measurable 改进。自适应 AI 框架——如基于智能体的模型和元学习系统——正在塑造复杂动态环境中的自主交易。

**3. 多智能体 LLM 系统**
最近的研究产生了多个 AI 智能体协作的框架：一个读取新闻/文件，一个生成信号，一个管理风险——所有动作实时协调。像 TradingAgents 和 FLAG-Trader (RL + LLM 融合) 这样的系统代表了这一前沿。

---

### 🏎️ 各家公司的专业化方向

各公司往往有所专长：HRT、Tower、Jump 和 Citadel Securities 侧重于 C++ 系统与超低延迟基础设施；Jane Street、Optiver、SIG 和 IMC 偏好概率论与交易判断；XTX、Two Sigma、AQR 和 WorldQuant 则最侧重于研究/机器学习。

---

### ⚠️ 军备竞赛问题

量化公司面临的核心挑战是 **alpha 衰减**——随着更多资金追逐相同信号，优势逐渐削弱。应对策略是向以下方向推进：
- 更 exotic 的资产类别（加密货币、固定收益 ETF、新兴市场）
- 更快的执行（定制芯片、共置）
- 更好的另类数据（卫星图像、信用卡流、财报电话会议的 NLP 分析）
- 人工智能驱动的 alpha 发现，以寻找人类不会想到去关注的信号

Jane Street 甚至已签约芯片初创公司 Etched 作为其定制 AI 推理芯片的客户，这表明顶级公司对其模型专用硬件的投入程度。

---

**参考文献：**
- [What Is Quant Trading? A Complete 2026 Guide - Tradermath](https://www.tradermath.org/articles/what-is-quant-trading)
- [Top HFT and Prop Trading Firms in 2026 - QuantInsti](https://www.quantinsti.com/articles/hft-prop-trading-firms/)
- [Jane Street took 10% of US equity market in 2024 - Global Trading](https://www.globaltrading.net/?p=38181)
- [Adaptive Alpha Weighting with PPO - arXiv](https://arxiv.org/html/2509.01393)
- [Jane Street Institutional Services](https://www.janestreet.com/institutional-services/)