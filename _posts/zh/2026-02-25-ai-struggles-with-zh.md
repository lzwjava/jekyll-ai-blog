---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI 挣扎于
translated: true
type: note
---

问题：在前端开发中，为什么用像 Claude 或 Codex 这样的 AI 模型通过视觉描述 UI 时，往往比后端开发中描述 API 和字段错误更难获得好结果？

回答：

你观察到在使用当前 LLMs（Claude、o1、Gemini、Grok、GPT-4o 等）进行 2025–2026 年编码时的真实且常见的局限性。

### 核心差异：Frontend 与 Backend 的“精度差距”

| Aspect                  | Backend (API, logic, validation)          | Frontend (UI/layout/styling/interaction)       | Why the difference matters for LLMs |
|-------------------------|--------------------------------------------|--------------------------------------------------|--------------------------------------|
| Specification language  | 主要为文本性和结构性的                    | 高度空间化 + 视觉化 + 隐式约定                  | LLMs 主要基于文本训练              |
| Exactness required      | 逻辑必须正确（通过/失败明确）              | Pixel-perfect + responsive + accessibility + feel | 小偏差就会破坏产品                  |
| Description mode used   | “field X 应为 number，最小 18，必须填写”   | “card 看起来现代、干净，带有微妙阴影”            | 视觉语言极度信息丢失                |
| Feedback loop           | 运行 → 查看 JSON / 错误消息                | 运行 → 查看渲染 → 调整 CSS                       | 视觉迭代更慢且主观                  |
| Common success rate     | 需求明确时成功率高                         | 仅用自然语言描述时中等–低                       | — |

### 视觉描述在前台失败的主要原因

1. **自然语言中的海量信息丢失**
   “一个美丽的居中登录表单，带有现代蓝色按钮”
   → 存在数百种有效实现（padding？font？border-radius？hover？mobile？contrast ratio？）

2. **缺乏共享视觉基础**
   模型从未“见过”你的屏幕。它仅从训练截图 + 代码中了解统计模式。

3. **CSS 高度上下文敏感**
   - `position: absolute` vs `flex` vs `grid` 会彻底改变一切
   - `gap` vs `margin` vs `padding` 与父元素交互不同
   - Tailwind vs CSS modules vs styled-components 会显著改变语法表面

4. **UI 审美极度主观**
   你认为的“clean/minimal/elegant”可能与 GitHub 代码中的主流完全不同 → 模型偏向平均水平

5. **聊天中缺乏迭代视觉反馈循环**
   Backend：“此字段返回 422 → 修复验证” → 1–2 轮
   Frontend：“在移动端未居中” → 需要多轮截图 + 描述

### 2025–2026 年在前台明显更有效的实用模式

- **最佳 → 最差顺序**（大致按成功率排序）

  1. 提供现有类似代码 + 说“让它看起来像这个但更改 X”
  2. 粘贴**非常详细**的 Figma 检查面板导出（spacing、颜色为 hex/hsl、font stack、weights、line-heights…）
  3. 以文本形式给出精确的**组件分解**
     示例：
     - outer: flex col, items-center, min-h-screen, bg-gray-50
     - card: w-full max-w-md, p-8, bg-white, rounded-2xl, shadow-xl
     - logo: mb-8, h-12, mx-auto
     - inputs: space-y-5 …

  4. 使用 Tailwind + 给出几乎逐行的 className 字符串
  5. 附加/引用**真实截图**（许多模型现在很好地接受图像）
  6. 纯自然语言视觉描述 ← **最差**，除非非常简单的组件

- 快速备忘单提示，通常能显著提升质量：

```
You are an expert React + Tailwind developer.
Generate **exact** JSX + className strings.
Do NOT use vague words like "nice", "modern", "beautiful".
Follow these exact design tokens and spacing rules:
- primary: #3b82f6
- radius: rounded-xl
- shadow: shadow-lg hover:shadow-xl
- input padding: py-3 px-4
- gap between form fields: space-y-4

Layout must use flex or grid — never position absolute unless explicitly needed.
Mobile-first approach. Make it responsive.

Task: centered login card containing: logo (h-10), email input, password input, submit button (bg-blue-600 hover:bg-blue-700), "forgot password" link.
```

### 总结

Backend 发挥了语言模型的优势（符号推理 + 严格契约）。
Frontend 暴露了它们的弱点（仅通过文本的空间推理 + 高审美变异）。

在模型对**纯描述的视觉推理**大幅改进之前（或每个人都常规附加 Figma/实际截图），最有效的方式是：

- 给出结构化文本规范（测量值、tokens、布局类型）
- 或给出视觉参考 + 小修改请求

这通常能缩小 70–80% 的质量差距，与“让它看起来 nice 和 modern”相比。

参考文献：

- 无（常见开发者经验观察，未使用特定外部来源）
