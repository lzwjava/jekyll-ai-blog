---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Azure Monitor Alerts Overview
translated: false
type: note
---

### Overview of Alerts in Azure

Azure Monitor alerts are a feature of Azure Monitor that proactively notify you when specific conditions are met in your Azure resources, helping you detect and resolve issues before they impact users. They work by evaluating data from metrics, logs, or activity logs against predefined rules. When a condition is triggered (e.g., CPU usage exceeds 80%), an alert fires, which can send notifications via email, SMS, or trigger automated actions like running a script.

Alerts are stateful (they resolve automatically when the issue clears) or stateless (they fire repeatedly until manually closed), depending on your configuration. They support monitoring across single or multiple resources and are charged based on the number of time series monitored.

#### Types of Alerts

Azure Monitor supports several alert types tailored to different data sources:

| Alert Type | Description | Best For |
| ------------------------- | ------------- | ---------- |
| **Metric Alerts** | Evaluate numerical metrics (e.g., CPU percentage, disk space) at regular intervals. Supports static or dynamic thresholds (AI-based). | Performance monitoring of VMs, databases, or apps. |
| **Log Search Alerts** | Run queries on Log Analytics data to detect patterns in logs. | Complex event analysis, like error spikes in application logs. |
| **Activity Log Alerts** | Trigger on administrative or operational events (e.g., resource creation/deletion). | Security and compliance auditing. |
| **Smart Detection Alerts** | AI-driven anomaly detection for web apps via Application Insights. | Automatic issue spotting in apps. |
| **Prometheus Alerts** | Query Prometheus metrics in managed services like AKS. | Container and Kubernetes environments. |

For most use cases, start with metric or log alerts.

### Prerequisites

- An Azure subscription with active resources to monitor.
- Permissions: Reader role on the target resource, Contributor on the resource group for the alert rule, and Reader on any action groups.
- Familiarity with the Azure portal (portal.azure.com).

### How to Create and Use a Metric Alert Rule (Step-by-Step)

Metric alerts are a common starting point. Here's how to create one in the Azure portal. This process takes about 5-10 minutes.

1. **Sign in to the Azure Portal**: Go to [portal.azure.com](https://portal.azure.com) and log in.

2. **Navigate to Alerts**:
   - From the home page, search for and select **Monitor**.
   - In the left menu, under **Insights**, select **Alerts**.
   - Click **+ Create** > **Alert rule**.

   *Alternative*: From a specific resource (e.g., a VM), select **Alerts** in the left menu, then **+ Create** > **Alert rule**. This auto-sets the scope.

3. **Set the Scope**:
   - In the **Select a resource** pane, choose your subscription, resource type (e.g., Virtual machines), and specific resource.
   - Click **Apply**. (For multi-resource alerts, select multiple resources of the same type in one region.)

4. **Configure the Condition**:
   - On the **Condition** tab, click **Signal name** and select a metric (e.g., "Percentage CPU" for a VM).
     - Use **See all signals** to filter by type (e.g., Platform metrics).
   - Preview data: Set a time range (e.g., last 24 hours) to see historical values.
   - Set **Alert logic**:
     - **Threshold**: Static (e.g., > 80) or Dynamic (AI-adjusted based on history).
     - **Operator**: Greater than, Less than, etc.
     - **Aggregation**: Average, Sum, Min, Max over the evaluation period.
     - For dynamic: Choose sensitivity (Low/Medium/High).
   - (Optional) **Split by dimensions**: Filter by attributes like instance name for granular alerts (e.g., per VM in a set).
   - **Evaluation**: Check every 1-5 minutes; look back 5-15 minutes.
   - Click **Done**.

5. **Add Actions (Optional but Recommended)**:
   - On the **Actions** tab, select **Add action groups**.
   - Choose an existing group (for emails/SMS) or create one:
     - Add recipients (e.g., email admins).
     - Add actions like Logic Apps for automation or webhooks for integrations.
   - Click **Done**.

6. **Set Rule Details**:
   - On the **Details** tab:
     - **Subscription** and **Resource group**: Auto-filled; change if needed.
     - **Severity**: Sev 0 (Critical) to Sev 4 (Verbose).
     - **Alert rule name**: e.g., "High CPU Alert - Prod VM".
     - **Description**: Optional notes.
   - **Advanced options**:
     - Enable the rule on creation.
     - Auto-resolve alerts (makes it stateful).
   - Add tags if required for organization.

7. **Review and Create**:
   - Go to **Review + create**.
   - Validate (fix any errors, like invalid thresholds).
   - Click **Create**. The rule activates immediately if enabled.

Once created, the alert will fire when conditions are met, sending notifications and updating its status (e.g., "Fired" to "Resolved").

#### Managing Alerts

- **View Alerts**: In Monitor > Alerts, see active/fired alerts. Filter by time, severity, or resource.
- **Edit a Rule**: Go to Monitor > Alerts > Alert rules, select the rule, and click **Edit**.
- **Test**: Use the preview in step 4 to simulate.
- **Scale**: For multiple resources, use Azure CLI/PowerShell or ARM templates. Enable built-in recommended rules via resource insights.

### Best Practices

- Start simple: One condition per rule initially.
- Use dynamic thresholds for noisy metrics to reduce false positives.
- Integrate with action groups for automated remediation (e.g., scale up a VM).
- Monitor costs: Based on monitored series (free for basic use; check pricing).
- For logs, follow similar steps but select **Log alerts** in creation and write a KQL query.

For log alerts or other types, the process is analogous—replace the condition with a query.

[Overview of Azure Monitor alerts](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview)
[Create metric alert rule](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-create-metric-alert-rule)
[Create log alert rule](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-create-log-alert-rule)
[Azure Monitor pricing](https://azure.microsoft.com/en-us/pricing/details/monitor/)
