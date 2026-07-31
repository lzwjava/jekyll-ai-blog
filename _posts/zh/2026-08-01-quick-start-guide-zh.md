---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 快速入门指南
translated: true
type: note
---

一切就绪 — `tb` v0.2.18 已安装（与此仓库匹配），Docker 正在运行，并且你的环境中已有 `DEEPSEEK_API_KEY` / `OPENROUTER_API_KEY`。以下是如何使用此仓库运行基准测试。

## 重要细节：任务文件夹位置

此仓库的最新提交将 `tasks/` 重命名为 `original-tasks/`（参见提交 `2af0e44`），但 CLI 仍然默认将 `--dataset-path` 设置为 `tasks`。因此，你**必须**始终显式传递 `--dataset-path`：

```bash
cd /mnt/data/terminal-bench

# 1) 先用一个任务进行冒烟测试（推荐）
tb run \
  --dataset-path original-tasks \
  --agent terminus \
  --model deepseek/deepseek-chat \
  -t "3d-model-format-legacy" \
  --n-concurrent 1

# 2) 按任务 ID 或通配符运行多个任务
tb run \
  --dataset-path original-tasks \
  --agent terminus \
  --model deepseek/deepseek-chat \
  -t "3d-*" \
  --n-concurrent 4

# 3) 运行此仓库中所有 241 个任务
tb run \
  --dataset-path original-tasks \
  --agent terminus \
  --model deepseek/deepseek-chat \
  --n-concurrent 4
```

## 关键标志说明

| 标志 | 作用 |
|---|---|
| `--dataset-path` | 指向此仓库的任务文件夹（`original-tasks`）——此处必须指定 |
| `--agent` | `terminus`（内置代理）、`naive`、`oracle`、`claude-code`、`aider`、`codex` 等 |
| `--model` | LiteLLM 命名方式：`deepseek/deepseek-chat`、`deepseek/deepseek-reasoner`、`openrouter/anthropic/claude-sonnet-4-...`、`openai/gpt-4o`、... |
| `-t / --task-id` | 特定任务 ID 或通配符模式；可重复使用；省略则运行所有任务 |
| `-e / --exclude-task-id` | 排除任务 |
| `--n-concurrent` | 并行试验数（默认 4） |
| `--n-attempts` | 每个任务的尝试次数（默认 1） |
| `--no-rebuild` | 重新运行时跳过重建 Docker 镜像（更快） |
| `--run-id` | 自定义运行名称（默认：时间戳） |
| `--output-path` | 结果目录（默认：`runs/`） |

## 无 LLM 的健全性检查（可选）

想在不消耗 token 的情况下验证测试框架是否正常工作？使用 **oracle** 代理，它仅运行参考解决方案——无需模型/API 密钥：

```bash
tb run --dataset-path original-tasks --agent oracle -t "3d-model-format-legacy"
```

## 查看结果

```bash
tb runs list               # 列出 ./runs 中的所有运行
tb runs summarize <run-id> # 通过/失败摘要及分数
tb runs status <run-id>    # 进度（已完成/未开始）
```

结果保存在 `runs/<run-id>/` 目录下（每个试验的 JSON 文件、日志等）。

## 提示

- 先从一个任务开始，配合 `--n-concurrent 1`，确认 Docker 镜像能构建且模型调用正常，然后再启动完整运行。
- 每个任务在首次运行时都会构建自己的 Docker 镜像——完整运行 241 个任务需要较长时间和大量磁盘空间；使用 `--n-concurrent` 来平衡速度与速率限制。
- 如果要下载发布的数据集而不是使用本地文件夹（例如排行榜集 `terminal-bench-core==0.1.1`），请使用 `--dataset terminal-bench-core==0.1.1`，并通过 `tb datasets list` 查看可用的数据集。

需要我现在启动一个单任务测试运行来验证整个流程是否正常吗？