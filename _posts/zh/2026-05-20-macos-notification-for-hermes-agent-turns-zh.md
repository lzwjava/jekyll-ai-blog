---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes Agent轮次的macOS通知
translated: true
type: note
---

这是一个用于 Hermes Agent 的 **LLM 调用后钩子脚本**——每当代理完成一轮（工具调用循环结束）时，它就会触发一个 macOS 通知。

具体步骤如下：

1. **从标准输入读取 JSON 载荷**——Hermes 通过 `post_llm_call` 钩子传递结构化数据，其中包含 `cwd`（当前工作目录）、`user_message` 和 `conversation_history` 数量。

2. **提取三个字段：**
   - **工作目录的基本名称**（例如 `hermes-agent`、`jekyll-ai-blog`）
   - **用户消息的前 10 个字符**（以便了解该轮的内容）
   - **截至目前对话的轮数**

3. **通过 `terminal-notifier` 触发 macOS 通知：**
   - 标题：`Hermes Agent — <项目目录>`
   - 副标题：`msg: <预览>  |  turns: <N>`
   - 正文：“Hermes 已完成一轮。”
   - 播放 `Glass` 音效
   - 点击后会将 Ghostty（你的终端）带到前台
   - 使用 `-group` 标志，使通知堆叠/替换，避免刷屏

4. **以 `printf '{}\n'` 结尾**——这是钩子系统期望的 JSON 响应（静默无操作，表示“一切正常，无需阻塞”）。

因此，每次我完成对你的回复后，会弹出一条通知，内容大致如下：

> **Hermes Agent — hermes-agent**
> msg: what's this  |  turns: 3
> Hermes 已完成一轮。

这纯粹是一个个人生产力/提醒功能——让你无需盯着终端就能知道代理已完成任务。代码写得干净利落。需要我对其进行自定义或禁用它吗？
