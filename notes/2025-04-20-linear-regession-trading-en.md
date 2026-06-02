---
audio: false
generated: true
lang: en
layout: post
title: Using Linear Regession to Trade
translated: false
type: note
---

Great question! You're combining two tasks here:

1. **Fetching historical stock data (e.g., Tencent) using TigerOpen API**
2. **Using that data with your existing numpy-based linear regression code**

---

## Will it work as-is?

**No, not directly.** Your current ML code expects `x_train` and `y_train` as numpy arrays of numeric values representing features and labels (e.g., population vs. profit). But the TigerOpen API returns **historical stock bars** (OHLCV data), which is a time series with multiple fields per timestamp.

You need to:

- Properly extract and preprocess the stock data into suitable `x_train` and `y_train` arrays.
- Adapt your model and code to the stock data context (e.g., predict closing price from previous days).

---

## How to adapt your stock data for your linear regression model?

### Step 1: Fetch historical data for Tencent (symbol `'00700'`)

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

### Step 2: Extract features and labels

A simple approach:

- Use the day index as `x_train` (e.g., 0, 1, 2, ...)
- Use the closing price as `y_train`

```python
import numpy as np

x_train = np.array([i for i in range(len(bars))])
y_train = np.array([bar.close for bar in bars])
```

Alternatively, you can use previous day's close as feature to predict next day's close, or more sophisticated features.

### Step 3: Use your linear regression code

Now your `x_train` and `y_train` are numpy arrays of numbers, so your code should work fine after you fix your `compute_cost` and `compute_gradient` functions (which currently return zero or zero gradients).

---

## Example: Implement compute_cost and compute_gradient

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

## Summary

- Fetch historical stock data with TigerOpen API
- Convert the time series data into numeric arrays (`x_train`, `y_train`)
- Implement or fix your cost and gradient functions
- Then your gradient descent and plotting code will work to fit a linear model to stock price data

---

## Bonus: Plotting stock prices

Your scatter plot will show the closing price over days, and the regression line will fit a trend.

---

If you want, I can help you write a complete example integrating TigerOpen data fetching with your numpy linear regression code! Just ask.
