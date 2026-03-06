import numpy as np
import matplotlib.pyplot as plt


class KalmanFilter:
    def __init__(self, dt, process_variance, measurement_variance):
        self.dt = dt
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.A = np.array([[1, dt], [0, 1]])
        self.H = np.array([[1, 0]])
        self.Q = (
            np.array([[0.25 * dt**4, 0.5 * dt**3], [0.5 * dt**3, dt**2]])
            * process_variance
        )
        self.R = np.array([[measurement_variance]])
        self.P = np.eye(2)
        self.x = np.zeros((2, 1))

    def predict(self):
        self.x = np.dot(self.A, self.x)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x[0]

    def update(self, measurement):
        y = measurement - np.dot(self.H, self.x)
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        self.x = self.x + np.dot(K, y)
        self.P = self.P - np.dot(np.dot(K, self.H), self.P)
        return self.x[0]


def simulate_system():
    dt = 0.1
    t = np.arange(0, 10, dt)
    n = len(t)

    # True signal: position = 0.1t^2
    true_position = 0.1 * t**2
    true_velocity = 0.2 * t

    # Add noise to measurements
    measurements = true_position + np.random.normal(0, 1, n)

    # Initialize Kalman filter
    kf = KalmanFilter(dt=dt, process_variance=0.1, measurement_variance=1.0)

    # Lists to store estimates
    estimates = []

    # Run Kalman filter
    for measurement in measurements:
        kf.predict()
        estimate = kf.update(measurement)
        estimates.append(estimate)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(t, true_position, "g-", label="True Position")
    plt.plot(t, measurements, "r.", label="Measurements")
    plt.plot(t, estimates, "b-", label="Kalman Filter Estimate")
    plt.xlabel("Time (s)")
    plt.ylabel("Position")
    plt.title("Kalman Filter Tracking Example")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    simulate_system()
