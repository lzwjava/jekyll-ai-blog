---
audio: false
generated: true
lang: zh
layout: post
title: GitHub Actions 定时任务调度
translated: true
type: note
---

是的，可以通过在 GitHub Actions 中使用 cron 计划来配置 GitHub 工作流，使其每天执行一次。

### 说明

GitHub Actions 允许您通过工作流自动化仓库中的任务，这些工作流定义在 `.github/workflows` 目录下的 YAML 文件中。触发工作流的一种方式是使用 `schedule` 事件，它采用类似 cron 的语法来指定工作流的运行时间。GitHub Actions 中的 cron 语法遵循标准 POSIX 格式，包含五个字段：分钟、小时、日期、月份和星期几。

要让工作流每天运行一次，可以使用如 `0 0 * * *` 的 cron 表达式，其含义是“每天 UTC 时间 00:00 运行”。具体解析如下：

- **分钟 (0)**：每小时的第 0 分钟
- **小时 (0)**：00:00（午夜）UTC
- **日期 (*)**：每月的每一天
- **月份 (*)**：每个月
- **星期几 (*)**：每周的每一天

### 示例配置

以下是一个每天运行一次的 GitHub Actions 工作流配置示例：

```yaml
name: 每日工作流
on:
  schedule:
    - cron: '0 0 * * *'
jobs:
  示例任务:
    runs-on: ubuntu-latest
    steps:
      - name: 输出信息
        run: echo "此任务每天运行一次！"
```

该工作流将在每天 UTC 时间午夜执行。

### 关键注意事项

- **时区**：计划任务基于 UTC 时间运行，如果需要按本地时区的特定时间执行，请相应调整 cron 表达式。
- **默认分支**：默认情况下，计划工作流会在仓库的默认分支（如 `main` 或 `master`）上运行，除非另有指定。
- **可靠性**：虽然 GitHub Actions 会尽力在指定时间运行工作流，但由于基础设施负载等原因，偶尔可能出现轻微延迟。
- **使用限制**：免费版 GitHub 账户对 Actions 使用有限制（例如每月运行分钟数），但单次日运行任务通常都在限制范围内。

### 结论

通过在工作流文件中正确配置 cron 表达式，GitHub Actions 确实可以每天执行一次工作流。因此，您的问题的答案是**肯定的**。
