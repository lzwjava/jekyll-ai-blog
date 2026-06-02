---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: AWS CLI Essential Command Options
translated: false
type: note
---

Question: Provide a comprehensive introduction to AWS CLI command options.

Answer:

The **AWS Command Line Interface (AWS CLI)** is a unified tool for managing AWS services from the terminal. Most commands follow this general structure:

```bash
aws [global options] <service> <operation> [parameters]
```

Example:
```bash
aws s3 ls s3://my-bucket --recursive --profile dev --region us-east-1 --output table
```

### Global Options (most important command-line flags)

These options can be placed **before** the service name and override configuration from files, environment variables, and defaults. They apply to almost every command.

| Option                  | Type      | Description                                                                 | Common Use Case                              | Example                                      |
|-------------------------|-----------|-----------------------------------------------------------------------------|----------------------------------------------|----------------------------------------------|
| `--profile <value>`     | string    | Selects a named profile from `~/.aws/credentials` and `~/.aws/config`      | Working with multiple AWS accounts           | `--profile prod`                             |
| `--region <value>`      | string    | Overrides the AWS Region (e.g., us-east-1, eu-west-1)                       | Targeting specific region                    | `--region ap-southeast-2`                    |
| `--output <value>`      | string    | Changes output format: `json` (default), `text`, `table`, `yaml`, `yaml-stream` | Human-readable output vs machine parsing     | `--output table`                             |
| `--debug`               | boolean   | Enables detailed debug logging                                              | Troubleshooting API calls                    | `--debug`                                    |
| `--endpoint-url <url>`  | string    | Overrides the service endpoint (useful for local stacks, custom endpoints) | LocalStack, MinIO, VPC endpoints             | `--endpoint-url http://localhost:4566`       |
| `--no-verify-ssl`       | boolean   | Disables SSL certificate validation                                         | Self-signed certs in local/dev environments  | `--no-verify-ssl`                            |
| `--no-paginate`         | boolean   | Disables automatic pagination (returns first page only)                    | Scripting when you want full control         | `--no-paginate`                              |
| `--query <JMESPath>`    | string    | Filters output using JMESPath expression                                    | Extracting specific fields                   | `--query "Reservations[].Instances[].InstanceId"` |
| `--cli-read-timeout`    | integer   | Socket read timeout in seconds (default 60)                                 | Very slow/large responses                    | `--cli-read-timeout 300`                     |
| `--cli-connect-timeout` | integer   | Connection timeout in seconds (default 60)                                  | Unreliable networks                          | `--cli-connect-timeout 30`                   |
| `--color <value>`       | string    | Controls color output: `on`, `off`, `auto`                                  | Terminal color preferences                   | `--color off`                                |
| `--version`             | —         | Shows AWS CLI version                                                       | Checking installed version                   | `aws --version`                              |

**Most frequently used combination**:
```bash
aws ec2 describe-instances \
  --profile sandbox \
  --region eu-central-1 \
  --output table \
  --query "Reservations[].Instances[].[InstanceId,State.Name,InstanceType]"
```

### Service-specific parameters vs global options

- **Global options** → listed above — placed **before** the service name
- **Service parameters** → specific to the operation — placed **after** the operation name

```bash
aws ec2 describe-instances   ← global options go here
  --instance-ids i-0123456789abcdef0   ← service parameters go here
  --filters "Name=tag:Environment,Values=prod"
```

### Output control – the most powerful trio

1. `--output table` → best for humans
2. `--output json` + `--query` → best for scripting / jq
3. `--output text` → simple, tab-separated, good for shell scripts

Example combining them:
```bash
aws s3api list-objects-v2 \
  --bucket my-bucket \
  --query "Contents[].{Key:Key, Size:Size}" \
  --output table
```

### Quick reference – precedence order (highest to lowest)

1. Command line options
2. Environment variables (`AWS_REGION`, `AWS_PROFILE`, `AWS_OUTPUT`, …)
3. AWS config/credentials files (`~/.aws/config`, `~/.aws/credentials`)
4. AWS CLI defaults

### Practical tips

- Use `--cli-auto-prompt` (v2) for interactive mode when learning commands
- Combine `--debug` + `> debug.log 2>&1` when something fails mysteriously
- Prefer named profiles over changing environment variables repeatedly
- For local development / testing → `--endpoint-url` + `--no-verify-ssl` is very common

These global options give you enormous flexibility without changing configuration files every time.

References:

- [AWS CLI Command Reference - Global Options](https://docs.aws.amazon.com/cli/latest/reference/)
- [Command line options in the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-options.html)
- [Command structure in the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-commandstructure.html)
