---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: Azure Log Analytics 与 Azure Insights 对比
translated: true
type: note
---

很好的问题——它们**密切相关**，但**并不相同**。让我们来清晰地解析一下。

---

### **1. Azure Log Analytics**

**Azure Log Analytics** 是 **Azure Monitor** 中的一个**工具/服务**，它允许你**收集、查询和分析**来自云端和本地资源的日志。

* 它将日志存储在 **Log Analytics 工作区**中。
* 你可以使用 **Kusto 查询语言 (KQL)** 运行查询来分析数据。
* 它用于：

  * 故障排除
  * 调查性能问题
  * 监控安全性
  * 创建自定义仪表板和警报

可以将 Log Analytics 视为 Azure 中所有日志数据的**数据湖和查询引擎**。

---

### **2. Azure Insights**

**Azure Insights**（通常以 **Application Insights** 或 **Azure Monitor Insights** 的形式出现）属于同一监控生态系统，但更侧重于**应用程序级别的监控**，而非原始日志。

“Insights”有以下不同类型：

* **Application Insights** — 监控应用程序（APM）：性能、异常、依赖项、用户行为等。
* **VM Insights**、**Container Insights**、**Network Insights** — 为特定资源类型提供预构建的监控视图。

所有这些 Insights **都将它们的遥测数据和指标存储在 Log Analytics 工作区中**，因此它们**底层依赖于 Log Analytics**。

---

### **3. 关系**

* **Azure Insights = 可视化和智能监控层**
* **Log Analytics = 底层的日志存储和查询引擎**

简而言之：

> Log Analytics 是数据*存放*和*被分析*的地方。
> Insights 是你*查看和解读*这些数据以用于特定资源类型的方式。

---

### **示例**

如果你在某个 Web 应用上启用 **Application Insights**：

* 它会收集遥测数据（请求、依赖项、跟踪、异常）。
* 这些数据存储在 **一个 Log Analytics 工作区**中。
* 你可以使用 **Log Analytics** 对相同的数据运行 KQL 查询，以进行更深度的自定义分析。

---

你想让我展示一个简单的 **KQL 示例**，说明 Log Analytics 如何查询 Application Insights 的数据吗？
