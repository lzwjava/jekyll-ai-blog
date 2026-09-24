---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 具有HTML可视化输出的聊天机器人
translated: true
type: note
---

**是否存在一个聊天机器人，其默认输出是可视化HTML而不是Markdown/文本？**

**是的——Claude 是目前最接近的主流例子。**

Anthropic 的 [Claude](https://claude.ai/?utm_source=chatgpt.com) 现在拥有 **Custom Visuals**（自定义可视化）：Claude 可以直接在对话中生成交互式图表、图线和UI，使用 **HTML/SVG**，而不仅仅是返回 Markdown。你可以与它们进行交互，并将结果下载为 HTML/SVG。([Claude Help Center][1])

更重要的是，Claude 拥有 **Artifacts**（工件），它本质上是聊天旁边的一个持久的HTML/UI画布。它可以生成：

* 单页网站
* 仪表板
* 交互式工具
* HTML/CSS/JS
* SVG 图线
* React 组件

并可以通过对话进行迭代。([Claude Help Center][2])

### 但如果你指的是 **"总是以HTML回答"**

还有更多有趣的选择：

| 系统 | HTML优先 | 交互式 | 可自托管 |
| -------------------------------- | ---------: | ----------: | ------------: |
| **Claude + Artifacts** | ★★★★☆ | ✅ | ❌ |
| **Open WebUI + Artifacts** | ★★★★★ | ✅ | ✅ |
| **LibreChat + Artifacts** | ★★★★★ | ✅ | ✅ |
| **你自己的 LLM + HTML 渲染器** | ★★★★★ | ✅ | ✅ |

Open WebUI 的工件系统明确地在聊天旁边渲染 **HTML/CSS/JS、SVG、Three.js 和 D3**。([Open WebUI][3]) LibreChat 类似地支持智能体生成 React、HTML、SVG 和 Mermaid 工件。([LibreChat][4])

对于我猜测你实际在寻找的东西，我会大致构建一个这样的协议：

```text
user
  │
  ▼
LLM
  │
  ├── answer intent
  │
  └── visual intent
         │
         ▼
   HTML artifact
         │
         ▼
┌──────────────────────┐
│  chat                │
│                      │
│  "Here is the result"│
│                      │
│  ┌────────────────┐  │
│  │  rendered HTML │  │
│  │                │  │
│  │   ┌─────┐      │  │
│  │   │chart│      │  │
│  │   └─────┘      │  │
│  │                │  │
│  └────────────────┘  │
└──────────────────────┘
```

而模型约定可以非常简单直接：

```xml
<artifact type="html">
<!doctype html>
<html>
...
</html>
</artifact>
```

然后你的聊天UI检测到 `<artifact type="html">` 并将其放入沙盒化的iframe/画布中。

甚至有针对 Claude Code 的技能专门设计来让模型 **在空间布局、图表、颜色或交互性有用的情况下优先选择 HTML 而非 Markdown**。([GitHub][5])

所以 **是的，这个产品类别是存在的**，但在以下两者之间仍有差距：

> "大语言模型可以制作HTML工件"

和

> **"每个回答都是一个可视化、可探索的HTML文档。"**

第二点作为聊天机器人用户体验的基本元素来说，有趣得令人惊讶。

我还可以描绘一个 **最小的约200行的HTML优先聊天机器人架构**，使用兼容OpenAI的模型 + iframe沙盒，如果你想要的是这个的话。

[1]: https://support.claude.com/en/articles/13979539-custom-visuals-in-chat-and-cowork?utm_source=chatgpt.com "聊天与Cowork中的自定义可视化 | Claude Help Center"
[2]: https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them?utm_source=chatgpt.com "什么是工件以及如何使用它们？ | Claude Help Center"
[3]: https://docs.openwebui.com/features/chat-conversations/chat-features/code-execution/artifacts/?utm_source=chatgpt.com "工件 / Open WebUI"
[4]: https://www.librechat.ai/docs/features/artifacts?utm_source=chatgpt.com "工件 - 生成式UI | LibreChat"
[5]: https://github.com/dogum/html-artifacts?utm_source=chatgpt.com "GitHub - dogum/html-artifacts：一个Claude技能，用于在任务需要时生成自包含的HTML工件而非markdown。 · GitHub"
