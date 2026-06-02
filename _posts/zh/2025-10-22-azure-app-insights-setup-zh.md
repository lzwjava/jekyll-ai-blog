---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Azure Application Insights 配置指南
translated: true
type: note
---

## 什么是 Azure Application Insights？

Azure Application Insights 是 Azure Monitor 中的应用程序性能管理（APM）服务，可帮助您监控实时 Web 应用程序。它提供了一系列工具，通过请求、依赖项、跟踪、指标和日志等遥测数据来检测问题、诊断故障和理解用户行为。该服务现由 OpenTelemetry 提供支持，以实现更广泛的兼容性。

## 先决条件
- 一个有效的 Azure 订阅。
- 在 Azure 中创建资源的权限（例如，所有者或贡献者角色）。
- 您的应用程序代码（支持 .NET、Java、Node.js、Python 等）。

## 步骤 1：创建 Application Insights 资源
1. 登录 [Azure 门户](https://portal.azure.com)。
2. 点击左上角菜单中的 **创建资源**。
3. 搜索 "Application Insights"，并在 **监控 + 管理** 下的结果中选择它。
4. 填写详细信息：
   - **订阅**：选择您的 Azure 订阅。
   - **资源组**：选择现有的资源组或创建一个新的。
   - **名称**：为您的资源指定一个唯一名称。
   - **区域**：选择靠近您的用户或应用程序的区域。
   - **工作区**：可选择链接到现有的 Log Analytics 工作区；否则，将自动创建一个新的。
5. 检查并点击 **创建**。部署需要几分钟时间。
6. 创建完成后，转到您资源的 **概述** 页面，并复制 **连接字符串**（将鼠标悬停在其上并点击复制图标）。此字符串用于标识您的应用程序发送遥测数据的位置。

**提示**：为开发、测试和生产环境使用不同的资源，以避免数据混淆。

## 步骤 2：检测您的应用程序
添加 OpenTelemetry 支持以自动收集遥测数据（请求、异常、指标等）。建议在生产环境中通过名为 `APPLICATIONINSIGHTS_CONNECTION_STRING` 的环境变量设置连接字符串。

### 对于 .NET (ASP.NET Core)
1. 安装 NuGet 包：
   ```
   dotnet add package Azure.Monitor.OpenTelemetry.AspNetCore
   ```
2. 在 `Program.cs` 中：
   ```csharp
   using Azure.Monitor.OpenTelemetry.AspNetCore;

   var builder = WebApplication.CreateBuilder(args);
   builder.Services.AddOpenTelemetry().UseAzureMonitor();
   var app = builder.Build();
   app.Run();
   ```
3. 使用您的连接字符串设置环境变量并运行应用程序。

### 对于 Java
1. 下载 Azure Monitor OpenTelemetry Distro JAR（例如 `applicationinsights-agent-3.x.x.jar`）。
2. 在同一目录下创建配置文件 `applicationinsights.json`：
   ```json
   {
     "connectionString": "在此处填写您的连接字符串"
   }
   ```
3. 使用代理运行您的应用程序：`java -javaagent:applicationinsights-agent-3.x.x.jar -jar your-app.jar`。

### 对于 Node.js
1. 安装包：
   ```
   npm install @azure/monitor-opentelemetry
   ```
2. 在您的应用程序入口点进行配置：
   ```javascript
   const { AzureMonitorOpenTelemetry } = require('@azure/monitor-opentelemetry');
   const provider = new AzureMonitorOpenTelemetry({
     connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING
   });
   provider.start();
   ```
3. 设置环境变量并启动您的应用程序。

### 对于 Python
1. 安装包：
   ```
   pip install azure-monitor-opentelemetry
   ```
2. 在您的应用程序中：
   ```python
   from azure.monitor.opentelemetry import configure_azure_monitor
   configure_azure_monitor(connection_string="在此处填写您的连接字符串")
   ```
3. 运行应用程序。

对于其他语言或自动检测（例如，对于 Azure App Service），请查阅官方文档。建议首先在本地进行测试。

## 步骤 3：查看和分析数据
1. 运行您已检测的应用程序并生成一些活动（例如，发送请求）。
2. 在 Azure 门户中，打开您的 Application Insights 资源。
3. 检查 **概述** 页面：查看实时指标、请求计数和响应时间（数据大约在 1-2 分钟内出现）。
4. 探索功能：
   - **实时指标**：适用于生产应用程序的实时数据流。
   - **故障**：深入分析异常和跟踪。
   - **性能**：分析依赖项和慢请求。
   - **使用情况**：跟踪用户会话和自定义事件。
   - **警报**：针对问题（例如，高故障率）设置通知。
5. 在 **日志** 中使用 Kusto 查询语言（KQL）查询数据以进行自定义分析。

## 最佳实践
- 从基本遥测开始；根据需要添加自定义事件/指标。
- 通过 **使用情况和预估成本** 页面监控成本（通过 Log Analytics 计费）。
- 对于浏览器监控，请将 JavaScript SDK 代码片段添加到您的网页中。

[创建和配置 Application Insights 资源](https://learn.microsoft.com/en-us/azure/azure-monitor/app/create-workspace-resource)
[在 Application Insights 中启用 OpenTelemetry](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable)
[Application Insights 概述](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
