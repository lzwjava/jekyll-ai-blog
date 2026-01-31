---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Google Cloud 迁移策略指南
translated: true
type: note
---

好问题。让我结合实际思考，为你梳理这个技术栈中的每个组件将如何映射到 Google Cloud。现在，我根据调研结果整理出一份全面的迁移映射表。

以下是交互式迁移架构图：

这是交互式迁移地图——点击每一行可以展开详情，并可以使用工作量过滤器（effort filters）。

针对你的技术栈，有几点特别值得注意：

**Db2 是最难处理的部分。** Cloud SQL 原生并不支持 Db2，因此真正的核心问题在于工作负载的落脚点。OLTP 和分类账数据（核心金融处理）最适合映射到 Cloud SQL PostgreSQL——一种常见的做法是对新应用使用 Cloud SQL PostgreSQL，并逐步迁移关键数据。报表和批处理导出更适合 BigQuery，可以使用类似 SHIFT™ Translator 的工具将 Db2 SQL 转换为 BigQuery 格式。为了在切换期间保持两侧同步的 CDC pipeline，可以使用 Striim 构建从 IBM Db2 到 Google Cloud 的数据流水线，通过 change data capture 实现实时数据集成。

**WebSphere 现在拥有顶级工具支持。** Google 的 Migrate to Containers 支持将 WebSphere 应用重新平台化（replatforming）到容器中，它使用传统的 WebSphere Server 容器镜像或 Open Liberty 社区镜像，包括检测 VM、通过 IBM binary scanner 发现应用，并将其拆分为独立的容器。尽管如此，从长期来看，更好的策略是迁移到 Open Liberty，而不是将 WAS 的授权费用带入云端。

**Control-M 到 Composer 的迁移路径非常成熟。** DAGify 是一个开源解决方案，可以自动化将 Control-M XML 文件转换为 Airflow 的原生 DAG 格式，从而显著减少手动工作量和潜在错误。考虑到你们现有的 Python 脚本能力以及 400 多个可重用脚本，你们非常适合原生编写和维护 Airflow DAGs。

**Vault 保持灵活性。** 你既可以将其更换为 GCP Secret Manager（最简单），如果你的团队有深度的 dynamic-credential 工作流，也可以在 GKE 上运行 Vault 本身——无论哪种方式都不需要更改应用代码。