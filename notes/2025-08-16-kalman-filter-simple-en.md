---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kalman Filter Explained Simply
translated: false
type: note
---

Here’s a **comprehensive guide to Kalman Filtering (卡尔曼滤波)** in English, structured for clarity:

---

# 1. Introduction

The **Kalman filter** is an **algorithm** that provides estimates of unknown variables by combining noisy sensor measurements with predictions from a system model. It is widely used in **control systems, navigation, robotics, computer vision, and finance**.

Key idea:
It works recursively — meaning it continuously updates its estimate as new measurements arrive, rather than waiting for the entire dataset.

---

# 2. Core Concepts

### State

The set of variables we want to estimate (e.g., position, velocity).

### Process Model

Describes how the state evolves over time, usually with some uncertainty.

### Measurement Model

Relates the actual sensor measurements to the underlying state.

### Noise

Both the process and the measurements have uncertainty (random noise). The Kalman filter explicitly models this using probabilities.

---

# 3. Mathematical Formulation

The Kalman filter assumes a **linear system** with Gaussian noise.

* **State equation (prediction):**

  $$
  x_k = A x_{k-1} + B u_k + w_k
  $$

  * $x_k$: state at time $k$
  * $A$: state transition matrix
  * $B u_k$: control input
  * $w_k$: process noise (Gaussian, covariance $Q$)

* **Measurement equation (observation):**

  $$
  z_k = H x_k + v_k
  $$

  * $z_k$: measurement
  * $H$: observation matrix
  * $v_k$: measurement noise (Gaussian, covariance $R$)

---

# 4. The Two Main Steps

### Step 1: Prediction

* Predict the state forward in time.
* Predict the uncertainty (error covariance).

### Step 2: Update (Correction)

* Compare predicted measurement to actual measurement.
* Compute **Kalman Gain** (how much trust to put in measurement vs. prediction).
* Update the estimate and reduce uncertainty.

---

# 5. Kalman Filter Equations (Linear Case)

1. **Predict state:**

   $$
   \hat{x}_k^- = A \hat{x}_{k-1} + B u_k
   $$

2. **Predict covariance:**

   $$
   P_k^- = A P_{k-1} A^T + Q
   $$

3. **Kalman Gain:**

   $$
   K_k = P_k^- H^T (H P_k^- H^T + R)^{-1}
   $$

4. **Update state:**

   $$
   \hat{x}_k = \hat{x}_k^- + K_k (z_k - H \hat{x}_k^-)
   $$

5. **Update covariance:**

   $$
   P_k = (I - K_k H) P_k^-
   $$

Where:

* $\hat{x}_k^-$: predicted state before update
* $\hat{x}_k$: updated state
* $P_k$: covariance matrix (uncertainty in estimate)

---

# 6. Intuition

* If the measurement is **very noisy** (large $R$), the Kalman gain becomes small → rely more on prediction.
* If the model is **uncertain** (large $Q$), the Kalman gain increases → rely more on measurements.
* Over time, it finds the **optimal balance** between trusting the model and trusting the sensors.

---

# 7. Variants

* **Extended Kalman Filter (EKF):** For nonlinear systems, uses linearization (Jacobian).
* **Unscented Kalman Filter (UKF):** For nonlinear systems, uses deterministic sampling.
* **Information Filter:** Works with inverse covariance for efficiency.
* **Ensemble Kalman Filter:** Used in weather forecasting and high-dimensional systems.

---

# 8. Applications

* **Navigation:** GPS + accelerometer fusion for position tracking.
* **Robotics:** SLAM (Simultaneous Localization and Mapping).
* **Finance:** Estimating hidden variables like volatility.
* **Computer Vision:** Object tracking in videos.
* **Control Systems:** Stabilizing aircraft and spacecraft.

---

# 9. Example Scenario

Imagine a self-driving car estimating its position:

* Model predicts position using velocity + previous state.
* GPS provides a noisy measurement of position.
* Kalman filter blends prediction and GPS to get a smoother, more accurate position.

Over time, the car can track its location even if GPS briefly drops out.

---

# 10. Key Strengths and Limitations

**Strengths:**

* Recursive, efficient (only needs last state, not entire history).
* Optimal for linear Gaussian systems.
* Widely tested and robust.

**Limitations:**

* Requires accurate models of dynamics and noise.
* Purely linear — nonlinear cases need EKF/UKF.
* Can diverge if assumptions are violated.

---

✅ In short: The **Kalman filter** is a mathematically elegant way to fuse predictions and measurements under uncertainty, balancing trust between models and sensors to produce the best possible estimate in real time.

---

Would you like me to also give you a **step-by-step Python implementation example** (like tracking position with noise), so you can see how it works in practice?
