---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中文文本渲染修复
translated: true
type: note
---

## ✅ 中文文本渲染已修复

### 根本原因

远程服务器上**完全没有中文字体**（仅有 DejaVu）。`video.py` 的中文字体加载器会查找 `NotoSansCJK-Black.ttc` / `NotoSerifCJK-Bold.ttc` / `wqy-zenhei.ttc` —— 这些文件都不存在，因此静默回退到了 **PIL 的默认位图字体**，该字体没有 CJK 字形 → 中文标题/字幕显示为 **豆腐块（□□□）**。

### 已应用的修复

1. **在远程服务器上安装了 `fonts-noto-cjk`** → 提供 `NotoSansCJK-Regular.ttc`、`NotoSansCJK-Bold.ttc`、`NotoSerifCJK-*.ttc`
2. **修改了 `video.py`**（提交 `f7f5d68`）：
   - 将 `NotoSansCJK-Bold.ttc`（SC 字体）添加到标题候选列表中——Ubuntu 24.04 的包提供的是 **Bold 而非 Black**，而 Black 原本是第一个标题候选字体
   - `_load_font(..., cjk=True)` 现在有一个 **fontconfig `fc-match ':lang=zh-cn'` 的最后回退机制**，因此即使字体路径发生变化，中文文本也不会再静默降级为豆腐块
3. **重新部署并重启了服务器**（健康检查返回 200，隧道仍然存活）

### 在远程服务器上已验证

| 检查项 | 结果 |
| --- | --- |
| 字体加载 | `Noto Sans CJK SC` Bold（标题）+ Regular（字幕）✓ |
| 完整幻灯片渲染 | `_create_slide_frame("AI 短视频创作工坊", "用人工智能…")` → 1080×1920 PNG ✓ |
| fc-match 回退 | 运行中的代码已包含 ✓ |
| 公网 URL | `https://rc-63980f23582dde21.radeon.firstdg.ai/health` → 200 ✓ |

### 关于图像内中文需要了解的一点

FLUX（像大多数扩散模型一样）在**生成的场景图像内部**渲染中文文本效果不佳——如果图像提示要求中文文字，你会得到乱码的伪字符。这是模型本身的局限性，不是代码的 bug。对于该管线的最佳实践：让场景**图像提示使用英文**，让 LLM 故事板进行翻译；仅在**标题/字幕叠加层**中使用中文——现在使用 Noto Sans CJK SC 可以正确渲染。

是否还需要我在 `gen-video` 中添加自动翻译步骤（LLM 将中文场景提示翻译成英文，然后再进行图像生成）？这样中文提示就能端到端地生成干净的视频。
