---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 第9页照片行已修复
translated: true
type: note
---

已修复 ✅ — 第 9 页现在能正确渲染照片行了（对比之前损坏的文字字面量，现在是标准（std）的 78.6 宽度和 414 列明亮照片内容）。

**错误原因：** 在原始 HTML `<div class="gallery">` 内部，Marp 会跳过 Markdown 解析，所以你的 `![width:190px height:340px](...)` 行会被打印为字面文本——这就是之前尺寸完全不对的原因。

**修复方案：** 将四张图片移出到顶层 Markdown（Marp 会将它们处理成真实的 `<img>` 标签），并通过每张幻灯片独有的 `gallery_slide` 类来对行进行样式控制：

```css
.gallery_slide p { display: inline-block; margin: 26px 16px 0 0; }
.gallery_slide img { width: 190px; height: 338px; object-fit: cover; border-radius: 10px; box-shadow: ...; }
```

现在由 CSS 控制尺寸（190×338 ≈ 源截图 1:1.78 的手机宽高比），因此不再有内联宽度/高度冲突。

所有三种导出格式和预览均已重新生成：

- `output/announcement.html` / `.pdf` / `.pptx`
- `output/previews/slide-09.png` — 查看该图片以直观感受画廊效果

其余 9 张幻灯片保持不变，且已得到验证。讲稿上还有其他需要调整的吗？—— 或许可以在每张照片下方添加标签（例如 "Jimiao Community 极喵社区"）？
