---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 Claude Opus 制作动画视频
translated: true
type: note
---

问题：人们如何利用Claude Opus 5.5制作高质量视频，比如那些流行的动态图形剪辑？

答案：

**关键点：Opus 5.5 不直接输出视频。** 它读取文本和图像，返回文本，因此无法直接生成 MP4。它实际编写的是一个程序，而浏览器自动化库会逐帧将该程序转换为画面。模型会编写 HTML、CSS 和 JavaScript 动画库，或 React，再由渲染引擎捕获各帧。

**常见工作流程**

1. **使用编码代理（Claude Code 是常见选择）。** 人们会提供一个长而详细的指令，让它工作数小时。据报道，Claude Code 曾在一段备受推崇的音乐视频上自主工作十二小时，通过查看自身输出来修正错误。
2. **选择渲染路径。** HyperFrames 适合 HTML 和 GSAP 工作，Manim 适合数学和数据讲解，Blender（通过其官方 Claude 连接器）适合 3D，而 Remotion 适合已经会写 React 的人。独立测试发现，Opus 5.5 倾向于自行选择最简单的路径：一个 HTML 文件、一个 seek 函数，以及 Playwright 来捕获帧。
3. **如需可编辑项目，请安装 Remotion 插件。** Remotion 的官方 Claude Code 插件可帮助 Claude Code 创建和编辑 Remotion 项目。设置命令如下：
   ```
   claude plugin marketplace add remotion-dev/claude-code-plugin
   claude plugin install remotion@remotion
   ```
4. **要求一个可编辑项目并明确渲染步骤。** 好的提示会要求帧驱动动画和本地资源，例如一个 15 秒的产品发布视频，或一个基于 CSV 文件的 20 秒图表动画。然后导出，例如：`npx remotion render src/index.tsx Promo out/promo.mp4 --codec=h264 --pixel-format=yuv420p --muted`
5. **（可选）混入视频模型。** 某些项目会使用视频模型制作实景镜头和物理效果，然后让 Opus 5.5 在该参考基础上重绘每一帧，以获得一致风格。

**人们正在制作的示例：** 解释型动画（如 AI 发展史）、音乐视频动画、品牌或产品发布视频。一位创作者表示，Opus 5.5 使用 Remotion 制作了一个周边产品发布视频，拥有出色的转场、节奏和品牌呈现。

**现实核查：** “一个提示搞定”的说法具有误导性。Anthropic 的 Claude Code 团队人员开玩笑说，帖子称“Claude 一次性完成”，而实际提示包含 1 万个字符，内含技能、示例和 API 密钥。因此，请准备好编写详细的指令，提供资源，并进行迭代。

**轻松入门方式：** 从 Remotion 的一个 10–15 秒小项目开始，确认导出正常，再扩展到更长的作品。

参考资料：
- [Opus 5.5 通过编写绘制每帧的程序生成动态设计视频](https://pasqualepillitteri.it/news/19006/opus-5-5-motion-design-video)
- [Claude Opus 5.5 动态图形：最佳工具，免费与付费](https://capitalandcompute.net/blog/claude-motion-graphics-tools/)
- [使用 Opus 5.5 制作视频：提示与 MP4 导出](https://ofox.ai/blog/opus-5-5-video-prompts-mp4-guide/)
- [Claude Opus 5.5 正在生成令人惊叹的动态图形视频：10 个最佳示例](https://officechai.com/ai/claude-opus-5-5-motion-graphic-videos/)
- [BridgeMind Remotion 案例（Hermes 案例库）](https://hermes-ai.net/ai-models/claude-opus-5-5/case/2102462889160286423/)