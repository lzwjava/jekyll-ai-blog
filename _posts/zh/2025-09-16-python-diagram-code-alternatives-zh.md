---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: Python图表即代码工具备选方案
translated: true
type: note
---

以下是适用于Python的软件设计/架构图生成方案（除Graphviz和NetworkX外），按使用场景分类并附简要说明及示例代码。

**代码即图表**（UML、C4、流程图、时序图）

- PlantUML（通过python-plantuml或本地JAR运行）
  - 适用于UML图表：类图、时序图、组件图、状态图、活动图、部署图
  - 可无缝集成至CI流程和文档系统
  - 示例：

    ```plantuml
    @startuml
    class 用户
    class 订单
    用户 "1" --> "*" 订单
    @enduml
    ```

- Mermaid（通过CLI或Kroki服务调用，Python可调用渲染器）
  - 简洁语法支持时序图、类图、流程图、实体关系图、状态图等
  - 在多种文档工具和wiki中渲染效果出色
  - 示例：

    ```mermaid
    flowchart LR
      API --> 数据库
    ```

- BlockDiag系列（blockdiag, seqdiag, actdiag, nwdiag）
  - 纯Python工具，通过文本生成框图、时序图、活动图和网络拓扑图
  - 示例（seqdiag）：

    ```seqdiag
    seqdiag {
      客户端 -> API [label = "GET /users"];
      API -> 数据库 [label = "查询"];
    }
    ```

- Structurizr（C4模型，提供社区版Python客户端）
  - 支持软件架构建模（上下文、容器、组件），可通过Structurizr/PlantUML渲染
  - 擅长多视角架构文档和架构决策记录工作流
- Kroki（图表即服务，提供Python客户端）
  - 通过统一HTTP接口渲染多种DSL（PlantUML、Mermaid、Graphviz、BPMN等）

**云与基础设施架构**

- Diagrams（mingrammer开发）
  - 通过代码生成云平台/系统架构图，内置官方图标库（AWS、Azure、GCP、K8s、本地设施）
  - 广泛用于架构概览图制作
  - 示例：

    ```python
    from diagrams import Diagram
    from diagrams.aws.compute import EC2
    from diagrams.aws.database import RDS
    with Diagram("网络服务", show=False):
        EC2("接口") >> RDS("数据库")
    ```

**交互式网络/图可视化**（适用于系统映射、依赖关系展示）

- PyVis（基于vis.js）
  - 极简代码生成可交互的HTML图例
  - 示例：

    ```python
    from pyvis.network import Network
    net = Network(); net.add_nodes(["API","数据库"]); net.add_edge("API","数据库"); net.show("架构.html")
    ```

- Dash Cytoscape / ipycytoscape（基于Cytoscape.js）
  - 为Dash应用或Jupyter提供可定制交互图表，适合依赖关系与流程探索
- Plotly
  - 支持自定义样式的交互式节点链接图，便于嵌入与分享
- Bokeh / HoloViews
  - 支持网络图的交互式绘图库，适合Python生态的仪表盘
- python-igraph
  - 内置布局算法的快速图计算库，可导出图表

**文档集成**（实现图表与文档紧密关联）

- Sphinx扩展：sphinxcontrib-plantuml、sphinxcontrib-mermaid、sphinxcontrib-blockdiag
  - 在reStructuredText/Markdown中直接编写图表，通过文档流水线自动构建
- MkDocs插件（支持Mermaid/PlantUML）
  - 现代化静态站点的高效集成方案

**代码与架构逆向工程**

- pylint的pyreverse工具
  - 从Python代码生成UML类图与包图（通常通过Graphviz渲染，工作流简洁）
- pydeps
  - 生成Python包导入依赖图，适用于大型代码库的架构映射

**专业图表**

- SchemDraw
  - 基于Python的程序化电路/逻辑/流程图绘制工具，输出矢量图
- railroad-diagrams
  - 生成语法规则图（适用于协议/规范文档）

**选型建议**

- 快速生成UML/时序图：PlantUML或Mermaid
- 云架构示意图：Diagrams（mingrammer）
- 交互式探索与分享：PyVis或Dash Cytoscape
- C4模型与动态架构文档：Structurizr（支持PlantUML/Mermaid导出）
- 代码自动生成图表：pyreverse、pydeps

若告知目标图表类型（UML类图、时序图、C4模型、云架构、数据流、包依赖）及输出格式（PNG/SVG/HTML/文档嵌入），我可提供最小化配置方案和入门模板。
