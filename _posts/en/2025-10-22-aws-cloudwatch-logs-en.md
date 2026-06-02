---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Reading AWS CloudWatch Logs
translated: false
type: note
---

### Introduction to Reading Logs in AWS CloudWatch

AWS CloudWatch Logs is a service that centralizes, monitors, and stores log files from your AWS resources (like EC2 instances, Lambda functions, or RDS databases) and applications. To read logs, you first need to ensure logs are being sent to CloudWatch (e.g., via the CloudWatch agent on EC2 or automatic integration with other services). Once set up, you can view logs through the AWS Management Console, AWS CLI, or programmatically via SDKs.

### Prerequisites

- **AWS Permissions**: Ensure your IAM user or role has `logs:DescribeLogGroups`, `logs:DescribeLogStreams`, `logs:GetLogEvents`, and `logs:FilterLogEvents` permissions (attach the `CloudWatchLogsReadOnlyAccess` policy).
- **Logs Configuration**: Logs must be routed to CloudWatch. For example:
  - Install the CloudWatch Logs agent on EC2 instances.
  - Enable logging in services like Lambda or ECS.
- **AWS CLI (Optional)**: If using the CLI, install and configure it with `aws configure`.

### Viewing Logs in the AWS Management Console

1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/) and open the CloudWatch service.
2. In the left navigation pane, choose **Logs** > **Log groups**.
3. Select the log group containing your logs (e.g., `/aws/lambda/my-function` for Lambda logs).
4. In the list of log streams (under the selected log group), choose the specific stream (e.g., one per instance or execution).
5. The log events will load. Customize the view:
   - **Expand Events**: Click the arrow next to an event to expand it, or switch to **Text** view above the list for plain text.
   - **Filter/Search**: Enter a filter in the search box (e.g., "ERROR" to show only error lines).
   - **Time Range**: Click the time selector next to the search box. Choose **Relative** (e.g., last 1 hour) or **Absolute** (custom dates), and toggle between UTC and local time.
6. Scroll through the events or download them as needed.

For advanced querying across multiple streams or groups, use **CloudWatch Logs Insights** (under Logs > Logs Insights). Write queries like `fields @timestamp, @message | filter @level = "ERROR" | sort @timestamp desc` to analyze and visualize logs.

### Reading Logs Using AWS CLI

Use these commands to list and retrieve logs programmatically. Replace placeholders like `my-log-group` with your actual names.

1. **List Log Groups**:

   ```
   aws logs describe-log-groups --log-group-name-prefix my-log-group
   ```

   This returns metadata like ARN, retention, and stored bytes.

2. **List Log Streams in a Group**:

   ```
   aws logs describe-log-streams --log-group-name my-log-group --log-stream-name-prefix 2025
   ```

   Filters streams by prefix (e.g., date-based names) and shows creation time and size.

3. **Get Log Events from a Stream**:

   ```
   aws logs get-log-events --log-group-name my-log-group --log-stream-name my-stream --start-time 1730137600000
   ```

   - `--start-time` and `--end-time`: Unix timestamps (milliseconds) for the time range.
   - `--limit`: Max events to return (default 1,000).
   - Output includes timestamps, ingestion time, and message text.
   - Use `--next-token` from the response to paginate.

For filtered searches across streams, use `filter-log-events`:

```
aws logs filter-log-events --log-group-name my-log-group --filter-pattern "ERROR" --start-time 1730137600000
```

### Tips and Best Practices

- **Retention**: Logs are kept indefinitely by default; adjust per group to manage costs (e.g., 30 days).
- **Costs**: Viewing is free, but ingestion and storage incur charges—monitor via CloudWatch metrics.
- **Troubleshooting**: If no logs appear, verify agent installation or service logging is enabled.
- For real-time monitoring, set up metric filters or alarms on log patterns.

[Working with log groups and log streams - Amazon CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html)
[CloudWatch Logs examples using AWS CLI](https://docs.aws.amazon.com/cli/v1/userguide/cli_cloudwatch-logs_code_examples.html)
[Analyzing log data with CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)
