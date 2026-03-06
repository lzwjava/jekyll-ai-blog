import numpy as np
import matplotlib.pyplot as plt


class DecisionStump:
    """Simple decision stump (single split) for regression."""

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
            # Sort by feature and try midpoints as thresholds
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
    """Vanilla GBM: Fits stumps to pseudo-residuals with shrinkage."""

    def __init__(self, n_estimators=100, learning_rate=0.1):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.models = []
        self.initial_pred = None

    def fit(self, X, y):
        n_samples = X.shape[0]
        # Initialize with mean (minimizer for squared loss)
        self.initial_pred = np.mean(y)
        current_pred = np.full(n_samples, self.initial_pred)

        for _ in range(self.n_estimators):
            # Pseudo-residuals: negative gradient of L = 1/2 (y - F)^2, so r = y - F
            residuals = y - current_pred

            # Fit weak learner to residuals
            stump = DecisionStump()
            stump.fit(X, residuals)
            self.models.append(stump)

            # Update with shrinkage (no line search for simplicity; could add argmin gamma)
            update = self.learning_rate * stump.predict(X)
            current_pred += update

    def predict(self, X):
        current_pred = np.full(X.shape[0], self.initial_pred)
        for model in self.models:
            current_pred += self.learning_rate * model.predict(X)
        return current_pred


# Example usage: Synthetic data (like paper's regression tests)
np.random.seed(42)
n_samples = 1000
n_features = 10
X = np.random.randn(n_samples, n_features)
true_coef = np.random.randn(n_features) * 2
y = X @ true_coef + np.random.randn(n_samples) * 0.1  # Noisy linear signal

# Split data
split = int(0.8 * n_samples)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Train GBM
gbm = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
gbm.fit(X_train, y_train)

# Predict and evaluate (squared error)
y_pred_train = gbm.predict(X_train)
y_pred_test = gbm.predict(X_test)
train_mse = np.mean((y_train - y_pred_train) ** 2)
test_mse = np.mean((y_test - y_pred_test) ** 2)
print(f"Train MSE: {train_mse:.4f}")
print(f"Test MSE: {test_mse:.4f}")

# Plot predictions vs. true (test set)
plt.figure(figsize=(8, 5))
plt.scatter(y_test, y_pred_test, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
plt.xlabel("True Values")
plt.ylabel("Predicted Values")
plt.title("GBM Predictions vs. True (Test Set)")
plt.tight_layout()
plt.show()

# Optional: Learning curve (cumulative predictions)
train_scores = []
current_pred_train = np.full(len(y_train), gbm.initial_pred)
for i in range(gbm.n_estimators):
    update = gbm.learning_rate * gbm.models[i].predict(X_train)
    current_pred_train += update
    score = np.mean((y_train - current_pred_train) ** 2)
    train_scores.append(score)

plt.figure(figsize=(8, 5))
plt.plot(train_scores)
plt.xlabel("Number of Boosting Iterations")
plt.ylabel("Train MSE")
plt.title("Learning Curve: MSE vs. Iterations")
plt.tight_layout()
plt.show()
