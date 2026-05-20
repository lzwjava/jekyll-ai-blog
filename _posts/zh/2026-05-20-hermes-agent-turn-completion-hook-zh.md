---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes 智能体回合完成钩子
translated: true
type: note
---

这是一个 **`post_llm_call` shell 钩子**，用于 Hermes Agent——每次 Agent 完成一轮（即工具调用循环结束且最终响应就绪后）时，它会触发一个 macOS 通知。

下面逐段解析：

---

**Shebang 与元数据**
```bash
#!/usr/bin/env bash
# ~/.hermes/agent-hooks/on-agent-done.sh
```
保存至 `~/.hermes/agent-hooks/`——这是 Hermes 监视生命周期钩子的目录。该钩子会在每次 LLM 调用完成后自动运行。

---

**读取负载**
```bash
payload="$(cat -)"
```

钩子系统通过 stdin 将 JSON 负载以管道方式传入脚本。负载包含当前上下文：`cwd`、`extra.user_message`、`extra.conversation_history` 等。

---

**通过内嵌 Python 提取数据**
```bash
extracted=$(echo "$payload" | python3 -c "...")
```

一段内联的 Python 脚本解析 JSON 并提取 3 项内容：

1. **目录名**——取 `cwd` 的 basename（例如，从 `/Users/lzwjava/projects/hermes-agent` 中提取 `hermes-agent`）
2. **用户消息的前 10 个字符**——以便了解最后一个提示的内容
3. **对话历史轮次计数**——当前所在的轮数

这些内容被打包成一个管道分隔的字符串，例如 `hermes-agent|what's the|3`。

---

**构造通知**
```bash
subtitle="msg: ${user_preview}  |  turns: ${hist_count}"
```

构建一个副标题，显示消息预览和对话深度。

---

**macOS 通知**
```bash
terminal-notifier \
  -title "Hermes Agent — ${dirname}" \
  -subtitle "${subtitle}" \
  -message "Hermes has completed one turn." \
  -sound Glass \
  -activate com.mitchellh.ghostty \
  -group com.hermes.notification \
  2>/dev/null || true
```

使用 [`terminal-notifier`](https://github.com/julienXX/terminal-notifier)（一个 macOS 通知 CLI 工具，可通过 `brew install terminal-notifier` 安装）来：

- 显示通知，例如：  
  **Hermes Agent — hermes-agent**  
  *msg: what's the  |  turns: 3*  
  Hermes has completed one turn.
- 播放 `Glass` 系统声音
- `-activate com.mitchellh.ghostty` 使得点击通知时将 **Ghostty**（你的终端模拟器）置于前台，而不是只打开通知中心
- `-group com.hermes.notification` 将所有 Hermes 通知归为一组（这样 macOS 会替换旧通知，而不是堆叠它们）

---

**钩子系统要求**
```bash
printf '{}\n'
```

钩子系统期望 stdout 上输出一个 JSON 对象（即使为空）作为确认。`{}` 表示“一切正常，继续”。如果没有这个输出，Hermes 可能会记录一条警告。

---

**为什么要用这个**：如果你在后台运行长时间任务，或者暂时离开让 Hermes 工作，这个提示音能让你知道 Agent 已完成一轮，可以接受下一个输入——无需一直盯着终端。