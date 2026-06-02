---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自动化HTML转图像管道
translated: true
type: note
---

以下是完整的流程：

1. **读取源文件** — 从 `timesheet/june-zh.md` 开始，这是中文考勤要求的 Markdown 文件。

2. **构建带样式的 HTML** — 创建一个自包含的 HTML 文件，包含：
   - Google Fonts（Noto Sans SC）用于中文渲染
   - 内联 CSS，采用卡片式布局（浅灰背景上的白色卡片）
   - 统计卡片、日历网格（CSS Grid）、表格、进度条、颜色编码区域
   - 所有样式均为内联（无外部依赖），确保独立渲染

3. **在无头浏览器中渲染** — 使用 `browser_navigate` 在 Browserbase 托管的 Chromium 实例中加载本地 HTML 文件。页面像真实浏览器一样渲染——字体、网格布局、表情符号、渐变均可正常显示。

4. **获取内容尺寸** — 通过 JS 控制台运行 `document.body.scrollWidth/scrollHeight`，获取内容的精确像素尺寸（例如，完整版为 720×3008）。

5. **截图** — 使用 `browser_vision` 捕获整页截图。问题：浏览器视口宽度为 1280px，但内容仅 720px，右侧会留下约 560px 的空白。

6. **裁剪至内容区域** — 使用 ImageMagick 的 `convert -crop 720x3008+0+0 +repage` 将图片精确裁剪到内容边界，去除所有空白区域。

7. **转换为 JPG** — 使用 `sips -s format jpeg -s formatOptions 95`（macOS 原生）或 ImageMagick 将 PNG 转换为 JPG，质量设为 95%。

8. **验证** — 对最终图片运行 `vision_analyze`，确认布局、可读性以及无裁剪问题。

关键技巧：浏览器截图总是捕获整个视口（默认宽度为 1280px），而不仅仅是内容。因此，你需要：
- 将视口调整为内容宽度，或者
- 事后使用 ImageMagick 裁剪

我选择了裁剪，因为它更可靠——HTML 正文宽度设置为固定像素值（680/720），卡片填充该宽度，因此裁剪到 `body.scrollWidth` 是精确的。

使用的工具：
  HTML/CSS  → write_file
  浏览器    → browser_navigate + browser_vision（Chromium 渲染 + 截图）
  JS        → browser_console（测量内容尺寸）
  裁剪      → ImageMagick convert（精确边界框）
  转换      → sips 或 ImageMagick（PNG → JPG）
  验证      → vision_analyze（输出质量检查）
