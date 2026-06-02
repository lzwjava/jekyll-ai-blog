---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 高级Kusto查询语言示例
translated: true
type: note
---

Kusto查询语言（KQL）是用于查询Azure数据资源管理器、Azure Monitor等Azure服务中大型数据集的强大工具。以下是结合了多种运算符、函数及高级功能（如时间序列分析、异常检测、数据透视和用户自定义函数）的复杂示例，这些示例源自风暴事件分析或销售数据等真实场景。每个示例均包含查询语句及简要说明。

### 1. 时间序列数据异常检测

该查询从指标表中聚合日均值，并通过序列分解识别异常，适用于监控日志或遥测数据中的异常模式。

```
TableName
| make-series Metric = avg(Value) on Timestamp step 1d
| extend Anomalies = series_decompose_anomalies(Metric)
```

### 2. 参数化筛选与汇总的用户自定义函数

此处的可复用函数通过区域和阈值筛选销售数据后计算总额，适用于Azure数据资源管理器仪表板中的动态报表生成。

```
let CalculateSales = (region: string, minSales: int) {
    SalesData
    | where Region == region and Sales > minSales
    | summarize TotalSales = sum(Sales)
};
CalculateSales("North America", 1000)
```

### 3. 交叉表分析的聚合数据透视

本查询按类别和区域对数值进行聚合，随后将区域透视作为列以便对比，常见于商业智能查询场景。

```
TableName
| summarize Total = sum(Value) by Category, Region
| evaluate pivot(Region, sum(Total))
```

### 4. 时间序列指标间的相关性分析

使用风暴事件数据创建两个指标的日序列，并通过计算相关性揭示其关联（如财产损失与死亡人数之间的关系）。

```
StormEvents
| make-series PropertyDamage = avg(DamageProperty), Fatalities = avg(Fatalities) on BeginTime step 1d
| extend Correlation = series_correlation(PropertyDamage, Fatalities)
```

### 5. 事件分析中的筛选、TopN选取与持续时间计算

该查询筛选德克萨斯州洪水事件，按损失程度选取前5条记录，并添加计算得出的持续时间列，适用于Azure Sentinel的事件响应分析。

```
StormEvents
| where State == 'TEXAS' and EventType == 'Flood'
| top 5 by DamageProperty
| project StartTime, EndTime, Duration = EndTime - StartTime, DamageProperty
```

### 6. 使用Let语句的静态值映射实现数据转换

通过定义字典映射源类型，筛选事件并投射友好名称，可用于日志中分类数据的标准化处理。

```
let sourceMapping = dynamic(
  {
    "Emergency Manager" : "Public",
    "Utility Company" : "Private"
  });
StormEvents
| where Source == "Emergency Manager" or Source == "Utility Company"
| project EventId, Source, FriendlyName = sourceMapping[Source]
```

以上示例可直接在Azure数据资源管理器Web界面或Log Analytics中运行。更多案例请探索官方示例库。

[Kusto查询语言（KQL）完整指南](https://medium.com/@danushidk507/comprehensive-guide-to-kusto-query-language-kql-from-beginner-to-advanced-8dff3bd7568e)
[教程：掌握常用Kusto查询语言运算符](https://learn.microsoft.com/en-us/kusto/query/tutorials/learn-common-operators?view=microsoft-fabric)
