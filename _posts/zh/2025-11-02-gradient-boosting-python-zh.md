---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Python梯度提升基础示例
translated: true
type: note
---

### Python 中的简单梯度提升示例

以下是使用 scikit-learn 的 `GradientBoostingRegressor` 在玩具回归数据集上实现 Friedman 梯度提升机的基础示例。这体现了 2001 年论文中的核心思想：通过收缩正则化，顺序拟合树模型到伪残差。

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# 步骤 1：生成合成数据（类似论文中的回归示例）
X, y = make_regression(n_samples=1000, n_features=10, noise=0.1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 步骤 2：初始化并训练 GBM
# 关键参数参考论文：n_estimators=1000（多次迭代），learning_rate=0.1（收缩率），
# max_depth=3（浅层树作为弱学习器），subsample=0.5（随机变体）
gbm = GradientBoostingRegressor(
    n_estimators=1000,
    learning_rate=0.1,
    max_depth=3,
    subsample=0.5,
    random_state=42
)
gbm.fit(X_train, y_train)

# 步骤 3：预测与评估
y_pred = gbm.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"测试集均方误差: {mse:.4f}")

# 步骤 4：绘制特征重要性（来自论文的可解释性部分）
importances = gbm.feature_importances_
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(8, 5))
plt.title("特征重要性")
plt.bar(range(X.shape[1]), importances[indices])
plt.xticks(range(X.shape[1]), [f'特征 {i}' for i in indices], rotation=45)
plt.tight_layout()
plt.show()

# 可选：绘制学习曲线（损失值随迭代次数变化）
test_score = np.zeros((gbm.n_estimators,), dtype=np.float64)
for i, y_pred in enumerate(gbm.staged_predict(X_test)):
    test_score[i] = gbm.loss_(y_test, y_pred)
plt.figure(figsize=(8, 5))
plt.title("偏差（损失）随提升迭代次数的变化")
plt.plot(test_score, label="测试集偏差")
plt.xlabel("迭代次数")
plt.ylabel("偏差")
plt.legend()
plt.show()
```

### 实现原理（与论文关联）

- **数据**：使用带噪声的合成回归数据，类似论文中的实证测试
- **模型**：默认使用最小二乘损失，将树模型拟合到负梯度（残差）
- **训练**：通过收缩率（`learning_rate=0.1`）顺序添加树模型以防止过拟合，符合论文建议
- **评估**：均方误差对应论文关注的平方误差；图表展示收敛过程和特征重要性（总不纯度减少量）
- **运行方式**：直接复制到 Jupyter notebook 或 Python 脚本中运行，需要安装 `scikit-learn` 和 `matplotlib`

这是一个实用的入门示例——scikit-learn 的实现紧密遵循了 Friedman 的算法。如需从零开始的实现版本，请告诉我！

[scikit-learn 梯度提升文档](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html)
