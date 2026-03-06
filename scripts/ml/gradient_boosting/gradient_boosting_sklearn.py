import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Step 1: Generate synthetic data (like the regression examples in the paper)
X, y = make_regression(n_samples=1000, n_features=10, noise=0.1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 2: Initialize and train the GBM
# Key params inspired by paper: n_estimators=1000 (many iterations), learning_rate=0.1 (shrinkage),
# max_depth=3 (shallow trees for weak learners), subsample=0.5 (stochastic variant)
gbm = GradientBoostingRegressor(
    n_estimators=1000, learning_rate=0.1, max_depth=3, subsample=0.5, random_state=42
)
gbm.fit(X_train, y_train)

# Step 3: Predict and evaluate
y_pred = gbm.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Test MSE: {mse:.4f}")

# Step 4: Plot feature importance (from the paper's interpretability section)
importances = gbm.feature_importances_
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(8, 5))
plt.title("Feature Importances")
plt.bar(range(X.shape[1]), importances[indices])
plt.xticks(range(X.shape[1]), [f"Feature {i}" for i in indices], rotation=45)
plt.tight_layout()
plt.show()

# Optional: Plot learning curve (loss vs. iterations)
test_score = np.zeros((gbm.n_estimators,), dtype=np.float64)
for i, y_pred in enumerate(gbm.staged_predict(X_test)):
    test_score[i] = mean_squared_error(y_test, y_pred)
plt.figure(figsize=(8, 5))
plt.title("Deviance (Loss) vs. Number of Boosting Iterations")
plt.plot(test_score, label="Test Deviance")
plt.xlabel("Number of Iterations")
plt.ylabel("Deviance")
plt.legend()
plt.show()
