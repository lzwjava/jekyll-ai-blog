---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Azure Application Insights Setup Guide
translated: false
type: note
---

## What is Azure Application Insights?

Azure Application Insights is an application performance management (APM) service in Azure Monitor that helps you monitor live web applications. It provides tools for detecting issues, diagnosing problems, and understanding user behavior through telemetry data like requests, dependencies, traces, metrics, and logs. It's now powered by OpenTelemetry for broader compatibility.

## Prerequisites

- An active Azure subscription.
- Permissions to create resources in Azure (e.g., Owner or Contributor role).
- Your application code (supports .NET, Java, Node.js, Python, and more).

## Step 1: Create an Application Insights Resource

1. Sign in to the [Azure portal](https://portal.azure.com).
2. Click **Create a resource** in the top-left menu.
3. Search for "Application Insights" and select it from the results under **Monitoring + management**.
4. Fill in the details:
   - **Subscription**: Choose your Azure subscription.
   - **Resource Group**: Select an existing one or create a new one.
   - **Name**: Give your resource a unique name.
   - **Region**: Choose a region close to your users or app.
   - **Workspace**: Optionally link to an existing Log Analytics workspace; otherwise, a new one is created automatically.
5. Review and click **Create**. Deployment takes a few minutes.
6. Once created, go to your resource's **Overview** page and copy the **Connection string** (hover over it and click the copy icon). This identifies where your app sends telemetry data.

**Tip**: Use separate resources for dev, test, and prod environments to avoid mixing data.

## Step 2: Instrument Your Application

Add OpenTelemetry support to collect telemetry automatically (requests, exceptions, metrics, etc.). Set the connection string via an environment variable named `APPLICATIONINSIGHTS_CONNECTION_STRING` (recommended for production).

### For .NET (ASP.NET Core)

1. Install the NuGet package:

   ```
   dotnet add package Azure.Monitor.OpenTelemetry.AspNetCore
   ```

2. In `Program.cs`:

   ```csharp
   using Azure.Monitor.OpenTelemetry.AspNetCore;

   var builder = WebApplication.CreateBuilder(args);
   builder.Services.AddOpenTelemetry().UseAzureMonitor();
   var app = builder.Build();
   app.Run();
   ```

3. Set the environment variable with your connection string and run the app.

### For Java

1. Download the Azure Monitor OpenTelemetry Distro JAR (e.g., `applicationinsights-agent-3.x.x.jar`).
2. Create a config file `applicationinsights.json` in the same directory:

   ```json
   {
     "connectionString": "Your connection string here"
   }
   ```

3. Run your app with the agent: `java -javaagent:applicationinsights-agent-3.x.x.jar -jar your-app.jar`.

### For Node.js

1. Install the package:

   ```
   npm install @azure/monitor-opentelemetry
   ```

2. Configure in your app entry point:

   ```javascript
   const { AzureMonitorOpenTelemetry } = require('@azure/monitor-opentelemetry');
   const provider = new AzureMonitorOpenTelemetry({
     connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING
   });
   provider.start();
   ```

3. Set the environment variable and start your app.

### For Python

1. Install the package:

   ```
   pip install azure-monitor-opentelemetry
   ```

2. In your app:

   ```python
   from azure.monitor.opentelemetry import configure_azure_monitor
   configure_azure_monitor(connection_string="Your connection string here")
   ```

3. Run the app.

For other languages or auto-instrumentation (e.g., for Azure App Service), check the official docs. Test locally first.

## Step 3: View and Analyze Data

1. Run your instrumented app and generate some activity (e.g., send requests).
2. In the Azure portal, open your Application Insights resource.
3. Check the **Overview** page: See live metrics, request counts, and response times (data appears in ~1-2 minutes).
4. Explore features:
   - **Live Metrics**: Real-time stream for production apps.
   - **Failures**: Drill into exceptions and traces.
   - **Performance**: Analyze dependencies and slow requests.
   - **Usage**: Track user sessions and custom events.
   - **Alerts**: Set up notifications for issues (e.g., high failure rates).
5. Query data using Kusto Query Language (KQL) in **Logs** for custom analysis.

## Best Practices

- Start with basic telemetry; add custom events/metrics as needed.
- Monitor costs via the **Usage and estimated costs** page (billed through Log Analytics).
- For browser monitoring, add the JavaScript SDK snippet to your web pages.

[Create and configure Application Insights resources](https://learn.microsoft.com/en-us/azure/azure-monitor/app/create-workspace-resource)
[Enable OpenTelemetry in Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable)
[Application Insights overview](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
