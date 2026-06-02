---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Kusto查询语言入门
translated: true
type: note
---

### Azure 中 KQL（Kusto 查询语言）入门指南

KQL 是一种功能强大的只读查询语言，专为分析 Azure 服务（如 Azure Data Explorer、Azure Monitor（Log Analytics）和 Microsoft Sentinel）中的大规模结构化、半结构化和非结构化数据而设计。它采用直观的管道式语法（使用 `|` 表示数据流），并针对日志分析、遥测数据和威胁检测等大数据场景进行了优化。以下是使用该语言的逐步指南。

#### 先决条件

- 拥有可访问相关服务（如 Azure Data Explorer 集群、Log Analytics 工作区或 Sentinel 实例）的有效 Azure 订阅。
- 具备适当权限：至少对数据库、表或工作区拥有读取权限。
- 对数据概念（如表和筛选）有基本了解会更有帮助，但 KQL 对初学者友好。
- 可选：安装 Azure Data Explorer 应用或使用 Web UI 快速入门——初始阶段无需编码环境。

#### 第一步：选择查询运行环境

KQL 可在多个 Azure 服务中运行。根据数据源选择适合的环境：

- **Azure Data Explorer**：适合大数据探索。通过 [dataexplorer.azure.com](https://dataexplorer.azure.com/) 访问 Web UI，选择集群和数据库后打开查询编辑器。
- **Azure Monitor / Log Analytics**：用于日志和指标。在 Azure 门户 (portal.azure.com) 中，转到 **Monitor > Logs**，选择工作区并使用查询编辑器。
- **Microsoft Sentinel**：用于安全分析。在 Azure 门户中，导航至工作区中的 **Microsoft Sentinel > Logs**。
- **其他选项**：Microsoft Fabric（通过 KQL 查询编辑器）或与 Power BI 等工具集成以实现可视化。

数据按层次结构组织：数据库 > 表 > 列。查询为只读操作；需使用以 `.` 开头的管理命令进行架构更改。

#### 第二步：理解基础语法

KQL 查询是以分号 (`;`) 分隔的纯文本语句，采用数据流模型：

- 以表名开头（例如 `StormEvents`）。
- 通过管道符 (`|`) 将数据传递至筛选、聚合等运算符。
- 以 `count` 或 `summarize` 等输出结尾。
- 名称和运算符区分大小写；必要时用 `['keyword']` 包裹关键字。

简单查询结构示例：

```
表名
| where 条件
| summarize 计数 = count() by 分组列
```

管理命令（非查询）以 `.` 开头（例如 `.show tables` 用于列出表）。

#### 第三步：编写并运行首个查询

1. 在所选服务中打开查询编辑器（如 Azure Data Explorer Web UI）。
2. 输入基础查询。使用示例数据（大多数环境中可用的 StormEvents 表）的示例：

   ```
   StormEvents
   | where StartTime between (datetime(2007-11-01) .. datetime(2007-12-01))
   | where State == "FLORIDA"
   | count
   ```

   - 此查询筛选 2007 年 11 月佛罗里达州的风暴事件并返回计数（例如 28）。
3. 点击 **运行** 执行。结果以表格形式显示；可通过 UI 转换为图表视图或导出。
4. 迭代优化：添加 `project`（选择列）、`summarize`（聚合）或 `extend`（添加计算列）等运算符。

建议优先掌握的常用运算符：

- `where`：筛选行（例如 `| where Level == "Error"`）。
- `summarize`：聚合数据（例如 `| summarize avg(Duration) by User`）。
- `join`：合并表。
- `search`：跨表全文搜索。

#### 第四步：探索高级功能与最佳实践

- **时间序列与分析**：使用 `make-series` 等函数分析趋势，或使用 `detect-anomalies` 检测异常值。
- **可视化**：在编辑器中切换至网格/图表视图。导出至 Power BI 以创建仪表板。
- **性能优化技巧**：合理排序运算符（尽早筛选）、用 `take 100` 限制结果数量，并在小型数据集上测试。
- **常见应用场景**：
  - **日志分析**：查询应用错误（`| where Level == "Error" | take 50`）。
  - **安全狩猎**：在 Sentinel 中搜索威胁（`search "suspicious login"`）。
  - **数据探索**：汇总指标（`| summarize count() by bin(TimeGenerated, 1h)`）。

#### 故障排除

- 报错？检查编辑器中的语法（会高亮问题）。确保表/列名称完全匹配。
- 无数据？确认工作区已摄入日志，或使用示例数据集。
- 通过 Azure 门户或文档中的交互式教程深入学习。

如需实践练习，可在 Azure Data Explorer 中加载示例数据并进行实验。

[参考文档]
[Kusto 查询语言 (KQL) 概述](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/)
[编写并运行首个 KQL 查询](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/tutorial?pivots=azuredataexplorer-cluster)
[常用 KQL 运算符](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/tutorial?pivots=azuredataexplorer-cluster&tabs=beginner)
