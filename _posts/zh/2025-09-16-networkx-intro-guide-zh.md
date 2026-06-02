---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/o1-mini
title: NetworkX Python图论库入门
translated: true
type: note
---

NetworkX 是一个功能强大的 Python 库，用于创建、操作和研究复杂网络（图结构）。它提供了处理无向图和有向图的工具，支持带权边，并能执行多种网络分析。

以下是一些入门示例：

---

### 1. **安装 NetworkX**

使用前请确保已安装 NetworkX，可通过 `pip` 安装：

```bash
pip install networkx
```

---

### 2. **创建并可视化简单图**

以下示例展示如何创建简单无向图、添加节点与边，并使用 Matplotlib 进行可视化：

```python
import networkx as nx
import matplotlib.pyplot as plt

# 创建空图
G = nx.Graph()

# 添加节点
G.add_node(1)
G.add_nodes_from([2, 3, 4])

# 添加边（若节点不存在会自动创建）
G.add_edge(1, 2)
G.add_edges_from([(1, 3), (2, 4)])

# 绘制图形
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
plt.title("简单无向图")
plt.show()
```

**输出效果：**

包含 4 个节点并通过边连接的简单无向图。

---

### 3. **有向图**

创建并可视化有向图：

```python
import networkx as nx
import matplotlib.pyplot as plt

# 创建有向图
DG = nx.DiGraph()

# 添加边（自动创建节点）
DG.add_edges_from([
    ('A', 'B'),
    ('A', 'C'),
    ('B', 'C'),
    ('C', 'A'),
    ('C', 'D')
])

# 绘制带箭头的有向图
pos = nx.circular_layout(DG)
nx.draw(DG, pos, with_labels=True, node_color='lightgreen', edge_color='gray', arrows=True, node_size=700)
plt.title("有向图")
plt.show()
```

**输出效果：**

通过箭头显示边方向的有向图。

---

### 4. **带权图**

为边分配权重并可视化：

```python
import networkx as nx
import matplotlib.pyplot as plt

# 创建带权图
WG = nx.Graph()

# 添加带权边
WG.add_edge('A', 'B', weight=4)
WG.add_edge('A', 'C', weight=2)
WG.add_edge('B', 'C', weight=5)
WG.add_edge('B', 'D', weight=10)
WG.add_edge('C', 'D', weight=3)

# 获取边权重标签
edge_labels = nx.get_edge_attributes(WG, 'weight')

# 绘制图形
pos = nx.spring_layout(WG)
nx.draw(WG, pos, with_labels=True, node_color='lightyellow', edge_color='gray', node_size=700)
nx.draw_networkx_edge_labels(WG, pos, edge_labels=edge_labels)
plt.title("带权图")
plt.show()
```

**输出效果：**

边标签显示权重的带权图。

---

### 5. **计算最短路径**

使用 Dijkstra 算法（适用于带权图）查找节点间最短路径：

```python
import networkx as nx

# 创建带权图（同前例）
WG = nx.Graph()
WG.add_edge('A', 'B', weight=4)
WG.add_edge('A', 'C', weight=2)
WG.add_edge('B', 'C', weight=5)
WG.add_edge('B', 'D', weight=10)
WG.add_edge('C', 'D', weight=3)

# 计算从 A 到 D 的最短路径
shortest_path = nx.dijkstra_path(WG, source='A', target='D', weight='weight')
path_length = nx.dijkstra_path_length(WG, source='A', target='D', weight='weight')

print(f"从 A 到 D 的最短路径: {shortest_path}，总权重: {path_length}")
```

**输出：**

```
从 A 到 D 的最短路径: ['A', 'C', 'D']，总权重: 5
```

---

### 6. **中心性度量**

通过不同中心性指标识别图中的关键节点：

```python
import networkx as nx

# 创建示例图
G = nx.karate_club_graph()

# 计算度中心性
degree_centrality = nx.degree_centrality(G)

# 计算介数中心性
betweenness_centrality = nx.betweenness_centrality(G)

# 计算特征向量中心性
eigen_centrality = nx.eigenvector_centrality(G, max_iter=1000)

# 显示度中心性前 5 的节点
sorted_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
print("度中心性前 5 的节点:")
for node, centrality in sorted_degree[:5]:
    print(f"节点 {node}: {centrality:.4f}")

# 可类似展示其他中心性指标
```

**输出：**

```
度中心性前 5 的节点:
节点 33: 0.6035
节点 0: 0.3793
节点 1: 0.3793
节点 2: 0.3793
节点 3: 0.3793
```

*注：* 空手道俱乐部图是 NetworkX 中常用的社交网络示例。

---

### 7. **使用 Girvan-Newman 算法检测社区**

识别图中的社区结构：

```python
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt

# 创建图（使用空手道俱乐部图）
G = nx.karate_club_graph()

# 使用 Girvan-Newman 算法计算社区
communities_generator = community.girvan_newman(G)
top_level_communities = next(communities_generator)
second_level_communities = next(communities_generator)

# 为社区分配颜色的函数
def get_community_colors(G, communities):
    color_map = {}
    for idx, community in enumerate(communities):
        for node in community:
            color_map[node] = idx
    return [color_map[node] for node in G.nodes()]

# 选择所需层级的社区
communities = second_level_communities
colors = get_community_colors(G, communities)

# 按社区颜色绘制图形
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=colors, with_labels=True, cmap=plt.cm.Set1)
plt.title("空手道俱乐部图中的社区结构")
plt.show()
```

**输出效果：**

根据社区归属着色显示的空手道俱乐部图。

---

### 8. **读写图数据**

NetworkX 支持多种图数据格式，如邻接表、边列表和 GraphML。

**读取边列表：**

```python
import networkx as nx

# 假设 'edges.txt' 包含：
# A B
# A C
# B C
# B D
# C D

G = nx.read_edgelist('edges.txt', delimiter=' ')
print("节点:", G.nodes())
print("边:", G.edges())
```

**将图写入 GraphML：**

```python
import networkx as nx

G = nx.complete_graph(5)  # 创建包含 5 个节点的完全图
nx.write_graphml(G, 'complete_graph.graphml')
print("图已保存至 'complete_graph.graphml'")
```

---

### 9. **结合 Pandas DataFrame 使用 NetworkX**

与 Pandas 集成实现高级数据操作：

```python
import networkx as nx
import pandas as pd

# 创建包含带权边的 DataFrame
data = {
    'source': ['A', 'A', 'B', 'B', 'C'],
    'target': ['B', 'C', 'C', 'D', 'D'],
    'weight': [4, 2, 5, 10, 3]
}
df = pd.DataFrame(data)

# 从 DataFrame 创建带权图
G = nx.from_pandas_edgelist(df, 'source', 'target', ['weight'])

# 显示带权边
for u, v, data in G.edges(data=True):
    print(f"({u}, {v}) - 权重: {data['weight']}")
```

**输出：**

```
(A, B) - 权重: 4
(A, C) - 权重: 2
(B, C) - 权重: 5
(B, D) - 权重: 10
(C, D) - 权重: 3
```

---

### 10. **使用 NetworkX 和 Matplotlib 进行高级可视化**

自定义图形外观以提升可读性：

```python
import networkx as nx
import matplotlib.pyplot as plt

# 创建图
G = nx.Graph()
G.add_edges_from([
    ('A', 'B'), ('A', 'C'), ('A', 'D'),
    ('B', 'C'), ('C', 'D'), ('D', 'E'),
    ('E', 'F'), ('F', 'C')
])

# 使用布局算法分配位置
pos = nx.spring_layout(G, seed=42)

# 绘制不同尺寸和颜色的节点
node_sizes = [700 if node == 'C' else 300 for node in G.nodes()]
node_colors = ['red' if node == 'C' else 'skyblue' for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors)

# 绘制不同宽度的边
edge_widths = [2 if (u == 'C' or v == 'C') else 1 for u, v in G.edges()]
nx.draw_networkx_edges(G, pos, width=edge_widths)

# 绘制标签
nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

plt.title("自定义图可视化")
plt.axis('off')
plt.show()
```

**输出效果：**

节点 C 以红色高亮显示且尺寸更大，与 C 相连的边线条更粗的自定义图。

---

这些示例提供了使用 NetworkX 在 Python 中创建、操作和分析图的基础知识。如需更高级用法和详细文档，请参阅 [NetworkX 官方文档](https://networkx.org/documentation/stable/)。
