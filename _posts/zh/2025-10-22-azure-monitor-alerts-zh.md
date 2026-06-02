---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Azure Monitor 警报概述
translated: true
type: note
---

### Azure 警报概述

Azure Monitor 警报是 Azure Monitor 的一项功能，当 Azure 资源满足特定条件时主动通知您，帮助您在问题影响用户之前检测并解决问题。其工作原理是根据预定义规则评估来自指标、日志或活动日志的数据。当条件触发时（例如 CPU 使用率超过 80%），警报会触发，可以通过电子邮件、短信发送通知，或触发自动操作（如运行脚本）。

警报可以是有状态的（当问题清除时自动解决）或无状态的（在手动关闭前会重复触发），具体取决于您的配置。它们支持跨单个或多个资源的监控，并根据监控的时间序列数量进行计费。

#### 警报类型
Azure Monitor 支持多种警报类型，以适应不同的数据源：

| 警报类型              | 描述 | 最佳适用场景 |
|-------------------------|-------------|----------|
| **指标警报**      | 定期评估数值指标（例如 CPU 百分比、磁盘空间）。支持静态或动态阈值（基于 AI）。 | 虚拟机、数据库或应用程序的性能监控。 |
| **日志搜索警报**  | 对 Log Analytics 数据运行查询以检测日志中的模式。 | 复杂事件分析，例如应用程序日志中的错误峰值。 |
| **活动日志警报**| 在管理或操作事件（例如资源创建/删除）时触发。 | 安全性和合规性审计。 |
| **智能检测警报** | 通过 Application Insights 对 Web 应用进行 AI 驱动的异常检测。 | 自动发现应用中的问题。 |
| **Prometheus 警报**  | 在托管服务（如 AKS）中查询 Prometheus 指标。 | 容器和 Kubernetes 环境。 |

对于大多数用例，可以从指标警报或日志警报开始。

### 先决条件
- 一个 Azure 订阅，其中包含要监控的活动资源。
- 权限：目标资源上的读者角色、警报规则资源组上的参与者角色，以及任何操作组上的读者角色。
- 熟悉 Azure 门户 (portal.azure.com)。

### 如何创建和使用指标警报规则（分步指南）
指标警报是一个常见的起点。以下是在 Azure 门户中创建一个指标警报的方法。此过程大约需要 5-10 分钟。

1. **登录 Azure 门户**：访问 [portal.azure.com](https://portal.azure.com) 并登录。

2. **导航到警报**：
   - 在主页中，搜索并选择 **Monitor**。
   - 在左侧菜单的 **Insights** 下，选择 **Alerts**。
   - 点击 **+ 创建** > **Alert rule**。

   *替代方法*：从特定资源（例如虚拟机）的左侧菜单中选择 **Alerts**，然后点击 **+ 创建** > **Alert rule**。这将自动设置范围。

3. **设置范围**：
   - 在 **Select a resource** 窗格中，选择您的订阅、资源类型（例如 Virtual machines）和特定资源。
   - 点击 **Apply**。（对于多资源警报，请在同一区域中选择多个相同类型的资源。）

4. **配置条件**：
   - 在 **Condition** 选项卡上，点击 **Signal name** 并选择一个指标（例如，对于虚拟机，选择 "Percentage CPU"）。
     - 使用 **See all signals** 按类型（例如 Platform metrics）进行筛选。
   - 预览数据：设置时间范围（例如过去 24 小时）以查看历史值。
   - 设置 **Alert logic**：
     - **Threshold**：静态（例如 > 80）或动态（基于历史记录由 AI 调整）。
     - **Operator**：大于、小于等。
     - **Aggregation**：评估期间的平均值、总和、最小值、最大值。
     - 对于动态阈值：选择敏感度（低/中/高）。
   - （可选）**Split by dimensions**：按属性（例如实例名称）进行筛选，以实现细粒度警报（例如，针对集合中的每个虚拟机）。
   - **Evaluation**：每 1-5 分钟检查一次；回溯 5-15 分钟。
   - 点击 **Done**。

5. **添加操作（可选但推荐）**：
   - 在 **Actions** 选项卡上，选择 **Add action groups**。
   - 选择现有的操作组（用于电子邮件/SMS）或创建一个新的：
     - 添加收件人（例如，管理员电子邮件）。
     - 添加操作，例如用于自动化的 Logic Apps 或用于集成的 Webhook。
   - 点击 **Done**。

6. **设置规则详细信息**：
   - 在 **Details** 选项卡上：
     - **Subscription** 和 **Resource group**：自动填充；如有需要，可以更改。
     - **Severity**：Sev 0（严重）到 Sev 4（详细）。
     - **Alert rule name**：例如 "High CPU Alert - Prod VM"。
     - **Description**：可选的备注。
   - **Advanced options**：
     - 创建时启用规则。
     - 自动解决警报（使其成为有状态）。
   - 如果需要组织管理，可以添加标签。

7. **查看并创建**：
   - 转到 **Review + create**。
   - 验证（修复任何错误，例如无效的阈值）。
   - 点击 **Create**。如果已启用，规则将立即激活。

创建后，当满足条件时，警报将触发，发送通知并更新其状态（例如，从“已触发”变为“已解决”）。

#### 管理警报
- **查看警报**：在 Monitor > Alerts 中查看活动/已触发的警报。按时间、严重性或资源进行筛选。
- **编辑规则**：转到 Monitor > Alerts > Alert rules，选择规则，然后点击 **Edit**。
- **测试**：使用步骤 4 中的预览进行模拟。
- **扩展**：对于多个资源，使用 Azure CLI/PowerShell 或 ARM 模板。通过资源洞察启用内置推荐规则。

### 最佳实践
- 从简单开始：初始时每个规则一个条件。
- 对于噪声指标，使用动态阈值以减少误报。
- 与操作组集成以实现自动修复（例如，扩展虚拟机）。
- 监控成本：基于监控的序列（基本使用免费；请查看定价）。
- 对于日志警报，遵循类似的步骤，但在创建时选择 **Log alerts** 并编写 KQL 查询。

对于日志警报或其他类型，过程类似——将条件替换为查询即可。

[Azure Monitor 警报概述](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview)
[创建指标警报规则](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-create-metric-alert-rule)
[创建日志警报规则](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-create-log-alert-rule)
[Azure Monitor 定价](https://azure.microsoft.com/en-us/pricing/details/monitor/)
