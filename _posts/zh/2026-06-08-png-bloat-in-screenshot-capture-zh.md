---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 截图捕获中的PNG膨胀
translated: true
type: note
---

以下是发现的内容：

`ww screenshot interact-note` **并未**使用JPG格式。它全程采用PNG格式且未做任何优化：

1. `capture_screenshot()` 保存为 `screenshot-{ts}.png`（位于 `ww/image/screenshot.py` 第18行）
2. `_encode_image_to_base64()` 读取原始文件字节并进行base64编码——不调整尺寸、不转换格式、不压缩（位于 `ww/note/screenshot_log.py` 第20-22行）
3. MIME类型根据扩展名设置，但由于始终是 `.png`，因此始终为 `image/png`

因此，全分辨率PNG被直接发送到视觉API。在Retina显示屏上，其像素密度通常是LLM视觉所需像素密度的2-3倍，而base64载荷因PNG对渐变/抗锯齿文本的无损编码而变得臃肿。

根据你的分析，这里存在明显的优化空间：转换为质量50-70的JPG格式，并在发送给视觉模型前可选地调整尺寸。需要我添加这个功能吗？