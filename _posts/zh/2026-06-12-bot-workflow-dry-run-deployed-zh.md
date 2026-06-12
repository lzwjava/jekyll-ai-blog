---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 机器人工作流空跑部署
translated: true
type: note
---

已提交为 `eac1e05` 并推送至 `main` 分支。共涉及 13 个文件，575 行新增内容。

需要注意：`bot.yml` 工作流现已在 GitHub 上生效，因此交易循环将按计划开始运行（美国交易时段每 15 分钟一次，外加北京时间早 7 点/晚 9 点的报告）。这是安全的——`BOT_DRY_RUN` 仓库变量未设置，因此默认处于模拟运行模式，仅将信号记录到 Actions 日志中。当您准备正式上线时，请在 Settings → Secrets and variables → Actions → Variables 下设置仓库变量 `BOT_DRY_RUN=0`。
