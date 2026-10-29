---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 氛围知识动画制作
translated: true
type: note
---

**问题：** 微信视频号上的"vibe 知识鉴赏"动画视频是如何制作的？

**回答：**

这是一类融合了 **lofi/舒适动画视觉** 与信息内容的审美型知识科普短视频。以下是它们通常的制作流程：

---

## 🎨 风格特点

- **Lofi 动漫美学** — 温暖的灯光、舒适的房间、窗上的雨滴、柔和的色调
- **知识叠加层** — 通过动画文字或旁白讲解艺术史、科学、文化等内容
- **氛围/lofi 背景音乐** — 不引人注意的、适合学习氛围的曲目
- 通常使用 **循环或缓慢平移的视觉效果** 来持续吸引注意力

---

## 🛠️ 常见制作流程

### 第一步 — 生成基础画面（AI 图像工具）
- **Midjourney / 即梦AI (Seedance 2.5) / 可灵AI (Kling)** — 生成舒适/美学风格的场景图像
- 常见工作流：使用 Midjourney 的 `/describe` 从参考图中提取提示词关键词，然后通过 `/imagine` 生成同风格的原创插画

### 第二步 — 让画面动起来（AI 视频 / 动态工具）
类似 Morphic 的工具可以让你直接描述一个 lofi 动漫场景（例如："一个女孩在雨窗前温暖灯光下学习"），并在浏览器中直接生成循环动画片段 — 无需 After Effects

对于更结构化的 **知识类动画**（图表、概念流程、数学），开源工具 **Manim**（因 3Blue1Brown 而闻名）被广泛使用：
- Manim 被称为"与 3Blue1Brown 相同的引擎" — 它能将文字描述转化为精确的数学/知识动画；如果你的视频涉及概念推导、物理模拟或编程可视化，Manim 的精确性无可替代
- 一种流行的"vibe coding"方式：使用 AI（如 Gemini 或 Claude）结合 Manim，仅凭文本提示词即可生成动画教学/绘图视频 — 整个制作过程就是把提示词交给模型

### 第三步 — 剪辑与包装（剪映 / CapCut）
生成 AI 图像后，将其导入剪映 (CapCut)，添加光晕、烟雾或飘动的树叶/元素等动画效果来丰富场景，然后叠加 lofi 音乐轨道并导出

对于进阶创作者：更高质量的工作流使用 Midjourney → Photoshop GenFill（用于扩展/合成）→ Magnific AI（超分辨率放大）→ After Effects（分层动画）— 这种方式制作单个作品需要一位创作者约 18 小时

### 第四步 — 添加知识内容
- 文字叠加层 / 字幕，包含关键知识点
- AI 配音（科大讯飞、ElevenLabs、即梦数字人）
- 旁白与画面节奏同步

---

## ⚡ 快速工具地图

| 目标 | 工具 |
|---|---|
| 生成舒适场景艺术图 | 即梦AI / 可灵AI / Midjourney |
| 让静态图像动起来 | Morphic / Runway / Pika / Vidu |
| 知识概念动画 | **Manim**（AI 生成脚本） |
| 最终剪辑与特效 | **剪映 (CapCut)** |
| Lofi 音乐 | Soundful / YouTube Audio Library |
| 配音 | 科大讯飞 / ElevenLabs |

---

**总结：** 大多数创作者将 **AI 图像生成 → AI 视频动画 → 剪映剪辑** 结合起来。"vibe" 美学来自 lofi 场景提示词；"知识鉴赏" 层则来自文字/旁白或叠加在画面上的 Manim 风格概念动画。

---

**参考资料：**
- [如何用 AI 制作 lofi anime 视频 — Morphic](https://morphic.com/zh/resources/videos/lofi-anime-videos)
- [在小红书用 AI 做动态 Lofi 音乐号完整教程 — 知乎](https://zhuanlan.zhihu.com/p/686529764)
- [2026年开源 AI 视频工具全景拆解 — 知乎](https://zhuanlan.zhihu.com/p/2058330553322058463)
- [用 AI 制作 Lofi 治愈视频 — 知乎](https://zhuanlan.zhihu.com/p/690904102)
- [Manim + Vibe Coding 动画制作 — Learn By Doing with Steven](https://learnbydoingwithsteven.bearblog.dev/shocking-results-from-manim-and-antigravity/)