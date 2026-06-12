---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ww 对话命令参考
translated: true
type: note
---

```
ww conversation --help
```

```
用法：ww conversation <command> [options]

命令：
  json <name>       从 stdin/剪贴板捕获对话 JSON
  generate          从对话 JSON 生成音频（Google Cloud TTS）
  notes             将对话 JSON 文件转换为 markdown 笔记

选项：
  --output-dir DIR  音频/JSON 文件的输出目录
  --input-dir DIR   对话 JSON 文件的输入目录
  --type en|cn      语音的语言类型（默认：en）
  --dry-run         跳过音频生成
  --file FILE       处理指定的 JSON 文件
  --seed N          语音选择的随机种子
```

典型用法：

```
# 从单个对话生成音频（英文，默认）
ww conversation generate --file computer-networks-plus.json \
  --input-dir ~/projects/jekyll-ai-blog/scripts/conversation

# 生成中文语音音频
ww conversation generate --file my-topic.json \
  --input-dir ~/projects/jekyll-ai-blog/scripts/conversation \
  --type cn

# 试运行 — 验证而不调用 TTS API
ww conversation generate --file my-topic.json \
  --input-dir ~/projects/jekyll-ai-blog/scripts/conversation \
  --dry-run

# 生成目录中所有对话的音频
ww conversation generate \
  --input-dir ~/projects/jekyll-ai-blog/scripts/conversation

# 自定义输出目录
ww conversation generate --file my-topic.json \
  --input-dir ~/projects/jekyll-ai-blog/scripts/conversation \
  --output-dir ~/Desktop/audio

# 以交互方式捕获新的对话 JSON
ww conversation json my-new-topic

# 将对话 JSON 转换为 markdown 笔记
ww conversation notes \
  --input-dir ~/projects/jekyll-ai-blog/scripts/conversation
```

默认值：
- `--input-dir` → `scripts/conversation`（相对于当前工作目录）
- `--output-dir` → `~/projects/blog-assets/conversations`
```