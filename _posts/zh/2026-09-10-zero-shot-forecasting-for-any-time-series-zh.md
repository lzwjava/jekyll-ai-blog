---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 任意时间序列的零样本预测
translated: true
type: note
---

问题：**TimesFM-3 实际有什么用？它能支持哪些应用？**

答案：**只要你有测量数据流并需要预测接下来会发生什么，它就能派上用场。** 可以把它看作是一个面向数值时间序列的 LLM。

TimesFM-3 的杀手级特性并非仅仅是“预测”。而是：

> **给它一个从未见过的新时间序列数据集，无需为这个数据集训练模型，就能得到一个有用的预测结果。**

谷歌表示，TimesFM-3 专为多变量预测设计，能够联合使用相关序列以及历史和未来的已知协变量。([Google Research][1])

### 具体应用

| 应用              | 输入                               | 预测                         |
| :---------------- | :--------------------------------- | :--------------------------- |
| 🛒 电子商务       | 历史销量、流量、促销活动           | 次日/下周/下月销量           |
| 📦 库存管理       | 销量 + 库存 + 交货周期             | 未来需求 / 缺货风险          |
| ⚡ 电力           | 历史负荷 + 天气数据                 | 未来电力需求                 |
| 💰 金融           | 价格、成交量、利率                 | 未来数值 / 区间              |
| 🏭 制造业         | 机器传感器数据                     | 未来传感器变化趋势           |
| 🖥️ 云/AI 基础设施 | GPU 利用率、请求量、延迟           | 未来工作负载                 |
| 🌐 可观测性       | CPU、内存、QPS、错误数             | 未来系统行为                 |
| 🚚 物流           | 订单量、交通、运力                 | 未来需求                     |
| 🏥 医疗健康       | 患者随时间变化的测量数据           | 未来测量值                   |
| 🌦️ 天气/环境      | 温度、湿度等                       | 未来测量值                   |

谷歌明确列出了**零售、金融、可观测性、制造业、医疗健康和自然科学**作为时间序列基础模型的实际应用领域。([Google Research][2])

### 一个真正有趣的例子

假设你运营着一个 GPU 集群：

```text
时间 ──────────────────────────────>

GPU 利用率        ▁▂▃▅▇▆▅▇▇▆▅
请求 QPS          ▁▂▃▄▆▅▅▇▇▆▅
队列长度          ▁▁▂▃▆▅▄▇▆▅▄
功耗              ▂▂▃▄▆▅▅▇▇▆▅
```

你想要得到：

```text
未来 1 小时 / 6 小时 / 24 小时
```

TimesFM-3 可以联合预测这些信号，而不是单独预测每个信号。

然后你可以构建：

```text
TimesFM-3
    ↓
预测 GPU 需求
    ↓
预测饱和概率
    ↓
启停 GPU 实例
    ↓
调度训练任务
    ↓
避免队列爆炸
```

这是一个**非常实用的 AI 代理 + 时间序列组合**。

---

## 最有价值的功能：未来已知信息

想象一个在线商店。

历史数据：

```text
销量
流量
价格
```

但你也知道：

```text
9月15日 → 促销活动
9月20日 → 节假日
9月25日 → 促销活动
```

那么：

```text
销量 ────────────────→ ?
流量 ──────────────→ ?
价格 ────────────────→ ?
促销活动 ────────────→ 已知未来
节假日 ──────────────→ 已知未来
```

TimesFM-3 可以利用这些未来协变量。

所以，你得到的不是：

```text
“根据过去数据，销量可能为 10,000。”
```

而是：

```text
普通日子      → 10,000
促销日        → 12,000
节假日        → 14,000
```

谷歌自己的示例就展示了促销计划如何导致预测销量提升。([Google Research][1])

---

## 另一个有用的应用：异常检测

TimesFM 本身不是异常检测器，但你可以将其概率预测转化为异常检测功能。

假设：

```text
预测结果：

第10百分位 = 80
第50百分位 = 100
第90百分位 = 120
```

而实际值突然变成：

```text
实际值 = 190
```

那么：

```text
190 >> 第90百分位
```

→ 可疑。

因此你可以构建：

```text
指标
   ↓
TimesFM
   ↓
预测区间
   ↓
实际值超出区间？
   ↓
告警
   ↓
LLM 代理调查日志
```

TimesFM 项目本身记录了这种方法。([GitHub][3])

这对于**DevOps / AI 基础设施可观测性**来说尤其有趣。

---

## 我认为这对你来说有意思的地方

你可以构建一个微型的**AI 基础设施预测器**：

```text
Prometheus
    │
    ├── GPU 利用率
    ├── 显存
    ├── CPU
    ├── 请求/秒
    ├── 队列长度
    ├── 延迟
    └── 功耗
          │
          ▼
      TimesFM-3
          │
          ├── 10分钟预测
          ├── 1小时预测
          ├── 6小时预测
          └── 不确定性
                  │
                  ▼
             代理
          ┌───────┴────────┐
          │                │
      扩展GPU容量        调查异常
```

这比简单地询问“明天股价会是多少？”要有趣得多。

因为**预测 + 行动**创造了一个真正的代理系统。

需要注意一点：虽然源代码采用 Apache-2.0 许可证，但已发布的 **TimesFM-3 权重目前为非商业/非生产许可证**。因此，对于你的公司，建议将其用于研究/基准测试，而不是暗中将预训练权重用于生产服务。([GitHub][4])

**一句话总结：** TimesFM-3 的用途在于将“一堆历史数值信号”转化为“接下来可能发生的情况（包括不确定性）”，特别是在多个信号相互影响的情况下。

[1]: https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/?utm_source=chatgpt.com "TimesFM-3: A zero-shot foundation model for multivariate forecasting"
[2]: https://www.research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/?utm_source=chatgpt.com "TimesFM-3: A zero-shot foundation model for multivariate forecasting"
[3]: https://github.com/google-research/timesfm/blob/master/timesfm-forecasting/SKILL.md?utm_source=chatgpt.com "timesfm/timesfm-forecasting/SKILL.md at master · google-research/timesfm · GitHub"
[4]: https://github.com/google-research/timesfm?utm_source=chatgpt.com "GitHub - google-research/timesfm: TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting. · GitHub"
