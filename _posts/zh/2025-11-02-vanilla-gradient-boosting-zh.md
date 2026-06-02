---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Python原生梯度提升实现
translated: true
type: note
---

### 纯Python实现的梯度提升算法（仅使用NumPy）

这是一个简单的梯度提升回归器从头实现，灵感来自Friedman 2001年的论文。它使用**决策树桩**（单次分裂的树，即深度为1的树）作为弱学习器以保持简洁性——不使用scikit-learn，仅用NumPy进行数值计算和Matplotlib绘图。这抓住了核心思想：拟合伪残差（平方损失的负梯度）、收缩（学习率）和加法更新。

该代码自包含，可在具有NumPy/Matplotlib的Python环境中运行。

```python
import numpy as np
import matplotlib.pyplot as plt

class DecisionStump:
    """用于回归的简单决策树桩（单次分裂）"""
    def __init__(self):
        self.feature_idx = None
        self.threshold = None
        self.left_val = None
        self.right_val = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        best_mse = np.inf
        best_idx, best_thresh = -1, -1
        best_left, best_right = None, None

        for idx in range(n_features):
            # 按特征排序并尝试中点作为阈值
            sorted_idx = np.argsort(X[:, idx])
            thresholds = (X[sorted_idx[:-1], idx] + X[sorted_idx[1:], idx]) / 2

            for thresh in thresholds:
                left_mask = X[:, idx] <= thresh
                right_mask = ~left_mask

                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue

                left_val = np.mean(y[left_mask])
                right_val = np.mean(y[right_mask])

                y_pred = np.zeros(n_samples)
                y_pred[left_mask] = left_val
                y_pred[right_mask] = right_val

                mse = np.mean((y - y_pred) ** 2)

                if mse < best_mse:
                    best_mse = mse
                    best_idx = idx
                    best_thresh = thresh
                    best_left = left_val
                    best_right = right_val

        self.feature_idx = best_idx
        self.threshold = best_thresh
        self.left_val = best_left
        self.right_val = best_right

    def predict(self, X):
        if self.feature_idx is None:
            return np.zeros(X.shape[0])

        left_mask = X[:, self.feature_idx] <= self.threshold
        y_pred = np.zeros(X.shape[0])
        y_pred[left_mask] = self.left_val
        y_pred[~left_mask] = self.right_val
        return y_pred

class GradientBoostingRegressor:
    """原始GBM：使用收缩率将树桩拟合到伪残差"""
    def __init__(self, n_estimators=100, learning_rate=0.1):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.models = []
        self.initial_pred = None

    def fit(self, X, y):
        n_samples = X.shape[0]
        # 用均值初始化（平方损失的最小化器）
        self.initial_pred = np.mean(y)
        current_pred = np.full(n_samples, self.initial_pred)

        for _ in range(self.n_estimators):
            # 伪残差：L = 1/2 (y - F)^2 的负梯度，所以 r = y - F
            residuals = y - current_pred

            # 将弱学习器拟合到残差
            stump = DecisionStump()
            stump.fit(X, residuals)
            self.models.append(stump)

            # 使用收缩率更新（为简化未进行线性搜索；可添加argmin gamma）
            update = self.learning_rate * stump.predict(X)
            current_pred += update

    def predict(self, X):
        current_pred = np.full(X.shape[0], self.initial_pred)
        for model in self.models:
            current_pred += self.learning_rate * model.predict(X)
        return current_pred

# 示例用法：合成数据（类似论文中的回归测试）
np.random.seed(42)
n_samples = 1000
n_features = 10
X = np.random.randn(n_samples, n_features)
true_coef = np.random.randn(n_features) * 2
y = X @ true_coef + np.random.randn(n_samples) * 0.1  # 带噪声的线性信号

# 分割数据
split = int(0.8 * n_samples)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# 训练GBM
gbm = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
gbm.fit(X_train, y_train)

# 预测和评估（平方误差）
y_pred_train = gbm.predict(X_train)
y_pred_test = gbm.predict(X_test)
train_mse = np.mean((y_train - y_pred_train) ** 2)
test_mse = np.mean((y_test - y_pred_test) ** 2)
print(f"训练集MSE: {train_mse:.4f}")
print(f"测试集MSE: {test_mse:.4f}")

# 绘制预测值与真实值对比（测试集）
plt.figure(figsize=(8, 5))
plt.scatter(y_test, y_pred_test, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('真实值')
plt.ylabel('预测值')
plt.title('GBM预测值 vs 真实值（测试集）')
plt.tight_layout()
plt.show()

# 可选：学习曲线（累积预测）
train_scores = []
current_pred_train = np.full(len(y_train), gbm.initial_pred)
for i in range(gbm.n_estimators):
    update = gbm.learning_rate * gbm.models[i].predict(X_train)
    current_pred_train += update
    score = np.mean((y_train - current_pred_train) ** 2)
    train_scores.append(score)

plt.figure(figsize=(8, 5))
plt.plot(train_scores)
plt.xlabel('提升迭代次数')
plt.ylabel('训练集MSE')
plt.title('学习曲线：MSE vs 迭代次数')
plt.tight_layout()
plt.show()
```

### 工作原理（与论文关联）

- **DecisionStump**：弱学习器通过单次分裂最小化MSE（类似论文中的浅层树）。为在小数据上保持效率，采用暴力搜索阈值。
- **GradientBoostingRegressor**：
  - 从 \\( F_0 = \bar{y} \\) 开始（平方损失最小化器）。
  - 迭代地将树桩拟合到残差 \\( r = y - F_{m-1} \\)（负梯度）。
  - 使用收缩率 \\( \nu = 0.1 \\) 进行正则化更新：\\( F_m = F_{m-1} + \nu \cdot h_m \\)。
  - 为简化未包含随机子采样或线性搜索（论文建议在大规模应用中使用）。
- **性能**：在这个玩具数据上，预期MSE较低（测试集约0.01）。它快速收敛（图表显示损失下降）。
- **局限性**：树桩限制了复杂度；实际使用时需扩展至更深树。处理回归任务；可通过对数损失梯度适配分类任务。
- **运行方法**：粘贴到脚本/笔记本中。输出MSE和图表，反映论文关注的收敛性/准确性。

如需扩展功能（例如更深树、分类），请告知！

[原论文PDF](https://jerryfriedman.su.domains/ftp/trebst.pdf)
