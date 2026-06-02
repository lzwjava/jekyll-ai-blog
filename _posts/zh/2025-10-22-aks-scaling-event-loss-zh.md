---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 防止AKS扩展期间的事件丢失
translated: true
type: note
---

### 事件丢失的可能原因
当您的服务在 Azure Kubernetes Service (AKS) 中从 1 个 Pod 自动扩展到 2 个 Pod 时，初始 Pod 会独自处理不断增长的负载，直到新 Pod 准备就绪（通常需要 1-2 分钟，具体取决于您的 Horizontal Pod Autoscaler (HPA) 配置）。如果事件量在此时间窗口内激增，您的 Event Hubs 命名空间可能会限制入口（例如，由于吞吐量单位不足），导致约 1% 的事件丢失（ServerBusy 错误）。Event Hubs 提供至少一次交付保证，但如果没有适当的重试机制，受限制的发送操作会静默失败或丢弃事件。

扩展本身不会中断现有 Pod 的连接——事件丢失源于瞬时过载，而非 Pod 终止。

### 修复和配置方法
要可靠地处理此问题：

1. **在 Event Hubs 命名空间上启用自动扩容**
   这会在入口流量超过基线时自动扩展吞吐量单位（TU）（例如从 1 TU 扩展到 20 TU），防止在扩展事件等负载激增期间发生限制。
   - 在 Azure 门户中：转到您的 Event Hubs 命名空间 > **设置** > **缩放** > 勾选**启用自动扩容** > 设置最大 TU（例如 20）> 保存。
   - CLI：`az eventhubs namespace update --resource-group <rg> --name <namespace> --enable-auto-inflate true --maximum-throughput-units 20`
   - 成本：按达到的最大值每小时计费；建议从 5-10 TU 的基线开始。
   这能确保容量主动增长，无需手动干预。

2. **配置生产者客户端以实现重试和可靠性**
   在应用代码中使用 Azure Event Hubs SDK 对瞬时错误（限制、超时）实现指数退避重试。默认设置通常为 3 次重试和 60 秒超时——请根据您的需求进行调整。批量处理事件（例如，每次发送 100-500 个事件）以减少 API 调用并提高弹性。
   - **通用最佳实践**：
     - 设置最大重试次数：5-10 次。
     - 指数退避：从 1 秒开始，最大延迟 30 秒。
     - 连接超时：30-60 秒。
     - 如果允许重复事件，请使用幂等键（例如，每个事件使用 UUID）（Event Hubs 在 Premium/Dedicated 层级支持此功能）。
     - 通过 Azure Monitor 进行监控：跟踪 `IncomingMessages` 与 `ThrottledRequests` 指标。

   - **示例：.NET (Azure.Messaging.EventHubs)**
     ```csharp
     using Azure.Messaging.EventHubs;
     using Azure.Messaging.EventHubs.Producer;

     var connectionString = "<your-connection-string>";
     var eventHubName = "<your-eventhub-name>";

     var clientOptions = new EventHubProducerClientOptions
     {
         Retry = new EventHubsRetryOptions
         {
             TryTimeout = TimeSpan.FromSeconds(60),  // 每次操作超时时间
             MaximumTries = 7,  // 最大重试次数
             Delay = TimeSpan.FromSeconds(2),  // 初始退避延迟
             MaximumDelay = TimeSpan.FromSeconds(30),  // 最大退避延迟
             Mode = RetryMode.Exponential  // 退避策略
         },
         ConnectionOptions = new EventHubConnectionOptions
         {
             TransportType = EventHubsTransportType.AmqpWebSockets  // 适用于 AKS 网络
         }
     };

     await using var producer = new EventHubProducerClient(connectionString, eventHubName, clientOptions);

     // 发送批次
     using var batch = await producer.CreateBatchAsync(new CreateBatchOptions { PartitionKey = "your-key" });
     batch.TryAdd(new EventData(Encoding.UTF8.GetBytes("event-data")));
     await producer.SendAsync(batch);
     ```
     这会在发生 ServerBusy 错误时重试，确保事件在扩展后成功送达。

   - **示例：Java (Azure Event Hubs Client)**
     ```java
     import com.azure.messaging.eventhubs.EventHubProducerAsyncClient;
     import com.azure.messaging.eventhubs.EventHubProducerClientBuilder;
     import com.azure.messaging.eventhubs.models.CreateBatchOptions;
     import com.azure.messaging.eventhubs.models.EventHubProducerAsyncClientBuilder;
     import com.azure.core.amqp.AmqpRetryOptions;

     String connectionString = "<your-connection-string>";
     String eventHubName = "<your-eventhub-name>";

     AmqpRetryOptions retryOptions = new AmqpRetryOptions()
         .setMaxRetries(7)
         .setInitialDelay(Duration.ofSeconds(2))
         .setMaxDelay(Duration.ofSeconds(30))
         .setTryTimeout(Duration.ofSeconds(60));

     EventHubProducerAsyncClient producer = new EventHubProducerClientBuilder()
         .connectionString(connectionString, eventHubName)
         .retryOptions(retryOptions)
         .transportType(TransportType.AMQP_WEB_SOCKETS)  // 适用于 AKS
         .buildAsyncClient();

     // 发送批次
     Flux<PartitionInformation> partitions = producer.getPartitionPropertiesFlux();
     // ... 发送批次逻辑，内置重试机制
     ```
     SDK 会在出错时透明地处理重试。

   - **其他语言**：Python (azure-eventhub)、Node.js（在 EventHubProducerClient 中使用重试选项）有类似模式。请参阅您所用技术栈的 SDK 文档。

3. **针对扩展的 AKS 特定处理**
   - **主动扩展**：调整 HPA 以更早开始扩展（例如，目标 CPU 使用率为 60% 而非 80%），以缩短过载窗口：
     ```yaml
     apiVersion: autoscaling/v2
     kind: HorizontalPodAutoscaler
     metadata:
       name: your-app-hpa
     spec:
       scaleTargetRef:
         apiVersion: apps/v1
         kind: Deployment
         name: your-app
       minReplicas: 1
       maxReplicas: 10
       metrics:
       - type: Resource
         resource:
           name: cpu
           target:
             type: Utilization
             averageUtilization: 60  # 在 CPU 使用率达到 60% 时扩展
     ```
     使用 `kubectl apply -f hpa.yaml` 应用配置。
   - **优雅的 Pod 行为**：在您的 Deployment YAML 中设置 `terminationGracePeriodSeconds: 30`，以便在将来缩容时允许缓冲的事件被刷新（虽然不直接针对扩容，但这是良好实践）。
   - **网络**：在客户端选项中使用 WebSockets（AMQP over WebSockets）以更好地处理 AKS 出口流量。
   - **监控**：启用 AKS 诊断到 Log Analytics；在扩展期间查询 Pod 事件（例如：`KubePodInventory | where TimeGenerated > ago(1h)`）。

4. **额外保障措施**
   - **区域冗余命名空间**：在命名空间创建时启用（在受支持区域中默认启用），以实现 99.99% SLA 并在区域故障期间无事件丢失。
   - **分区**：根据负载使用 4-32 个分区（例如，匹配预期的并行生产者数量）；分配分区键以实现有序分组。
   - **捕获功能**：启用 Event Hubs Capture 到 Blob Storage，作为任何罕见丢失的备份（Premium 层级）。
   - **测试**：使用 Apache JMeter 等工具模拟负载；在配置后监控是否实现零限制。

此设置应将事件丢失降至接近零。首先实施自动扩容和客户端重试以获得快速成效。

### 参考文档
- [Azure Event Hubs 中的可靠性](https://learn.microsoft.com/zh-cn/azure/reliability/reliability-event-hubs)
- [使用 Event Hubs 进行扩展](https://learn.microsoft.com/zh-cn/azure/event-hubs/event-hubs-scalability)
- [Event Hubs .NET SDK 重试选项](https://learn.microsoft.com/zh-cn/dotnet/api/azure.messaging.eventhubs.producer.eventhubproducerclientoptions.retryoptions)
- [AKS 扩展概念](https://learn.microsoft.com/zh-cn/azure/aks/concepts-scale)
