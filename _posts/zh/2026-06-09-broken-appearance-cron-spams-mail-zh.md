---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 破碎外观Cron发送垃圾邮件
translated: true
type: note
---

以下是完整情况：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
系统 CRONTAB（crontab -l）  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

  */10* ***/opt/homebrew/bin/ww appearance smart-auto  
  0*** *     /opt/homebrew/bin/ww projects update  

  两个任务：每10分钟检查外观，每小时执行 git pull。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
ww projects update — 运行中  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

- 配置：148个仓库，分布在8个类别（ai-models、ai-training、ai-inference、ai-apps、ai-agents、dev-tools、infra-network、web-platforms）  
- 本地缺失2个仓库：TensorRT-LLM、rocBLAS（已干净跳过）  
- 最近一次运行：134个当前，12个已更新，0个失败（耗时27.9秒）  
- 主要更新：hermes-agent（265次提交）、warp（3次）、langfuse（1次）、desktop（15次）  
- 上次运行（来自邮件）：118个当前，26个已更新，2个失败（hermes-agent + desktop — 临时问题，现已解决）  

  结论：每小时执行的 cron 任务确实在正常工作——拉取上游的实际变更。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
邮件 — 163封 CRON 邮件（大部分为错误）  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

  140封 × "appearance smart-auto" — 故障（96%失败率）  
  23封 × "projects update" — 正常输出（成功邮件）  

  外观任务每10分钟向你的邮箱发送垃圾邮件，内容为：  

    FileNotFoundError: [Errno 2] No such file or directory: 'imagesnap'  

  根本原因：cron 运行时 PATH 为 /usr/bin:/bin — 不包含  
  /opt/homebrew/bin（imagesnap 所在目录）。该二进制文件已安装：  

    /opt/homebrew/bin/imagesnap  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
需要修复  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

  两种方案：  

  1. 在 crontab 中使用完整路径（最干净）：  
     将外观任务行改为：  
     PATH=/opt/homebrew/bin:/usr/bin:/bin  
     */10* ** * /opt/homebrew/bin/ww appearance smart-auto  

  2. 或者在 crontab 顶部添加 PATH 指令：  
     PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin  

  需要我修复 crontab 吗？另外，需要清除 /var/mail/lzwjava 中累积的163封 cron 邮件吗？  

  Hermes cron：0个任务（你正在使用系统 crontab）。
