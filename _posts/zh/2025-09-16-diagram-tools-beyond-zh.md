---
audio: false
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: 超越Graphviz和NetworkX的图表工具
translated: true
type: note
---

除 Graphviz 和 NetworkX 之外的优秀选择，按您的使用偏好分类。

文本/DSL「代码即图表」
- PlantUML：完整 UML（时序图、类图、组件图、部署图）、C4 模型、活动图；庞大生态系统。
- Mermaid：轻量级类 Markdown 语法；适用于流程图、时序图、类图、ER 图、状态图；在 GitHub/GitLab 原生渲染。
- D2（Terrastruct 开发）：简洁通用的图表 DSL，具备自动布局功能；支持分层和大规模图表。
- Structurizr（C4）：基于 DSL 的模型优先（C4）工具；可导出至 PlantUML/Mermaid；适合架构文档。
- C4-PlantUML：基于 PlantUML 的 C4 模型模板。
- nomnoml：极简语法，快速绘制类图/关系草图。
- Kroki：支持多种 DSL（PlantUML、Mermaid、Graphviz）的渲染服务器，适用于文档流水线。

代码优先（通过代码/基础设施即代码生成图表）
- diagrams（mingrammer，Python）：程序化云架构图（AWS/Azure/GCP/K8s）。
- Terraform 辅助工具：Inframap（通过状态文件绘制）、Blast Radius（基于 Terraform 的交互式图表）。
- AWS CDK：cdk-dia 可从 CDK 应用生成架构图。
- Go/TS 库：GoDiagrams（Go）、ts-graphviz（TypeScript）支持基于代码的生成。

Web 可视化库（交互式图表）
- Cytoscape.js：大规模图形可视化，内置布局算法，性能优异。
- D3.js：功能强大但层级较低，适用于自定义图形/图表可视化。
- vis-network（vis.js）：搭载物理引擎的简易网络图。
- Sigma.js：专为大规模型图提供快速渲染。
- ECharts：内置图形模块的通用图表库；可快速呈现结果。
- pyvis（Python）：通过 Vis.js 实现简易交互式网络图。

GUI 绘图工具（拖拽式操作）
- diagrams.net（draw.io）：免费易用，提供大量符号库（UML、云图标）。
- yEd/yFiles：强大的自动布局；yFiles 为商业 SDK，yEd 是免费桌面工具。
- Lucidchart/Miro：协同网页工具；适合团队协作。
- OmniGraffle（macOS）、Visual Paradigm、StarUML、Enterprise Architect：专业 UML/架构工具。

架构专用及领域工具
- C4 模型：Structurizr、C4-PlantUML、Mermaid C4 扩展。
- 云架构 SaaS：Cloudcraft（AWS）、Hava、Lucidscale、CloudSkew；支持从云服务/IaC 导入。
- BPMN/流程：Camunda Modeler、bpmn.io。
- 时序/定时图：WebSequenceDiagrams、WaveDrom（定时图）。
- ER/数据库图表：dbdiagram.io、SchemaSpy。

按场景快速选型
- 基于 Markdown/README 的文档即代码：Mermaid
- 完整 UML + C4 模板方案：PlantUML 或 Structurizr
- 基于代码/IaC 的云架构：diagrams（Python）、Inframap/Blast Radius（Terraform）、cdk-dia（AWS CDK）
- 交互式 Web 应用图形：Cytoscape.js 或 vis-network；定制化可视化选用 D3.js
- 快速 GUI 绘图：diagrams.net（draw.io）；自动布局需求选用 yEd

若提供您的偏好（文本/GUI、静态图像/交互式、使用语言及图表类型如时序图/C4/云架构/ER 图），我可为您推荐精简清单和入门模板。
