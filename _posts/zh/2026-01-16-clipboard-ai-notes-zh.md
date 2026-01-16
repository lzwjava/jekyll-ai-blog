---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 从剪贴板自动创建 AI 笔记
translated: true
type: note
---

**Question:** 但是在使用 AI chatbots 时，我仍然需要点击浏览器里的复制按钮。有没有办法避开这个额外的手动步骤？

**Answer:**

是的 —— 在使用 AI chatbots (Grok, Claude, ChatGPT, Gemini, Perplexity 等) 时，你几乎可以完全消除手动的 “点击复制” 步骤。以下是 2026 年最实用的方法，按从易到难、从手动到自动的顺序排列：

### 1. 对大多数人来说最好且最简单的方法 (2025–2026 现状)

使用一个**专用的 clipboard monitoring + hotkey tool**，它会监视新的 AI 生成文本，并将其直接发送到你的 note-creation 脚本。

**macOS – Raycast + Clipboard History + Custom Script Command** (强烈推荐)

- Raycast 已经拥有出色的 clipboard history 功能。
- 创建一个 Raycast Script Command (或使用现有的 "Quicklinks / Script" 工作流)。
- 脚本示例 (`new-grok-note-from-clipboard`):

```bash
#!/bin/bash
cd ~/projects/blog-source   # ← 你的 repo 路径
# 获取最新的剪贴板内容 (Raycast 传递 {clipboard} 或使用 pbpaste)
text=$(pbpaste)

# 可选：仅当看起来像 AI 输出时才继续 (启发式判断)
if [[ "$text" == *"Answer:"* || "$text" == *"# "* || ${#text} -gt 300 ]]; then
    echo "$text" | python3 scripts/create/create_note_from_clipboard.py grok-fast
    echo "Note created from clipboard"
else
    echo "Clipboard doesn't look like AI output – skipped"
fi
```

- 在 Raycast 中分配全局热键 → 例如 `⌃⌥ N`
- 工作流：AI 给出回答后 → **按下你的热键** → 笔记立即创建 (无需点击复制)

许多 Raycast 用户正是这样进行 Obsidian / blog / Notion daily note 创建的。

**Windows – PowerToys + AutoHotkey**

AutoHotkey v2 脚本示例 (保存为 `.ahk`，启动时运行):

```autohotkey
^!n:: {                               ; Ctrl+Alt+N
    text := A_Clipboard               ; 获取当前剪贴板
    if (StrLen(text) < 200) {
        MsgBox "Clipboard too short – nothing sent"
        return
    }
    Run 'cmd.exe /c cd /d "C:\path\to\blog-source" && python scripts\create\create_note_from_clipboard.py grok-fast', , 'Hide'
    ; 或者使用 ComObjCreate("WScript.Shell").Run(...) 以实现更干净的执行
    ToolTip "Note created from clipboard", 100, 100
    SetTimer () => ToolTip(), -1500
}
```

→ AI 回答出现后 → **全选 + 复制** (或让 AI 自动复制，如果可能) → 按下热键 → 完成

### 2. “零复制” 的更优选择 (完全无需手动复制)

| Method                              | Requires manual copy? | Platform        | Effort | Auto-selects AI answer? | Notes |
|-------------------------------------|------------------------|-----------------|--------|---------------------------|-------|
| Browser extension + localhost server| No                     | All             | High   | Yes (with DOM parsing)    | 自动化程度最高 – 见下文 |
| Raycast AI / Extension integrations | No                     | macOS           | Medium | Yes                       | Raycast 可以直接与 Grok/Claude API 通信 |
| Obsidian Web Clipper + Templater    | Sometimes              | All (Obsidian)  | Medium | Partial                   | 如果你使用 Obsidian 而不是 Git repo |
| Custom userscript (Tampermonkey)    | No                     | All             | High   | Yes                       | 注入 "Send to my blog" 按钮 |
| Claude / ChatGPT custom action      | No                     | Web             | Low    | Yes (if they support)     | Claude Projects + Tools 可以 POST 到 localhost |

**2026 年最自动且现实的选择** → 微型 FastAPI/Flask server + browser userscript/extension

快速设置大纲：

1. 运行一个小服务器 (一个终端窗口 / launch agent):

```python
# local_note_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.post("/create-note")
async def create_note(payload: dict):
    content = payload.get("content", "")
    model = payload.get("model", "grok-fast")
    if not content:
        return {"error": "No content"}
    p = subprocess.run(
        ["python", "scripts/create/create_note_from_clipboard.py", model],
        input=content.encode(),
        cwd="/Users/lzwjava/projects/blog-source",
        capture_output=True
    )
    return {"status": "ok", "output": p.stdout.decode()}
```

2. 添加浮动按钮或热键的 Userscript (Tampermonkey / Violentmonkey):

```javascript
// ==UserScript==
// @name         AI → Blog Note
// @match        https://chat.openai.com/*
// @match        https://claude.ai/*
// @match        https://grok.x.ai/*
// ==/UserScript==

document.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 'Enter') {   // Ctrl+Enter
        let text = window.getSelection().toString();
        if (!text) {
            // fallback: 尝试寻找最后一条助理消息
            let msg = document.querySelector('[data-message-author-role="assistant"]');
            text = msg?.innerText || '';
        }
        if (text.length > 200) {
            fetch('http://localhost:8000/create-note', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({content: text, model: 'grok-fast'})
            }).then(r => r.json()).then(console.log);
        }
    }
});
```

→ AI 回答后 → 选择文本 (或不选) → **Ctrl+Enter** → 笔记创建成功

这是目前许多 power users 用来完全跳过复制粘贴模式的做法。

选择与你的 OS 匹配且你愿意花精力搭建这一小块基础设施的方式即可。

如果你告诉我你主要使用的浏览器 + OS + 你最常使用的 AI chat，我可以提供更精确的步骤甚至开箱即用的代码。

References:

- None required for this answer