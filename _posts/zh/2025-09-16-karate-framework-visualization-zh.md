---
audio: false
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: 空手道测试框架架构可视化
translated: true
type: note
---

以下是使用 NetworkX 和 Matplotlib 绘制 Karate 测试框架高层架构/流程的独立 Python 脚本。该脚本按角色对组件进行分组（编写、执行、运行时、协议/IO、外部系统和报告），并展示了从特性文件通过引擎到协议和报告的典型流程。

使用说明：
- 执行 pip install networkx matplotlib
- 如需更美观的布局可选择性安装 pygraphviz 或 pydot + graphviz；脚本会自动检测并回退到弹簧布局

代码：

```python
import networkx as nx
import matplotlib.pyplot as plt

# 尝试使用 Graphviz 获得更清晰布局；不可用时回退到弹簧布局
def get_layout(G):
    try:
        # 尝试 PyGraphviz
        from networkx.drawing.nx_agraph import graphviz_layout
        return graphviz_layout(G, prog="dot")
    except Exception:
        try:
            # 尝试 pydot
            from networkx.drawing.nx_pydot import graphviz_layout
            return graphviz_layout(G, prog="dot")
        except Exception:
            # 回退方案：弹簧布局
            return nx.spring_layout(G, k=1.2, seed=42)

G = nx.DiGraph()

# 按类别定义节点
nodes = {
    # 编写层
    "特性文件 (.feature)": "编写",
    "可复用特性 (call/read)": "编写",
    "karate-config.js / 属性配置": "编写",
    "测试数据 (JSON/CSV)": "编写",

    # 执行层
    "运行器 (CLI/JUnit5/Maven/Gradle)": "执行",
    "并行运行器": "执行",

    # 运行时层
    "Karate 引擎 (DSL 解释器)": "运行时",
    "JS 引擎": "运行时",
    "变量/上下文": "运行时",
    "断言与匹配器": "运行时",

    # 协议/IO层
    "HTTP/REST/SOAP/GraphQL": "协议",
    "WebSocket": "协议",
    "UI 驱动 (web)": "协议",
    "Mock 服务": "协议",

    # 外部系统
    "外部系统/服务": "外部",

    # 报告层
    "报告 (HTML, JUnit, JSON)": "报告",
    "CI/CD": "报告",
}

# 添加带类别属性的节点
for n, cat in nodes.items():
    G.add_node(n, category=cat)

# 定义边（u -> v）及可选标签
edges = [
    # 编写层到执行层
    ("特性文件 (.feature)", "运行器 (CLI/JUnit5/Maven/Gradle)", "执行"),
    ("karate-config.js / 属性配置", "运行器 (CLI/JUnit5/Maven/Gradle)", "配置"),
    ("测试数据 (JSON/CSV)", "特性文件 (.feature)", "数据驱动"),
    ("可复用特性 (call/read)", "特性文件 (.feature)", "复用"),

    # 执行层到运行时层
    ("运行器 (CLI/JUnit5/Maven/Gradle)", "并行运行器", "可选"),
    ("运行器 (CLI/JUnit5/Maven/Gradle)", "Karate 引擎 (DSL 解释器)", "调用"),
    ("并行运行器", "Karate 引擎 (DSL 解释器)", "并行化"),

    # 运行时内部交互
    ("Karate 引擎 (DSL 解释器)", "JS 引擎", "脚本表达式"),
    ("Karate 引擎 (DSL 解释器)", "变量/上下文", "状态管理"),

    # 引擎到协议层
    ("Karate 引擎 (DSL 解释器)", "HTTP/REST/SOAP/GraphQL", "调用 API"),
    ("Karate 引擎 (DSL 解释器)", "WebSocket", "发送/接收"),
    ("Karate 引擎 (DSL 解释器)", "UI 驱动 (web)", "驱动 UI"),
    ("Karate 引擎 (DSL 解释器)", "Mock 服务", "启动/桩"),

    # 协议层到外部系统
    ("HTTP/REST/SOAP/GraphQL", "外部系统/服务", "请求"),
    ("WebSocket", "外部系统/服务", "消息"),
    ("UI 驱动 (web)", "外部系统/服务", "浏览器/应用"),
    ("Mock 服务", "外部系统/服务", "模拟"),

    # 响应流回引擎
    ("外部系统/服务", "Karate 引擎 (DSL 解释器)", "响应"),

    # 断言与报告
    ("Karate 引擎 (DSL 解释器)", "断言与匹配器", "验证"),
    ("断言与匹配器", "报告 (HTML, JUnit, JSON)", "结果"),
    ("Karate 引擎 (DSL 解释器)", "报告 (HTML, JUnit, JSON)", "运行时日志"),
    ("报告 (HTML, JUnit, JSON)", "CI/CD", "发布"),
]

# 添加边到图
for u, v, label in edges:
    G.add_edge(u, v, label=label)

# 按类别设置颜色
category_colors = {
    "编写": "#4C78A8",
    "执行": "#F58518",
    "运行时": "#B279A2",
    "协议": "#54A24B",
    "外部": "#9A9A9A",
    "报告": "#E45756",
}

# 构建节点颜色列表
node_colors = [category_colors[G.nodes[n]["category"]] for n in G.nodes()]

# 计算布局
pos = get_layout(G)

plt.figure(figsize=(14, 10))
# 绘制节点
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1600, alpha=0.9, linewidths=1.2, edgecolors="black")
# 绘制边
nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle="-|>", arrowsize=16, width=1.2, connectionstyle="arc3,rad=0.06")
# 绘制标签
nx.draw_networkx_labels(G, pos, font_size=9, font_color="white")

# 绘制部分边标签以减少杂乱
important_edge_labels = {
    (u, v): d["label"]
    for u, v, d in G.edges(data=True)
    if d["label"] in {"执行", "调用", "并行化", "调用 API", "启动/桩", "验证", "结果", "发布"}
}
nx.draw_networkx_edge_labels(G, pos, edge_labels=important_edge_labels, font_size=8, label_pos=0.5, rotate=False)

# 图例
import matplotlib.patches as mpatches
legend_patches = [mpatches.Patch(color=col, label=cat) for cat, col in category_colors.items()]
plt.legend(handles=legend_patches, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.05), frameon=False)

plt.title("Karate 测试框架工作原理（高层流程）", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.show()
```

该示意图传达的信息：
- 编写层：编写 .feature 文件，可复用其他特性，通过 karate-config 配置，并注入数据
- 执行层：通过 CLI/JUnit5/Maven/Gradle 运行，支持并行执行
- 运行时层：Karate 引擎解释 DSL，使用 JS 引擎处理表达式，并管理场景状态
- 协议/IO层：引擎驱动 HTTP（REST/SOAP/GraphQL）、WebSocket 和 UI（通过 Karate 驱动），还可启动 Mock 服务来桩接依赖项
- 外部系统：真实服务或模拟服务进行响应
- 报告层：断言生成报告（HTML、JUnit XML、JSON），可供 CI/CD 发布

如需针对特定场景定制示意图（如仅限 API 测试，或强调 Mock 或 UI），请告知，我将调整节点/边。
