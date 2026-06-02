---
audio: false
generated: true
lang: zh
layout: post
title: 使用线性回归进行交易
translated: true
type: note
---

很好的问题！你这里结合了两个任务：

1. **使用 TigerOpen API 获取历史股票数据（如腾讯）**
2. **将该数据与你现有的基于 numpy 的线性回归代码结合使用**

---

## 现有代码能直接使用吗？

**不能直接使用。** 你当前的机器学习代码期望 `x_train` 和 `y_train` 是代表特征和标签（例如人口 vs 利润）的数值型 numpy 数组。但 TigerOpen API 返回的是**历史股票 K 线数据**，这是一个包含每个时间戳多个字段的时间序列。

你需要：

- 正确提取并预处理股票数据，将其转换为合适的 `x_train` 和 `y_train` 数组。
- 使你的模型和代码适应股票数据的上下文（例如，根据前几天的数据预测收盘价）。

---

## 如何调整股票数据以适配你的线性回归模型？

### 步骤 1：获取腾讯（代码 `'00700'`）的历史数据

```python
bars_dict = quote_client.get_bars(
    symbols=['00700'],
    period=BarPeriod.DAY,
    begin_time='2024-01-01',
    end_time=datetime.now().strftime('%Y-%m-%d'),
    limit=100,
    right=QuoteRight.BR
)

bars = bars_dict.get('00700', [])
```

### 步骤 2：提取特征和标签

一个简单的方法是：

- 使用天数索引作为 `x_train`（例如 0, 1, 2, ...）
- 使用收盘价作为 `y_train`

```python
import numpy as np

x_train = np.array([i for i in range(len(bars))])
y_train = np.array([bar.close for bar in bars])
```

或者，你可以使用前一天的收盘价作为特征来预测第二天的收盘价，或者使用更复杂的特征。

### 步骤 3：使用你的线性回归代码

现在你的 `x_train` 和 `y_train` 是数值型的 numpy 数组，在你修复了 `compute_cost` 和 `compute_gradient` 函数（它们目前返回零或零梯度）之后，你的代码应该可以正常工作。

---

## 示例：实现 compute_cost 和 compute_gradient

```python
def compute_cost(x, y, w, b):
    m = x.shape[0]
    total_cost = 0.5 * np.sum((w * x + b - y) ** 2) / m
    return total_cost

def compute_gradient(x, y, w, b):
    m = x.shape[0]
    error = w * x + b - y
    dj_dw = np.sum(error * x) / m
    dj_db = np.sum(error) / m
    return dj_dw, dj_db
```

---

## 总结

- 使用 TigerOpen API 获取历史股票数据
- 将时间序列数据转换为数值数组（`x_train`, `y_train`）
- 实现或修复你的成本函数和梯度函数
- 然后你的梯度下降和绘图代码将能够工作，以将线性模型拟合到股票价格数据

---

## 附加：绘制股票价格图

你的散点图将显示每日收盘价，回归线将拟合其趋势。

---

如果你需要，我可以帮你编写一个完整的示例，将 TigerOpen 数据获取与你的 numpy 线性回归代码集成起来！尽管提出。
