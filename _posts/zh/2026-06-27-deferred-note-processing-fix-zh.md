---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 延迟票据处理修复
translated: true
type: note
---

以下是发生的事情：

**问题：** Hermes 中的 `/note` 命令同步执行了完整流程——LLM 标题生成、文件创建、git commit + push。这个过程很慢（约 10-30 秒）且脆弱（pre-commit 钩子如 `end-of-file-fixer` 会修改文件，导致提交失败）。

**修复：** 更新了 `/Users/lzwjava/.hermes/plugins/note/__init__.py`——`/note` 插件现在仅将内容加入队列到 `~/.config/ww/note_queue.json`（即时完成，<1 秒）。与 `ww note` 模式相同。

**处理：** 延迟到 `ww note process` 执行，由 `ww note watch` 后台监视器自动清空。当前没有运行监视器或 cron ——队列将一直累积，直到你：

- 在终端中运行 `ww note watch`
- 添加系统 crontab 条目（`*/5 * * * * ww note process`）
- 手动运行 `ww note process`
