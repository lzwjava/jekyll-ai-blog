---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'TimesFM 3.0: 多变量预测基础模型'
translated: true
type: note
---

问题：**什么是 Google TimesFM 3.0（`google/timesfm-3.0-pytorch`）？**

答案：

**TimesFM 3.0 本质上是一个约 3.3 亿参数的时间序列预测基础模型——可以将其理解为“LLM 风格的预训练模型，但其中的 token 是数值时间序列数据块，而非文本。”** Google 于 **2026 年 8 月 31 日** 发布了该模型。([Google Research][1])

![Image](https://images.openai.com/static-rsc-4/Pt_F0BPCex4-gs5xj1xq0s1rFgt5MBr_u0yos-UK8_uAfVy6cX3rY67Y4F02kguTLWTIK2lbFNSgNqewlr_QcIMtc3LISFIl50gEz22N_WdMnk0BCnK6RiBzb2vyY23LoOwzl7pvZw1f9xEfHMAzrCO9dePy4MXIfWnyDpyHi58ZxZ5RIlfqlUrY8vTdAiFf?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/HDICMDYMia_I4VeaZx-Q3WLTeLs-yak6nfh01u82cXbSF6FHEiIdPutNyD3naOp9YCYkRNmgbXwpb8zIBvvvnDpqHE4B5KN2SgAqJEKSxZeKgyNxyhXiN2isvJVFS2hWINljwdowdD8g60q7oazirCIrhtLrX6C3A5rgiScZw2pO4lzV4G7OQglQvsYBEBL1?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/dp4go55OwzOsy3b-I8odzeMsY9rgEkTmngW-F9BT0XJLGZ-9-CCWlAt3EOrcPl-3muxZPHo3jHhFiz9D7CShcgrfETp32XsCM8QLIzeELmw8qZm_xpiBgyn7Puw6Z7-Hx-uzwk0Jmn98RuE9CO2N3BNyymet39KSVuKfZ8iyw6dZoS20HSbPSPNOvZU2qjt1?purpose=fullsize)

### 1. 重要突破：多变量

早期的 TimesFM 模型主要是**单变量**的：

```text
销售额(t-100 ... t)
        ↓
      TimesFM
        ↓
销售额(t+1 ... t+H)
```

TimesFM 3 能够联合建模多个相关序列：

```text
销售额 ─────────┐
交通流量 ───────┤
温度 ───────────┼──→ TimesFM 3 → 未来销售额 + 交通流量 + ...
促销活动 ───────┤
节假日 ─────────┘
```

这可能是最重要的改进。

它可以处理：

* 多个目标序列
* **仅过去协变量**
* **过去 + 未来协变量**
* 点预测
* 分位数预测

并且是 **零样本** 完成，无需针对特定任务进行微调。([Google Research][1])

---

### 2. 架构

Hugging Face 模型卡片描述为：

```text
堆叠混合 Transformer
    +
变量注意力机制
    +
CPM 迭代 RevIN
```

其参数为：

```text
20 层 Transformer
d_model = 1280
注意力头数 = 16

输入块大小 = 32
输出块大小 = 64
```

检查点约 **0.3B 参数**，以 F32 safetensors 格式分发。([Hugging Face][2])

其概念上的前向传播大致为：

```text
原始时间序列
      ↓
归一化 / RevIN
      ↓
分块为 32 大小的块
      ↓
嵌入
      ↓
Transformer × 20
      ↓
跨变量混合信息
      ↓
预测 64 步块
      ↓
反归一化
      ↓
预测结果
```

因此，它并非简单的 MLP/回归模型。它使用 Transformer 作为**处理数值信号的通用序列模型**。

---

### 3. “基础模型”为何重要

有趣的部分不在于 3.3 亿的参数数量。

而在于**预训练**。

Google 表示 TimesFM 3 在**超过 1 万亿个时间点**上进行了训练，结合了真实世界和合成数据。([Google Research][1])

这带来了与 LLM 相同的基本理念：

```text
预训练一次
    ↓
学习通用时间模式
    ↓
给定新的时间序列
    ↓
无需训练新模型即可预测
```

例如，你可以给它提供：

```python
温度 = [...]
用电量 = [...]
交通流量 = [...]
```

并要求它预测接下来的 24 个点。

你无需为每个新数据集重新训练：

```text
LSTM
XGBoost
Transformer
ARIMA
```

---

### 4. 协变量尤其有用

假设你要预测零售需求。

```text
目标变量：
    冰淇淋销量

过去协变量：
    客流量
    温度

未来已知协变量：
    促销活动
    节假日
    天气预报
```

区分这些类型很重要：

```text
仅过去：
    x[0:T]

过去 + 未来：
    x[0:T+H]
```

TimesFM 3 可以同时使用两者。([Google Research][1])

这使其远比仅能处理以下形式的模型更实用：

```text
y[t-k:t] → y[t:t+H]
```

---

### 5. 极其简单的使用方式

官方仓库展示了大致用法：

```python
import numpy as np

from timesfm3 import TimesFM3Evaluator, ModelConfig

config = ModelConfig(
    checkpoint_path="google/timesfm-3.0-pytorch",
    per_core_batch_size=16,
    device="cuda",
)

model = TimesFM3Evaluator(config)

x = np.random.randn(3, 128).astype(np.float32)

outputs = list(
    model.predict_batch(
        contexts=[x],
        horizon=24,
        return_quantiles=True,
        use_symmetric_averaging=False,
    )
)

forecast = outputs[0].forecast
```

对于：

```text
3 个变量 × 128 个历史数据点
```

你将得到：

```text
3 个变量 × 24 个未来点
```

以及请求的分位数预测（如果指定）。([GitHub][3])

---

### 6. 分位数预测

这是另一个有用的特性。

替代仅输出：

```text
预测[t] = 123
```

你可以获得不确定性信息：

```text
10% ── 105
20% ── 112
...
50% ── 123
...
90% ── 145
```

输出包含对应十分位的 9 个分位数，中位数位于索引 4。([Hugging Face][2])

这比单一点估计有用得多，适用于：

* 库存管理
* 容量规划
* 云/GPU 需求
* 金融风险
* 能源
* 交通流量
* 可观测性

---

### 7. 模型规模如何？

有趣的是，**按 LLM 标准，3.3 亿参数非常小**。

| 模型             | 近似参数量 | 领域       |
| ---------------- | ----------: | ---------- |
| GPT-2 small      |        124M | 语言       |
| TimesFM 3        |    **330M** | 时间序列   |
| TimesFM 2.5      |        200M | 时间序列   |
| 7B LLM           |          7B | 语言       |

Hugging Face 检查点列出的参数约为 0.3B。([Hugging Face][4])

因此，你的 **RTX 4070 12GB** 对于推理来说应该绰绰有余；吞吐量可能是比模型适配更值得关注的限制因素。

---

### 8. TimesFM 3 为何对你来说值得关注

我建议不要把它仅仅看作“又一个预测库”，而是看作：

> **当我们将基础模型范式应用于数值序列时，会发生什么？**

两者的类比惊人地直接：

```text
LLM

数字/文本
    ↓
分词
    ↓
Transformer
    ↓
下一个 token 预测
```

对比：

```text
TimesFM

时间序列
    ↓
分块
    ↓
Transformer
    ↓
未来块预测
```

一个重要的研究问题由此产生：

```text
足够广泛的预训练
能否取代特定任务的时间序列模型？
```

Google 报告称，TimesFM 3 在 **fev-bench、TIME Benchmark 和 GIFT-Eval** 等基准测试中，在比较的基础模型中排名第一。([GitHub][3])

对你的公司而言，一个重要的注意事项：**3.0 版本的预训练权重目前受 Google 非商业许可协议限制**，明确禁止将默认权重用于商业/生产环境。源代码采用 Apache-2.0 许可，但这**并不**意味着 3.0 版本的权重可以商用。([GitHub][3])

[TimesFM 3 Hugging Face 模型](https://huggingface.co/google/timesfm-3.0-pytorch?utm_source=chatgpt.com)
[Google Research — TimesFM 3 公告](https://www.research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/?utm_source=chatgpt.com)
[Google Research TimesFM GitHub](https://github.com/google-research/timesfm?utm_source=chatgpt.com)

我还可以从概念上对 **TimesFM 3 vs TimesFM 2.5 vs Chronos-2 vs TabPFN-TS** 进行基准测试，并展示在您的 4070 显卡上我实际会运行哪一个。

[1]: https://www.research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/?utm_source=chatgpt.com "TimesFM-3: 一个用于多变量预测的零样本基础模型"
[2]: https://huggingface.co/google/timesfm-3.0-pytorch "google/timesfm-3.0-pytorch · Hugging Face"
[3]: https://github.com/google-research/timesfm?utm_source=chatgpt.com "GitHub - google-research/timesfm: TimesFM（时间序列基础模型）是 Google Research 开发的一个用于时间序列预测的预训练基础模型。 · GitHub"
[4]: https://huggingface.co/google/timesfm-3.0-pytorch?utm_source=chatgpt.com "google/timesfm-3.0-pytorch · Hugging Face"