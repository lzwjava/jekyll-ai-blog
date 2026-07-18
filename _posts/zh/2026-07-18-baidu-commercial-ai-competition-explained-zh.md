---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 百度商业AI竞赛解析
translated: true
type: note
---

问题：什么是CTI（百度商业智能大赛）？

答案：

此处CTI指的是**百度商业AI技术创新大赛**（Baidu Commercial AI Technology Innovation Competition），而非常见的"计算机电话集成"或"网络威胁情报"等含义。（[cti.baidu.com][1]）

这是由百度商业AI团队主办的AI竞赛，旨在探索**产业AI+商业场景**，尤其聚焦推荐、广告、大模型优化及AI工程人才。大赛始于2023年，面向高校、科研院所及行业从业者开放。（[cti.baidu.com][1]）

其独特之处在于并非纯粹的Kaggle式精度竞赛，而是更贴近**真实世界的AI工程实践**：

### 典型赛道

**1. 商业预测/推荐**

* 用户行为预测
* CTR（点击率）预测
* 转化率预测
* 广告排序模型

示例：

```
用户历史
     |
     v
嵌入层 + 特征
     |
     v
Transformer / DeepFM / DIN / DLRM
     |
     v
P(点击 | 用户, 广告)
```

目标是最大化CTR/CVR等商业指标。（[cti.baidu.com][2]）

**2. 大模型推理优化**

更偏重AI基础设施：

```
大语言模型
   |
   +-- 量化
   +-- KV缓存优化
   +-- CUDA内核
   +-- 批处理
   +-- 内存优化
   |
   v
更低延迟 / 更高吞吐量
```

例如，2023年赛事包含AIGC推理优化，重点提升大模型服务效率。（[cti.baidu.com][2]）

**3. 生成式推荐/广告**

近期赛事向以下方向演进：

* 基于Transformer的推荐
* 生成式排序
* 长用户行为序列建模
* 高性能推理

2026年竞赛聚焦"生成式推荐广告排序推理性能优化"。（[cti.baidu.com][1]）

对于您这种背景（nanoGPT、GPT-2训练、GPU/ROCm实验），有趣的部分可能**并非传统推荐模型**，而是：

```
AI基础设施
    |
    +-- vLLM风格服务
    +-- CUDA/ROCm优化
    +-- 量化
    +-- 分布式推理
    +-- 模型压缩
```

这实际上更接近企业需求：

* 精度高1%但GPU成本高10倍的模型 → 糟糕
* 精度达95%但服务成本降低100倍的模型 → 有价值

商业AI本质上是优化问题：

[
\text{商业价值} =
\frac{\text{模型质量} \times \text{流量}}{\text{计算成本} \times \text{延迟}}
]

该竞赛本质上就是训练人们解决这个方程式。（[cti.baidu.com][2]）

参考资料：

* 百度商业AI技术创新大赛官网（[cti.baidu.com][1]）
* 2023百度商业AI技术创新大赛介绍（[cti.baidu.com][2]）

[1]: https://cti.baidu.com/?utm_source=chatgpt.com "百度商业AI技术创新大赛"
[2]: https://cti.baidu.com/2023/index.html?utm_source=chatgpt.com "百度商业AI技术创新大赛"
