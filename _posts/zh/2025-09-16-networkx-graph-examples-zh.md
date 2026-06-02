---
audio: false
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: NetworkX图创建与分析示例
translated: true
type: note
---

NetworkX 是一个功能强大的 Python 库，用于创建、分析和可视化复杂网络。以下是几个展示其功能的示例：

## 1. 基础图创建与可视化

```python
import networkx as nx
import matplotlib.pyplot as plt

# 创建空图
G = nx.Graph()

# 添加节点
G.add_node(1)
G.add_nodes_from([2, 3])
G.add_nodes_from(range(4, 7))

# 添加边
G.add_edge(1, 2)
G.add_edges_from([(2, 3), (3, 4), (4, 5), (5, 6), (6, 1)])

# 可视化图形
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray')
plt.show()
```

## 2. 有向图示例

```python
# 创建有向图
D = nx.DiGraph()

# 添加边（自动添加节点）
D.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)])

# 使用不同节点颜色绘制
pos = nx.spring_layout(D)
nx.draw(D, pos, with_labels=True, node_color='lightgreen',
        edge_color='red', node_size=1000, arrowsize=20)
plt.show()
```

## 3. 图分析示例

```python
# 创建图
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)])

# 基础图属性
print("节点数量:", G.number_of_nodes())
print("边数量:", G.number_of_edges())
print("节点:", G.nodes())
print("边:", G.edges())
print("节点2的度:", G.degree(2))
print("节点2的邻居:", list(G.neighbors(2)))
print("图是否连通?", nx.is_connected(G))
print("从1到5的最短路径:", nx.shortest_path(G, 1, 5))
```

## 4. 加权图示例

```python
# 创建加权图
G = nx.Graph()

# 添加带权重的边
G.add_edge('A', 'B', weight=4)
G.add_edge('B', 'C', weight=2)
G.add_edge('A', 'C', weight=1)
G.add_edge('C', 'D', weight=5)

# 绘制带权重标签的边
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightcoral')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()
```

## 5. 社交网络分析示例

```python
# 创建社交网络图
social = nx.Graph()

# 添加人员及其连接关系
people = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
social.add_nodes_from(people)

connections = [('Alice', 'Bob'), ('Alice', 'Charlie'),
               ('Bob', 'Charlie'), ('Bob', 'David'),
               ('Charlie', 'Eve'), ('David', 'Eve')]
social.add_edges_from(connections)

# 计算中心性指标
degree_centrality = nx.degree_centrality(social)
betweenness_centrality = nx.betweenness_centrality(social)
closeness_centrality = nx.closeness_centrality(social)

print("度中心性:", degree_centrality)
print("介数中心性:", betweenness_centrality)
print("接近中心性:", closeness_centrality)

# 可视化
nx.draw(social, with_labels=True, node_color='lightgreen', node_size=2000)
plt.show()
```

## 6. 随机图生成

```python
# 创建 Erdős–Rényi 随机图
random_graph = nx.erdos_renyi_graph(10, 0.3)  # 10个节点，30%的边概率

# 可视化
nx.draw(random_graph, with_labels=True, node_color='skyblue')
plt.show()
```

## 7. 图算法示例

```python
# 创建图
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 6), (5, 6)])

# 查找两个节点间的所有简单路径
print("从1到6的所有路径:", list(nx.all_simple_paths(G, 1, 6)))

# 最小生成树
T = nx.minimum_spanning_tree(G)
print("最小生成树中的边:", T.edges())

# 社区检测（需要 python-louvain 包）
# pip install python-louvain
try:
    import community as community_louvain
    partition = community_louvain.best_partition(G)
    print("社区划分:", partition)
except ImportError:
    print("请安装 python-louvain 包以使用社区检测功能")
```

这些示例涵盖了基础图创建、可视化、分析和一些常见算法。NetworkX 提供了更多用于处理复杂网络的功能。
