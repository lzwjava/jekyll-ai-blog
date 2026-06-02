---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 读取AWS CloudWatch日志
translated: true
type: note
---

### AWS CloudWatch 日志读取指南
AWS CloudWatch Logs 是一项用于集中收集、监控和存储来自 AWS 资源（如 EC2 实例、Lambda 函数或 RDS 数据库）及应用程序日志文件的服务。要读取日志，首先需要确保日志已发送至 CloudWatch（例如通过 EC2 上的 CloudWatch 代理或其他服务的自动集成功能）。设置完成后，您可以通过 AWS 管理控制台、AWS CLI 或 SDK 编程方式查看日志。

### 前置条件
- **AWS 权限**：确保您的 IAM 用户或角色拥有 `logs:DescribeLogGroups`、`logs:DescribeLogStreams`、`logs:GetLogEvents` 和 `logs:FilterLogEvents` 权限（可附加 `CloudWatchLogsReadOnlyAccess` 策略）。
- **日志配置**：日志必须路由至 CloudWatch。例如：
  - 在 EC2 实例上安装 CloudWatch Logs 代理
  - 在 Lambda 或 ECS 等服务中启用日志功能
- **AWS CLI（可选）**：若使用 CLI，需通过 `aws configure` 安装并配置

### 通过 AWS 管理控制台查看日志
1. 登录 [AWS 管理控制台](https://console.aws.amazon.com/) 并打开 CloudWatch 服务
2. 在左侧导航栏选择 **Logs** > **Log groups**
3. 选择包含日志的日志组（例如 Lambda 日志的 `/aws/lambda/my-function`）
4. 在日志流列表（所选日志组下）中选择特定流（例如按实例或执行划分的流）
5. 日志事件将加载显示，可自定义视图：
   - **展开事件**：点击事件旁的箭头展开，或切换列表上方的 **Text** 视图查看纯文本
   - **过滤/搜索**：在搜索框中输入过滤条件（如 "ERROR" 仅显示错误行）
   - **时间范围**：点击搜索框旁的时间选择器，选择 **Relative**（如最近1小时）或 **Absolute**（自定义日期），并切换 UTC 与本地时间
6. 滚动查看事件或按需下载

若需跨多个流或组进行高级查询，可使用 **CloudWatch Logs Insights**（路径：Logs > Logs Insights）。通过类似 `fields @timestamp, @message | filter @level = "ERROR" | sort @timestamp desc` 的查询语句实现日志分析与可视化。

### 使用 AWS CLI 读取日志
通过以下命令以编程方式列出和获取日志，请将 `my-log-group` 等占位符替换为实际名称。

1. **列出日志组**：
   ```
   aws logs describe-log-groups --log-group-name-prefix my-log-group
   ```
   返回 ARN、保留策略和存储量等元数据

2. **列出日志组中的流**：
   ```
   aws logs describe-log-streams --log-group-name my-log-group --log-stream-name-prefix 2025
   ```
   按前缀过滤流（如基于日期的命名），显示创建时间与大小

3. **从日志流获取事件**：
   ```
   aws logs get-log-events --log-group-name my-log-group --log-stream-name my-stream --start-time 1730137600000
   ```
   - `--start-time` 与 `--end-time`：时间范围的 Unix 时间戳（毫秒）
   - `--limit`：返回事件上限（默认 1,000 条）
   - 输出包含时间戳、摄取时间和消息文本
   - 使用响应中的 `--next-token` 进行分页

跨流过滤搜索可使用 `filter-log-events`：
```
aws logs filter-log-events --log-group-name my-log-group --filter-pattern "ERROR" --start-time 1730137600000
```

### 技巧与最佳实践
- **保留策略**：日志默认永久保存，建议按组调整保留周期（如30天）以控制成本
- **费用说明**：查看日志免费，但摄取和存储会产生费用——可通过 CloudWatch 指标监控
- **故障排查**：若无日志显示，请验证代理安装或服务日志功能是否启用
- 实时监控可通过设置日志模式的指标过滤器或告警实现

[使用日志组和日志流 - Amazon CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html)
[AWS CLI 的 CloudWatch Logs 示例](https://docs.aws.amazon.com/cli/v1/userguide/cli_cloudwatch-logs_code_examples.html)
[使用 CloudWatch Logs Insights 分析日志数据](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)
