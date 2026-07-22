---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Pi Agent 笔记扩展已构建并推送
translated: true
type: note
---

以下是我们的完整工作摘要：

---

## 1. 探索项目（`/mnt/data/zz`）

一个机器学习数据管道，用于下载、提取、分词和分析大型数据集（FineWeb、Wikimedia 等），以进行模型训练。

## 2. 研究 Pi Agent 扩展 API

您分享了您的 Hermes `note` 插件（Python），我阅读了 Pi Agent 文档中关于扩展、会话格式以及示例（`bookmark.ts`、`summarize.ts`）的内容。

## 3. 构建了一个 Pi Agent note 扩展

编写了 `~/.pi/agent/extensions/note/index.ts` —— 一个 TypeScript 编写的 `/note` 命令，其功能包括：

- 从会话中捕获助手回复
- 去除推理标签
- 追加内容到 `~/.config/pi/note_queue.json`
- 支持 `N`（回复序号）和 `--title` 参数

## 4. 备份到 `~/projects/config/`

将扩展和 `settings.json` 复制到 `~/projects/config/pi/agent/`，以便在另一台机器上使用。

## 5. 提交并推送

```
cd ~/projects/config
git add pi/agent/
git commit -m "add pi agent note extension and settings"
git pull --rebase
git push
```

成功推送到 `github.com:lzwjava/config.git`。
