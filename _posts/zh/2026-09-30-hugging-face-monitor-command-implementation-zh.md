---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hugging Face 监控命令实现
translated: true
type: note
---

已完成。以下是已实施内容的摘要：

## 新命令：`ww monitor huggingface`

### 创建的文件
- **`ww/monitor/__init__.py`** — 包标记文件
- **`ww/monitor/huggingface.py`** — 监控模块

### 修改的文件
- **`ww/main.py`** — 在帮助文本中添加了 `monitor` 组、分发链和 `all_groups` 列表
- **`~/.zsh/completions/_ww`** — 在命令数组中添加了 `monitor`、`monitor_cmds` 数组、子命令分发以及 `--now`/`--hours` 标志补全

### 工作原理
1. **获取**来自 `https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=10` 的前 10 个热门模型
2. **比较**与存储在 `~/.ww/monitor/hf_trending.json` 的缓存快照
3. **发送 Telegram 提醒**当前 10 个模型发生变化时（列出新条目、移除的条目和位置变动）
4. **缓存**当前的前 10 个模型作为下次运行的基准

### 标志
- `--now` — 即使前 10 个模型未变化也强制发送提醒
- `--hours N` — 回溯 N 小时（用于 cron 定时任务）

### Telegram 配置
在 `.env` 文件中设置以下环境变量：
```
TELEGRAM_BOT_TOKEN=<你的机器人令牌>
TELEGRAM_CHAT_ID=<你的聊天 ID>
```
（同时支持 `TELEGRAM_HABIT_BOT_API_KEY` 作为备用。）

### Cron 定时任务（包含在模块注释中）
```cron
* * * * * cd /Users/lzwjava/projects/ww && uv run ww monitor huggingface >> /tmp/ww-monitor-hf.log 2>&1
```
每 10 分钟执行一次（可根据需要调整为 `*/10 * * * *`）。