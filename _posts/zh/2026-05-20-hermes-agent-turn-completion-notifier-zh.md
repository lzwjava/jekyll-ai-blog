---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes 代理回合完成通知器
translated: true
type: note
---

问题：你能解释一下这个 Bash 脚本的作用吗？

答案：

这个脚本是 macOS 上 Hermes 代理的 **后处理钩子**。它用于在 Hermes 完成一次对话回合时通知用户。我们逐步分析：

---

### 1. **脚本元数据**

```bash
#!/usr/bin/env bash
# ~/.hermes/agent-hooks/on-agent-done.sh
```

* Shebang（`#!/usr/bin/env bash`）确保脚本使用 Bash 运行。
* 脚本位于 `~/.hermes/agent-hooks/` 中，当 Hermes 完成一个回合时触发。

---

### 2. **Bash 安全选项**

```bash
set -euo pipefail
```

* `-e` → 如果任何命令失败则退出。
* `-u` → 将未设置变量视为错误。
* `-o pipefail` → 使脚本在管道任何部分失败时出错。

这让脚本更健壮，避免静默错误。

---

### 3. **读取负载**

```bash
payload="$(cat -)"
```

* 从 `stdin` 读取 JSON 输入。Hermes 通过 JSON 将回合信息传递给钩子。

---

### 4. **使用 Python 提取数据**

```bash
extracted=$(echo "$payload" | python3 -c "
import json, sys
data = json.load(sys.stdin)

# 当前工作目录名称
cwd = data.get('cwd', '')
import os
dirname = os.path.basename(cwd) if cwd else 'unknown'

# 用户消息的前 10 个字符
extra = data.get('extra', {})
user_msg = extra.get('user_message', '')[:10]

# 对话历史条目数
history = extra.get('conversation_history', [])
hist_count = len(history)

print(f'{dirname}|{user_msg}|{hist_count}')
" 2>/dev/null) || extracted="unknown||0"
```

* 使用 Python 安全地解析 JSON。
* 提取三条关键信息：

  1. `dirname` → 当前工作目录名称（如果有）。
  2. `user_msg` → 用户最后一条消息的前 10 个字符。
  3. `hist_count` → 到目前为止的对话回合数。
* 输出以 `|` 分隔的字符串，供 Bash 解析。
* 如果失败，默认为 `"unknown||0"`。

---

### 5. **分割提取的值**

```bash
IFS='|' read -r dirname user_preview hist_count <<< "$extracted"
```

* 使用 `IFS='|'` 将字符串分割为三个变量：

  * `dirname` → 文件夹名称
  * `user_preview` → 用户消息片段
  * `hist_count` → 对话回合数

---

### 6. **构建通知副标题**

```bash
subtitle="msg: ${user_preview}  |  turns: ${hist_count}"
```

* 将提取的信息组合成小字符串，用于 macOS 通知。

---

### 7. **发送 macOS 通知**

```bash
osascript -e "
display notification \"Hermes has completed one turn.\" with title \"Hermes Agent — ${dirname}\" subtitle \"${subtitle}\" sound name \"Glass\"
" >/dev/null 2>&1 || true
```

* 使用 `osascript`（通过 shell 调用 AppleScript）显示通知：

  * **标题：** `"Hermes Agent — <directory>"`
  * **副标题：** `"msg: <前10个字符> | turns: <计数>"`
  * **声音：** `"Glass"`
* 将所有输出重定向到 `/dev/null` 以保持静默。
* `|| true` 确保即使通知被阻止，脚本也不会失败。

---

### 8. **返回空 JSON**

```bash
printf '{}\n'
```

* 输出 `{}`，以便 Hermes 的钩子系统知道脚本成功完成。
* 作为“静默无操作”响应。

---

### ✅ **总结**

* 该钩子在每个 Hermes 代理回合后触发。
* 提取基本上下文：目录、用户消息预览和对话长度。
* 发送 **非侵入式的 macOS 通知**。
* 如果出现问题，会优雅地失败。

这是一个 **在 macOS 上直观跟踪 Hermes 活动的简单而有效的方法**。

---

如果你愿意，我还可以 **绘制一个小的流程图，展示 JSON 如何从 Hermes → 该脚本 → macOS 通知**，这将使流程更易于理解。

需要我这样做吗？
