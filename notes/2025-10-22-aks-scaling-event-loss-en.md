---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Preventing Event Loss During AKS Scaling
translated: false
type: note
---

### Likely Cause of Event Loss
When your service auto-scales from 1 to 2 pods in Azure Kubernetes Service (AKS), the initial pod handles the increasing load alone until the new pod is ready (typically 1-2 minutes, depending on your Horizontal Pod Autoscaler (HPA) config). If event volume spikes during this window, your Event Hubs namespace may throttle ingress (e.g., due to insufficient throughput units), leading to ~1% loss (ServerBusy errors). Event Hubs provides at-least-once delivery, but without proper retries, throttled sends fail silently or drop events.

Scaling up itself doesn't disrupt the existing pod's connection—loss stems from transient overload, not pod termination.

### How to Fix and Configure
To handle this reliably:

1. **Enable Auto-Inflate on Event Hubs Namespace**
   This automatically scales throughput units (TUs) when ingress exceeds your baseline (e.g., from 1 to 20 TUs), preventing throttling during load spikes like scaling events.
   - In Azure Portal: Go to your Event Hubs namespace > **Settings** > **Scale** > Check **Enable auto-inflate** > Set max TUs (e.g., 20) > Save.
   - CLI: `az eventhubs namespace update --resource-group <rg> --name <namespace> --enable-auto-inflate true --maximum-throughput-units 20`
   - Cost: Billed per hour for the max reached; start with 5-10 TUs baseline.
   This ensures capacity grows proactively without manual intervention.

2. **Configure Producer Client for Retries and Reliability**
   Use the Azure Event Hubs SDK in your app code to implement exponential backoff retries on transient errors (throttling, timeouts). Defaults are often 3 retries with 60s timeout—tune for your needs. Batch events (e.g., 100-500 per send) to reduce API calls and improve resilience.
   - **General Best Practices**:
     - Set max retries: 5-10.
     - Exponential backoff: Start at 1s, max delay 30s.
     - Connection timeout: 30-60s.
     - Use idempotent keys (e.g., UUID per event) if duplicates are tolerable (Event Hubs supports this in Premium/Dedicated tiers).
     - Monitor via Azure Monitor: Track `IncomingMessages` vs. `ThrottledRequests` metrics.

   - **Example: .NET (Azure.Messaging.EventHubs)**
     ```csharp
     using Azure.Messaging.EventHubs;
     using Azure.Messaging.EventHubs.Producer;

     var connectionString = "<your-connection-string>";
     var eventHubName = "<your-eventhub-name>";

     var clientOptions = new EventHubProducerClientOptions
     {
         Retry = new EventHubsRetryOptions
         {
             TryTimeout = TimeSpan.FromSeconds(60),  // Per-operation timeout
             MaximumTries = 7,  // Max retries
             Delay = TimeSpan.FromSeconds(2),  // Initial backoff
             MaximumDelay = TimeSpan.FromSeconds(30),  // Max backoff
             Mode = RetryMode.Exponential  // Backoff strategy
         },
         ConnectionOptions = new EventHubConnectionOptions
         {
             TransportType = EventHubsTransportType.AmqpWebSockets  // For AKS networking
         }
     };

     await using var producer = new EventHubProducerClient(connectionString, eventHubName, clientOptions);

     // Send batch
     using var batch = await producer.CreateBatchAsync(new CreateBatchOptions { PartitionKey = "your-key" });
     batch.TryAdd(new EventData(Encoding.UTF8.GetBytes("event-data")));
     await producer.SendAsync(batch);
     ```
     This retries on ServerBusy, ensuring events land post-scale.

   - **Example: Java (Azure Event Hubs Client)**
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
         .transportType(TransportType.AMQP_WEB_SOCKETS)  // For AKS
         .buildAsyncClient();

     // Send batch
     Flux<PartitionInformation> partitions = producer.getPartitionPropertiesFlux();
     // ... logic to send batch with retries built-in
     ```
     The SDK handles retries transparently on errors.

   - **Other Languages**: Similar patterns in Python (azure-eventhub), Node.js (use retry options in EventHubProducerClient). See SDK docs for your stack.

3. **AKS-Specific Handling for Scaling**
   - **Proactive Scaling**: Tune HPA to scale earlier (e.g., target CPU 60% vs. 80%) to reduce overload window:
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
             averageUtilization: 60  # Scale at 60% CPU
     ```
     Apply with `kubectl apply -f hpa.yaml`.
   - **Graceful Pod Behavior**: Set `terminationGracePeriodSeconds: 30` in your Deployment YAML to allow buffered events to flush on future scale-downs (not directly for up, but good practice).
   - **Networking**: Use WebSockets (AMQP over WebSockets) in client options for better AKS egress handling.
   - **Monitoring**: Enable AKS diagnostics to Log Analytics; query for pod events during scale (e.g., `KubePodInventory | where TimeGenerated > ago(1h)`).

4. **Additional Safeguards**
   - **Zone-Redundant Namespace**: Enable in namespace creation (default in supported regions) for 99.99% SLA and no loss during zone failures.
   - **Partitions**: Use 4-32 partitions based on load (e.g., match expected parallel producers); assign partition keys for ordered grouping.
   - **Capture Feature**: Enable Event Hubs Capture to Blob Storage as a backup for any rare losses (Premium tier).
   - **Test**: Simulate load with tools like Apache JMeter; monitor for zero throttling post-config.

This setup should drop loss to near-zero. Start with auto-inflate + client retries for quick wins.

### References
- [Reliability in Azure Event Hubs](https://learn.microsoft.com/en-us/azure/reliability/reliability-event-hubs)
- [Scaling with Event Hubs](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-scalability)
- [Event Hubs .NET SDK Retry Options](https://learn.microsoft.com/en-us/dotnet/api/azure.messaging.eventhubs.producer.eventhubproducerclientoptions.retryoptions)
- [AKS Scaling Concepts](https://learn.microsoft.com/en-us/azure/aks/concepts-scale)
