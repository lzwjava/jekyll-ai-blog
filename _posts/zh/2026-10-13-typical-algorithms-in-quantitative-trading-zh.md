---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 量化交易中的典型算法
translated: true
type: note
---

**问题：** 量化交易中使用的典型算法有哪些——例如 DeepSeek（High-Flyer Capital）、机器学习驱动的基金以及 Jane Street 等公司所使用的算法？

---

**回答：**

量化交易算法通常分为几个层面——**alpha generation**、**execution** 和 **risk management**——每个层面都有各自的技术。

---

## 1. 经典统计/数学策略

这些即使在尖端公司也仍然是基础：

| 策略 | 核心思想 |
| --- | --- |
| **Mean Reversion** | 价格偏离均衡 → 回归均值（配对交易、统计套利） |
| **Momentum / Trend** | 资产朝一个方向趋势 → 跟随趋势 |
| **Factor Models** | Fama-French 风格的风险溢价暴露（价值、规模、质量等） |
| **Statistical Arbitrage** | 协整配对或篮子 → 利用暂时错误定价 |
| **Market Making** | 持续报价买/卖，通过买卖价差和库存控制获利 |

---

## 2. 机器学习方法

这是现代量化基金（Two Sigma、DE Shaw、High-Flyer/DeepSeek）的区别所在：

### 监督学习（Alpha 预测）

- **Tree ensembles**：XGBoost、LightGBM——横截面 alpha 的行业主力；可解释性强，能很好地处理非线性
- **带正则化的线性模型**：LASSO/Ridge 用于在数百个信号中进行特征选择
- **神经网络（MLP、ResNet）**：表格金融数据预测

### 序列/时间序列模型

- **LSTM / GRU**：捕捉价格/成交量序列中的时间依赖性
- **Transformers（Attention）**：应用于逐笔数据、订单簿快照或跨资产相关性——2020 年后越来越流行

### 强化学习（执行与策略）

- 训练智能体以优化订单执行（最小化市场冲击）或投资组合再平衡
- DeepMind 风格的强化学习被 Goldman Sachs 和 Citadel 等公司用于最优执行

### NLP / LLM 信号

- 来自财报电话会议、新闻通讯、Reddit/X（原 Twitter）的情绪
- **DeepSeek 的母公司 High-Flyer（幻方科技）** 大量利用大型语言模型进行另类数据信号提取——他们构建 DeepSeek 的部分原因就是为了降低这些工作负载的 GPU 成本

---

## 3. 高频交易（HFT）算法

由 Virtu、Optiver、IMC 以及 Jane Street 在某些产品线中使用：

- **订单簿建模**：基于 L2/L3 订单簿动态预测短期价格方向
- **延迟套利**：竞速抢先跨场所的价格差异进行套利
- **成交概率模型**：预测被动限价单是否会成交的 ML 模型
- **队列位置建模**：用于订单到达/队列动态的泊松过程

---

## 4. Jane Street 特别介绍

Jane Street 更偏向**概率推理 + 市场微观结构**，而不是“ML-first”：

- **期权和 ETF 做市**：他们在全球范围内主导 ETF 套利和期权做市
- **Kelly Criterion / Bayesian updating**：根据边际优势 × 概率实时调整仓位
- **系统化自由裁量**：量化模型提供信息，但人在压力市场中经常进行干预
- 他们的技术栈以 **OCaml** 闻名——他们更看重正确性和推理速度，而非纯粹的 ML 火力
- 他们大力招聘**数学概率**和**博弈论**方面的人才

---

## 5. DeepSeek / High-Flyer Capital 的方法

High-Flyer 开创了深度学习在中国 A 股市场的应用（大约 2015 年起）：

- **端到端深度学习**：原始 OHLCV + 订单簿数据 → 通过神经网络直接生成 alpha 信号
- **非常大的特征集**：数千个技术和另类数据特征输入梯度提升 + 神经集成
- **GPU 集群**：他们构建了中国最大的私有 GPU 集群之一，专门用于模型训练
- DeepSeek（LLM 实验室）的拆分部分是为了开发高效 AI 基础设施，并反哺交易模型开发

---

## 快速对比

| 公司类型 | 主要方法 | 优势 |
| --- | --- | --- |
| **Renaissance / Two Sigma** | 统计模式 + ML 集成 | 数据广度 + 信号多样性 |
| **Jane Street / Optiver** | 做市 + 概率模型 | 微观结构专业知识 |
| **High-Flyer (DeepSeek)** | 价格/另类数据的深度学习 | 神经网络 + GPU 规模 |
| **Citadel Securities** | HFT + 做市 + 统计套利 | 延迟 + 跨资产范围 |
| **DE Shaw** | 系统性多策略 | 策略广度 + 风险管理 |

---

这些公司真正的“秘密武器”并不是某个单一算法，而是**数据质量、特征工程、稳健的回测基础设施和严格的风险管理的结合**。

---

**参考资料：**

- [Advances in Financial Machine Learning – Marcos López de Prado](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086)
- [Jane Street: How We Think About Markets](https://www.janestreet.com/what-we-do/)
- [High-Flyer Capital / DeepSeek Background](https://www.reuters.com/technology/chinas-deepseek-ai-was-trained-high-flyer-quant-funds-gpu-cluster-2025-01-29/)
- [Two Sigma: Data Science in Finance](https://www.twosigma.com/articles/)
- [QuantLib & Academic Papers on Execution Algorithms (Almgren-Chriss)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=488769)
