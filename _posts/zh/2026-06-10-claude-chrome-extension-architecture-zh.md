---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Chrome扩展架构
translated: true
type: note
---

**问题：** Claude 在 Chrome 中是如何内部工作的——它是否基于现有的“浏览器使用”技术（Playwright、browser-use、CDP）？

**回答：**

既是也不是。它与 browser-use/Playwright MCP 属于同一 *类别* 的技术——一个驱动浏览器的 LLM 工具调用循环——但它并非基于 Playwright 或 `browser-use` 库构建。它是一个原生的 Chrome 扩展，通过 `chrome.debugger` API 直接与 **Chrome DevTools 协议（CDP）** 通信，并注入内容脚本。没有外部驱动程序进程，没有独立的浏览器实例——它直接附加到 *你正在运行的* Chrome 配置文件上。

## 核心循环

这是标准的 Anthropic 代理循环。该扩展构建一个系统提示（服务器配置 + 平台 + 标签页上下文 + 领域技能），解析当前页面类型可用的工具，流式传输 claude-sonnet-4-5 响应，执行所有 tool_use 块，将结果反馈回去，并循环直到 Claude 返回一个没有工具调用的响应——然后从所有标签页分离 CDP 调试器。在执行过程中，它持续访问官方的 `/v1/messages` 端点——与你使用的 API 相同。大约 30 行代码，其结构如下：

```python
import anthropic

client = anthropic.Anthropic()
messages = [{"role": "user", "content": task}]

while True:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=10000,
        system=build_system_prompt(tab_context, domain_skills),
        tools=[read_page, find, computer, form_input, javascript_tool, ...],
        messages=messages,
    )
    tool_uses = [b for b in resp.content if b.type == "tool_use"]
    if not tool_uses:
        break  # 完成——分离调试器
    messages.append({"role": "assistant", "content": resp.content})
    messages.append({"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": t.id,
         "content": execute_in_browser(t.name, t.input)}  # ← CDP / 内容脚本
        for t in tool_uses
    ]})
```

唯一新颖的部分是 `execute_in_browser`——工具如何与页面进行交互。

## 感知：优先使用无障碍树，其次使用像素

该扩展使用两种模式来理解页面：页面的无障碍树，以及当无障碍树无法达成目标时的屏幕截图。无障碍树是浏览器为屏幕阅读器构建的结构——关于交互元素的语义信息：角色（按钮、链接、输入框）、名称、描述、状态。

具体来说，`read_page` 工具通过 `chrome.scripting.executeScript` 注入一个 `window.__generateAccessibilityTree(filter, depth, maxChars, refId)` 函数，该函数递归遍历 DOM（默认深度 15）并将元素映射到 ARIA 角色。它支持一个过滤器（'interactive' 仅限按钮/链接/输入框，或 'all'），一个用于将读取范围限定到子树的 `ref_id`，并将输出限制在 50,000 个字符以内。每个元素获得一个 `ref_N` 句柄，模型在后续的点击/输入调用中使用——这与 Playwright MCP 的 `browser_snapshot` 中基于 ref 的交互模式相同，但这是自实现的，而不是使用 Playwright 的 ariaSnapshot。

为什么优先使用无障碍树而不是屏幕截图？Token 消耗。文本结构的角色+名称将页面压缩约 10–50 倍（相对于视觉），并且 ref 是精确的（没有坐标回归）。缺点在逆向工程文章中有所说明：长页面的完整无障碍树会急剧膨胀上下文，而屏幕截图回退（每张 100–500 KB）会在多次交互中持续存在，使得长任务变得缓慢且昂贵。

## 动作：通过 chrome.debugger 使用 CDP

这是有趣的权限层。与依赖高级 DOM API 的标准扩展不同，该扩展利用了 `chrome.debugger` API，使其能够直接访问 Chrome DevTools 协议。通过 CDP，它可以合成“受信任”的用户事件（点击、按键），这些事件与人类硬件输入无法区分；读取网络请求、控制台日志以及原始的无障碍树；并向任何打开的页面注入任意 JavaScript。

“受信任事件”这一点很重要：从内容脚本执行的简单 `element.dispatchEvent(new MouseEvent('click'))` 会产生 `isTrusted: false` 的事件，许多网站（React 合成事件守卫、机器人检测、支付 iframe）会忽略这些事件。CDP 的 `Input.dispatchMouseEvent` / `Input.dispatchKeyEvent` 通过浏览器的输入管道，因此它们是 `isTrusted: true`——与 Playwright 和 Puppeteer 使用的技巧相同，只是从扩展内部访问，而不是通过外部 WebSocket 连接到 `--remote-debugging-port`。

一个实际后果：所有操作都依赖于调试器权限，当调试器附加时，浏览器会显示调试横幅，并且标签页会获得焦点——因此“后台操作”在实践中并不完全隐蔽。你已经看到黄色的“Claude 正在调试此浏览器”栏——那就是 `chrome.debugger.attach()`。

## 技术栈对比

| | Claude in Chrome | browser-use / Playwright MCP | OpenAI Operator 风格 |
|---|---|---|---|
| 浏览器 | **你的** Chrome 配置文件（扩展） | 由 Playwright 启动的独立浏览器 | 云虚拟机浏览器 |
| 传输方式 | `chrome.debugger` → 进程内 CDP | WebSocket → 通过 Playwright 访问 CDP | 视觉 + VNC 类 |
| 感知方式 | 自定义无障碍树遍历器（`ref_N`）+ 屏幕截图回退 | ariaSnapshot / DOM 提取 | 主要依赖屏幕截图 |
| 身份验证 | 免费——继承你已登录的会话 | 必须重放 cookies/登录 | 在虚拟机中重新登录 |
| Claude Code 桥接 | 原生消息主机（stdio JSON）→ 扩展 | 不适用 | 不适用 |

因此，对于“它是否使用了某种浏览器使用技术”这个问题的诚实回答是：它独立实现了每个浏览器代理都会趋同的三个基本原语——**(1)** 一个用于低成本感知的无障碍树/DOM 序列化，**(2)** 用于受信任输入 + 控制台/网络内省的 CDP，**(3)** 一个针对 `/v1/messages` 的工具调用循环——但以扩展的形式打包，以便它使用你真实的会话而不是沙盒浏览器。这种会话继承既是杀手级功能（无需身份验证管道），也是需要大量权限提示和提示注入防护措施的原因。

如果你想研究一个在微观层面工作的重实现循环，`browser-use` 仓库（Python，通过 Playwright 使用 CDP）就是该领域的 nanoGPT——阅读它的 DOM 序列化器，并与下面 gist 中的 `read_page` 模式进行比较；你会看到趋同的设计。

**参考文献：**

- [Claude for Chrome 扩展内部原理 (v1.0.56) — sshh12 gist](https://gist.github.com/sshh12/e352c053627ccbe1636781f73d6d715b)
- [生化人会话：逆向与检测 Claude AI 代理 Chrome 扩展 — CHEQ](https://cheq.ai/blog/the-cyborg-session-reversing-detecting-claude-ai-agent-chrome-extension/)
- [Claude in Chrome 的工作原理 — 逆向工程文章](https://medium.com/@buttercanbentley/how-claude-in-chrome-works-45b86b06f689)
- [将 Claude Code 与 Chrome 结合使用（测试版）— Claude Code 文档](https://code.claude.com/docs/en/chrome)
