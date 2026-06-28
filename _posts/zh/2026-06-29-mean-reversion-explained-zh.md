---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 均值回归解析
translated: true
type: note
---

问题："均值回归"是什么意思？

答案：

均值回归是指一个序列在偏离其长期均值后，有统计学上的趋势向该均值回归。形式上：如果 `x_t` 远高于 `μ`，则下一步的期望移动 `E[x_{t+1} - x_t]` 为负，反之亦然。回归的强度随偏差的大小而变化。

经典的连续时间模型是 **Ornstein–Uhlenbeck 过程**：

```
dx_t = θ(μ - x_t) dt + σ dW_t
```

- `μ` — 序列回归的长期均值
- `θ` — 回归速度（θ 越大，回弹越快）；偏差的半衰期为 `ln(2)/θ`
- `σ` — 波动率
- `dW_t` — 布朗噪声

离散化后，它就是一个 AR(1)：

```python
import numpy as np

def ou(n=1000, theta=0.1, mu=0.0, sigma=0.2, x0=2.0, dt=1.0):
    x = np.empty(n); x[0] = x0
    for t in range(1, n):
        x[t] = x[t-1] + theta*(mu - x[t-1])*dt + sigma*np.sqrt(dt)*np.random.randn()
    return x
```

注意 `x[t] = (1 - θ)·x[t-1] + θ·μ + noise` —— 系数 `(1-θ) < 1` 保证了回归。如果该系数 ≥ 1，则序列是随机游走（无回归）或爆炸性的。

**它在哪些地方出现：**
- *量化交易* — 配对交易/统计套利：交易两个协整资产之间的价差，押注其回归均值。用 ADF 检验平稳性；通过 AR(1) 的 OLS 估计 θ。
- *波动率/利率模型* — 利率的 Vasicek、CIR 模型使用 OU 动力学。
- *业绩归因* — "均值回归"：极端异常值之后往往跟随不那么极端的值，这是一种纯粹的抽样假象，而非某种驱动力。

其镜像行为是 **动量/趋势**，即偏差持续或累积而非衰减（系数 ≥ 1）。

快速均值回归检验 —— 拟合 AR(1)，检查斜率是否显著小于 1：

```python
from statsmodels.regression.linear_model import OLS
import statsmodels.api as sm

x = ou()
X = sm.add_constant(x[:-1])
beta = OLS(x[1:], X).fit().params[1]   # < 1 ⇒ 均值回归
half_life = -np.log(2) / np.log(beta)  # 步数
```