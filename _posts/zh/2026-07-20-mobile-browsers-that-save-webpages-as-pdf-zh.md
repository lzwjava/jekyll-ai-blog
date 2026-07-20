---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 移动浏览器保存网页为PDF
translated: true
type: note
---

**问题：哪些移动浏览器可以将网页转换为 PDF？**

多款移动浏览器支持直接或通过系统打印功能**“将网页保存为PDF”**：

| 浏览器            | 平台            | 网页→PDF支持 | 方式                                    |
| ----------------- | --------------- | ------------ | --------------------------------------- |
| Google Chrome     | Android / iOS   | ✅ 支持       | 分享/菜单 → 打印 → 保存为PDF             |
| Microsoft Edge    | Android / iOS   | ✅ 支持       | 分享 → 打印 → 保存为PDF                  |
| Safari            | iPhone/iPad     | ✅ 极佳       | 分享 → 选项 → PDF → 存储到“文件”         |
| Firefox           | Android / iOS   | ⚠️ 有限       | 通常通过打印/分享系统                     |
| Brave             | Android / iOS   | ✅ 支持       | 分享 → 打印 → 保存PDF                    |
| Samsung Internet  | Android         | ✅ 支持       | 菜单 → 打印 → 保存PDF                    |

我的推荐：

1. **iPhone/iPad → Safari**
   * 集成度最高。
   * 原生生成PDF。
   * 保留阅读模式排版。

2. **Android → Chrome 或 Edge**
   * 使用Android系统打印管道。
   * 生成干净的PDF。

3. **技术文章/文档 → Edge**
   * Edge 凭借 Chromium 与 PDF 的集成，通常能更好地处理长页面。

对于开发者，另一个强大的选择是：

```bash
# Desktop/headless Chrome
chrome --headless \
  --print-to-pdf=page.pdf \
  https://example.com
```

或：

```bash
npx playwright pdf https://example.com output.pdf
```

这对于归档文档、博客文章、研究论文等能提供更高的质量。
