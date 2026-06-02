---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: NetworkX与Matplotlib图论教程
translated: true
type: note
---

### 安装所需库
要使用 NetworkX 和 Matplotlib 绘制图表，请按需安装：
- NetworkX：用于图结构的创建与操作
- Matplotlib：提供绘图功能

通过 pip 安装：
```bash
pip install networkx matplotlib
```

为获得更快的渲染速度，Matplotlib 建议安装 NumPy（`pip install numpy`）

### 基础设置与示例
1. **导入库**：
   ```python
   import networkx as nx
   import matplotlib.pyplot as plt
   ```

2. **创建图结构**：
   使用 NetworkX 构建简单无向图（可自定义为有向图、带权重边等）：
   ```python
   G = nx.Graph()  # 创建空图
   G.add_nodes_from([1, 2, 3, 4, 5])  # 添加节点（例如5个节点）
   G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])  # 添加边（连接关系）
   ```

3. **绘制并显示图表**：
   使用 Matplotlib 后端进行可视化：
   ```python
   nx.draw(G, with_labels=True)  # 绘制带节点标签的图
   plt.show()  # 显示图表
   ```

这将生成基础的环形布局图（包含5个节点的循环结构）

### 高级定制功能
- **布局控制**：调整节点位置（如随机布局、弹簧布局）：
  ```python
  pos = nx.spring_layout(G)  # 力导向布局，适用于真实网络
  nx.draw(G, pos=pos, with_labels=True, node_color='lightblue', edge_color='gray')
  plt.title("网络拓扑图")
  plt.show()
  ```
- **节点与边样式**：自定义视觉呈现：
  ```python
  nx.draw(G, pos=pos, node_size=500, node_color='red', edge_width=2, font_size=10)
  ```
- **有向图**：用于层次关系展示，使用 `nx.DiGraph`：
  ```python
  DG = nx.DiGraph()
  DG.add_edges_from([('A', 'B'), ('B', 'C')])
  nx.draw(DG, with_labels=True, arrows=True)
  plt.show()
  ```
- **图表导出**：保存为文件而非直接显示：
  ```python
  plt.savefig('diagram.png')
  ```

### 技巧与资源
- 查阅 NetworkX 文档（networkx.org）了解树状图、网格图等图类型
- 参考 Matplotlib 文档（matplotlib.org）学习嵌入式 GUI 或子图功能
- 处理大型图结构（超过100个节点）时，建议使用 `nx.draw_networkx` 或 Graphviz 等外部工具提升性能
- 可在 Jupyter notebook 中进行交互式绘图实验。若遇显示问题，常见原因是缺少图形后端（可通过 `pip install pyqt5` 等命令安装交互窗口支持）
