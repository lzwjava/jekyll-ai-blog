---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: AWS CLI 常用命令选项
translated: true
type: note
---

Question: 请对 AWS CLI 命令选项进行全面的介绍。

Answer:

**AWS Command Line Interface (AWS CLI)** 是从终端管理 AWS 服务的统一工具。大多数命令遵循以下通用结构：

```bash
aws [global options] <service> <operation> [parameters]
```

示例：
```bash
aws s3 ls s3://my-bucket --recursive --profile dev --region us-east-1 --output table
```

### 全局选项 Global Options (最重要的命令行标志)

这些选项可以放置在服务名称之**前**，并会覆盖来自文件、环境变量和默认值的配置。它们几乎适用于每一个命令。

| 选项                    | 类型      | 描述                                                                        | 常见用例                                     | 示例                                         |
|-------------------------|-----------|-----------------------------------------------------------------------------|----------------------------------------------|----------------------------------------------|
| `--profile <value>`     | string    | 从 `~/.aws/credentials` 和 `~/.aws/config` 中选择命名配置文件                | 处理多个 AWS 账号                            | `--profile prod`                             |
| `--region <value>`      | string    | 覆盖 AWS Region (例如 us-east-1, eu-west-1)                                 | 针对特定区域                                 | `--region ap-southeast-2`                    |
| `--output <value>`      | string    | 更改输出格式: `json` (默认), `text`, `table`, `yaml`, `yaml-stream`           | 人类可读输出 vs 机器解析                     | `--output table`                             |
| `--debug`               | boolean   | 启用详细的 debug 日志                                                       | 排除 API 调用故障                             | `--debug`                                    |
| `--endpoint-url <url>`  | string    | 覆盖服务 endpoint (对 local stacks, 自定义 endpoint 有用)                    | LocalStack, MinIO, VPC endpoints             | `--endpoint-url http://localhost:4566`       |
| `--no-verify-ssl`       | boolean   | 禁用 SSL 证书验证                                                           | 本地/开发环境中的自签名证书                  | `--no-verify-ssl`                            |
| `--no-paginate`         | boolean   | 禁用自动分页 (仅返回第一页)                                                  | 需要完全控制时的脚本编写                     | `--no-paginate`                              |
| `--query <JMESPath>`    | string    | 使用 JMESPath 表达式过滤输出                                                | 提取特定字段                                 | `--query "Reservations[].Instances[].InstanceId"` |
| `--cli-read-timeout`    | integer   | Socket 读取超时时间，以秒为单位 (默认 60)                                   | 响应非常慢或非常大的情况                     | `--cli-read-timeout 300`                     |
| `--cli-connect-timeout` | integer   | 连接超时时间，以秒为单位 (默认 60)                                         | 网络不稳定时                                 | `--cli-connect-timeout 30`                   |
| `--color <value>`       | string    | 控制彩色输出: `on`, `off`, `auto`                                           | 终端颜色偏好                                 | `--color off`                                |
| `--version`             | —         | 显示 AWS CLI 版本                                                           | 检查安装的版本                               | `aws --version`                              |

**最常用的组合**:
```bash
aws ec2 describe-instances \
  --profile sandbox \
  --region eu-central-1 \
  --output table \
  --query "Reservations[].Instances[].[InstanceId,State.Name,InstanceType]"
```

### 服务特定参数 vs 全局选项

- **全局选项 Global options** → 如上所述 — 放置在服务名称之**前**
- **服务参数 Service parameters** → 操作特定的参数 — 放置在操作名称之**后**

```bash
aws ec2 describe-instances   ← 在此处放置全局选项
  --instance-ids i-0123456789abcdef0   ← 在此处放置服务参数
  --filters "Name=tag:Environment,Values=prod"
```

### 输出控制 – 最强大的三剑客

1. `--output table` → 对人类最友好
2. `--output json` + `--query` → 最适合脚本编写 / jq
3. `--output text` → 简单的制表符分隔，适合 shell 脚本

结合使用的示例：
```bash
aws s3api list-objects-v2 \
  --bucket my-bucket \
  --query "Contents[].{Key:Key, Size:Size}" \
  --output table
```

### 快速参考 – 优先级顺序 (从高到低)

1. 命令行选项 (Command line options)
2. 环境变量 (`AWS_REGION`, `AWS_PROFILE`, `AWS_OUTPUT`, …)
3. AWS config/credentials 文件 (`~/.aws/config`, `~/.aws/credentials`)
4. AWS CLI 默认值

### 实用技巧

- 学习命令时，使用 `--cli-auto-prompt` (v2) 进入交互模式
- 当出现莫名故障时，结合使用 `--debug` + `> debug.log 2>&1`
- 优先使用命名 profile，而不是反复更改环境变量
- 对于本地开发 / 测试 → `--endpoint-url` + `--no-verify-ssl` 非常常用

这些全局选项为您提供了极大的灵活性，而无需每次都修改配置文件。

References:

- [AWS CLI Command Reference - Global Options](https://docs.aws.amazon.com/cli/latest/reference/)
- [Command line options in the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-options.html)
- [Command structure in the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-commandstructure.html)
