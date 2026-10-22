---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 已添加双语和主题切换
translated: true
type: note
---

完成。两个功能都已上线，位于单个 `index.html` 文件中（86.5 KB，仍然无需构建步骤）。

## 新增内容

**🌐 英文 / 中文切换**（顶部导航中的胶囊开关）
- 完整、手工翻译的每个部分的中文版——精选内容、数据统计、重点领域、实验、整个实验室笔记本（训练表格、状态、GPU 构建）、服务、关于时间线、联系、页脚、导航
- 即时就地切换（无需重新加载），动画锚点导航可跳转到 *当前* 语言块中的对应部分
- 语言选择保存在 `localStorage` 中；自动检测 `zh` 浏览器；预绘制脚本防止任何闪烁；`<html lang>` 以及页面标题/元描述正确切换
- 品牌/项目名称（vLLM、nanoGPT、SEC-EDGAR-GPT…）有意保留为英文

**☀/☾ 深色 / 浅色模式切换**
- 通过 CSS 变量实现的浅色主题——暖纸背景、深墨文字、调整琥珀色强调以增强对比度
- 保存在 `localStorage` 中；默认遵循 `prefers-color-scheme`；预绘制脚本防止白屏闪烁；`theme-color` 元标签和页头模糊效果自适应

## 已验证

- HTML 有效：没有未闭合/不匹配的标签，没有重复的 ID
- 两个脚本均通过 `node --check`
- 使用 DOM 存根在 Node 中模拟了完整控制流：
  - 英文→中文→英文切换，`lang="zh-CN"`、标题、已存储的偏好
  - 主题浅色↔深色切换，包含 `theme-color` 元标签更新
  - 使用已存储的偏好重新加载时恢复 `zh` + `light`
  - 锚点滚动根据当前语言块解析
- 全部 7 个部分均以两种语言呈现

预览方式：
```bash
cd /Users/lzwjava/projects/truth-labs && python3 -m http.server 8080
```

有一点值得快速浏览：我亲自翻译了所有内容，所以请对中文文案的语气进行一次检查——尤其是宣言引文和标语翻译。