---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes Agent中的浏览器工具
translated: true
type: note
---

我正在使用的浏览器工具内置在 Hermes Agent（您正在与之对话的 CLI AI 代理）中。其工作方式如下：

**Stack:**
- **Browserbase** — 底层的无头浏览器基础设施（云端托管的 Chromium 实例）。它具备隐身能力（不过在此场景下未使用住宅代理）。
- 这些工具以我可按顺序调用的函数形式暴露：

| Tool | What it does |
|------|-------------|
| `browser_navigate(url)` | 打开页面，初始化会话 |
| `browser_snapshot()` | 读取 DOM/无障碍树 — 返回元素引用（如 `@e1`、`@e2`） |
| `browser_click(ref)` | 通过引用点击元素 |
| `browser_type(ref, text)` | 通过引用在输入框中键入文本 |
| `browser_press(key)` | 键盘按键（Enter、Tab、Escape） |
| `browser_scroll(direction)` | 向上 / 向下滚动 |
| `browser_console(expression)` | 在页面上下文中执行 JS，读取结果 |
| `browser_vision(question)` | 截图 + 视觉分析（原生视觉或备用模型） |
| `browser_back()` | 后退导航 |

**Workflow for this login attempt:**
1. `browser_navigate` → 加载 `http://192.168.22.1`，获取带有引用 ID 的表单结构
2. `browser_type(@e1, "admin")` → 填写用户名
3. `browser_type(@e2, "admin")` → 填写密码
4. `browser_click(@e3)` → 点击“登录”按钮
5. 通过 `browser_snapshot()` 和 `browser_console()` 检查结果，读取 JS 状态
6. 经过 3 次失败的组合后，`browser_vision()` → 截图以读取中文错误消息

**Key detail:** `dosubmit()` JS 函数在 POST 之前对密码进行 Base64 编码，因此我也可以直接通过 `browser_console` 调用它，以编程方式操作表单，而不是点击。

它本质上是一个远程控制的 Chromium —— 可以类比为 Playwright/Puppeteer，但托管在云端，并通过 CLI 代理作为工具调用访问。