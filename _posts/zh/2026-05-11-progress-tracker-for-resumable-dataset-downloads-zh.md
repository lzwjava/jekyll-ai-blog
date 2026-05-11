---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 可恢复数据集下载进度跟踪器
translated: true
type: note
---

- progress.json 与 parquet 文件一同位于输出目录中。它存储所选分片计划，每个分片的状态为：pending（待处理）或 done（已完成）。
  - 首次运行时：列出 Hugging Face 上的分片，选择 1000 亿 token 的切片，写入 progress.json，然后开始下载。
  - 在分片下载中途取消（Ctrl-C）：正在传输的分片会留下一个 .part 文件。JSON 中仍将其标记为 pending。
  - 重新启动时：加载 progress.json（无需调用 HF API），立即跳过已完成的分片，通过 HTTP Range 恢复 .part 文件的下载——仅继续下载该分片。
  - 使用 --refresh-plan 参数可强制从 Hub 重新列出分片，以获取新计划。

每个分片完成后状态会通过 fsync 同步（通过 .tmp + os.replace 实现原子操作），因此崩溃不会导致 JSON 不一致。