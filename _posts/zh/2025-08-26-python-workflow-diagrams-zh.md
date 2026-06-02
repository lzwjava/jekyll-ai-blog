---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 工作流图Python库
translated: true
type: note
---

如果你正在寻找能够轻松绘制工作流或流程图的Python库——类似于**maniod**这样可以简化图表绘制的工具——这里有一系列值得探索的优秀选择：

---

### 推荐用于工作流和流程图的Python包

#### **1. Graphviz（通过Python）**

* 一个广泛使用的开源工具，用于绘制DOT语言定义的图表。
* 提供多种布局样式，如分层（`dot`）、圆形（`circo`）、径向（`twopi`）和力导向（`neato`、`fdp`）（[维基百科][1]）。
* 在Python中，你可以使用`graphviz`或`pygraphviz`包装器以DSL风格编程方式定义节点和边。

> “我曾用GraphViz处理这类需求。我喜欢它的主要原因是它更像是一种DSL，而非制作流程图的GUI工具。”（[Reddit][2]）

#### **2. NetworkX**

* 一个原生的Python库，用于通过Matplotlib或Graphviz布局创建、分析和可视化图形（[维基百科][3]）。
* 支持有向图、多边以及多种布局算法，如弹簧布局、多部图（非常适合分层工作流）、圆形布局等（[维基百科][3]）。
* 非常适合生成数据驱动的工作流图表，其中图形结构是动态的。

#### **3. Pyvis（使用VisJS）**

* 让你能够在笔记本或网页中使用Python构建交互式工作流可视化。
* 基于VisJS构建；高度可定制的交互性、布局物理效果、工具提示——对于探索性图表来说响应迅速且用户友好（[GitHub][4]，[arXiv][5]）。

#### **4. Graph-tool**

* 一个高性能的Python/C++库，用于图形操作和可视化。
* 通过Cairo或Graphviz提供良好的导出功能，并支持复杂的图形算法，如果你需要分析加可视化能力的话（[维基百科][6]）。

#### **5. igraph**

* 一个快速、可扩展的图形库（C语言核心，带Python接口）。
* 非常适合性能密集型任务和大规模图形的交互式绘图支持（[arXiv][7]）。

#### **6. pyflowsheet**

* 专为工程场景下的**工艺流程图**量身定制。
* 让你能够从代码生成流程表——最小化繁琐操作，是过程工程师的理想选择（[GitHub][4]）。

#### **7. Plotly Sankey Diagram**

* 用于表示带有定量流量的流程——Sankey图通过箭头宽度显示流量大小。
* 当你不只需要展示结构，还需要展示步骤间流量大小时非常有用（[Plotly][8]）。

---

### 其他提到的工具

* **Schemdraw**：专为电路原理图设计，但包含流程图模块。图表精美，但布局必须手动指定（[Stack Overflow][9]）。
* **VisTrails**：一个基于UI的科学工作流工具（未积极维护），用于可视化地管理、可视化和探索流水线（[维基百科][10]）。
* **PM4Py**：专注于**流程挖掘**而非绘制任意工作流。更多是关于分析事件日志（[arXiv][11]）。

---

以下是一个快速分类，帮助你选择：

* **想要类似DSL的静态流程图？** → **Graphviz**
* **需要动态/自定义图形结构？** → **NetworkX**（+ Matplotlib或Graphviz）
* **想要在笔记本/网页中的交互性？** → **Pyvis**
* **处理大型、对性能敏感的图形？** → **igraph** 或 **graph-tool**
* **需要从代码生成工程风格的流程表？** → **pyflowsheet**
* **表示阶段之间的定量流动？** → **Plotly Sankey**

---

### 示例代码片段

**Graphviz（Python）**

```python
from graphviz import Digraph

dot = Digraph()
dot.node('A', 'Start')
dot.node('B', 'Process')
dot.node('C', 'End')
dot.edge('A', 'B')
dot.edge('B', 'C')

dot.render('flowchart', view=True)
```

**NetworkX**

```python
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edge('A', 'B')
G.add_edge('B', 'C')

pos = nx.multipartite_layout(G, subset_key=lambda n: {'A':0,'B':1,'C':2}[n])
nx.draw(G, pos, with_labels=True, arrows=True)
plt.show()
```

**Plotly Sankey**

```python
import plotly.graph_objects as go

fig = go.Figure(go.Sankey(
    node = dict(label=["Start","Process","End"], pad=15, thickness=20),
    link = dict(source=[0,1], target=[1,2], value=[1,1])
))
fig.show()
```

---

### 总结

* **Graphviz** 适用于清晰、DSL/代码定义的工作流。
* **NetworkX** 适用于通过Python实现灵活、布局驱动的图表。
* **Pyvis** 适用于在笔记本或网页中的交互式、丰富可视化。
* **igraph** / **graph-tool** 适用于性能密集型的图形任务。
* **pyflowsheet** 适用于工艺流程图。
* **Plotly Sankey** 如果你需要流量大小可视化。

如果你需要任何特定库的帮助或示例实现，请告诉我！

[1]: https://en.wikipedia.org/wiki/Graphviz?utm_source=chatgpt.com "Graphviz"
[2]: https://www.reddit.com/r/Python/comments/ewbku/recommended_methodsapps_for_making_flowcharts/?utm_source=chatgpt.com "推荐制作流程图的方法/应用？ : r/Python"
[3]: https://en.wikipedia.org/wiki/NetworkX?utm_source=chatgpt.com "NetworkX"
[4]: https://github.com/Nukleon84/pyflowsheet?utm_source=chatgpt.com "Nukleon84/pyflowsheet: 一个用于绘制工艺流程图的Python包..."
[5]: https://arxiv.org/abs/2006.04951?utm_source=chatgpt.com "使用Pyvis和VisJS进行网络可视化"
[6]: https://en.wikipedia.org/wiki/Graph-tool?utm_source=chatgpt.com "Graph-tool"
[7]: https://arxiv.org/abs/2311.10260?utm_source=chatgpt.com "igraph实现跨编程语言的快速稳健网络分析"
[8]: https://plotly.com/python/sankey-diagram/?utm_source=chatgpt.com "Python中的Sankey图 - Plotly"
[9]: https://stackoverflow.com/questions/22920433/python-library-for-drawing-flowcharts-and-illustrated-graphs?utm_source=chatgpt.com "用于绘制流程图和说明性图形的Python库"
[10]: https://en.wikipedia.org/wiki/VisTrails?utm_source=chatgpt.com "VisTrails"
[11]: https://arxiv.org/abs/1905.06169?utm_source=chatgpt.com "Python流程挖掘（PM4Py）：弥合流程与数据科学之间的鸿沟"
