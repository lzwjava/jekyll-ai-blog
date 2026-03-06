import matplotlib.pyplot as plt
import pandas as pd

from k_means import KMeans

df = pd.read_csv("Mall_Customers.csv")

X = df[["Annual Income (k$)", "Spending Score (1-100)"]]

plt.close()
plt.style.use("seaborn")
plt.scatter(X["Annual Income (k$)"], X["Spending Score (1-100)"])
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score (1-100)")

model = KMeans(max_iter=500, tolerance=0.001, n_clusters=5, runs=100)
clusters, data_with_clusters = model.fit(X)

print(model.cost_)

plt.close()
for i, cluster_mean in enumerate(clusters):
    data_cluster_i = data_with_clusters[data_with_clusters[:, -1] == i]
    plt.scatter(data_cluster_i[:, 0], data_cluster_i[:, 1], label="Cluster " + str(i))
    plt.plot(
        cluster_mean[0],
        cluster_mean[1],
        label="Centroid " + str(i),
        marker="*",
        markersize=15,
        markeredgecolor="k",
        markeredgewidth=1,
    )
    plt.xlabel("Annual Income (k$)")
    plt.ylabel("Spending Score (1-100)")
    plt.style.use("seaborn")
    plt.legend()

plt.show()
