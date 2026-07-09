---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 跨平台截图模块修复
translated: true
type: note
---

修复完成。不再需要 `--linux` 参数——平台会自动检测。

**`ww/image/screenshot.py` 中的变更内容：**

1. **延迟导入 Quartz** — 将 `import Quartz` 移入 `sys.platform == "darwin"` 分支内，而不是模块顶层。此前崩溃的原因是：Python 在加载模块时会尝试导入所有顶层名称，而 `Quartz`（pyobjc）在 Linux 上并不存在。

2. **`capture_screenshot()` 现在可在 Linux 上运行** — 回退到 `_capture_linux()`，该函数会依次尝试 scrot → ImageMagick `import` → gnome-screenshot → spectacle → ffmpeg x11grab。工具搜索顺序与 `screenshot_linux.py` 一致。

3. **`main()` 的描述已更新** — 现在显示“macOS / Linux”，而非仅“macOS”。

**结果：**
- `ww screenshot interact-note` → 导入 `capture_screenshot` 不再崩溃
- `ww screenshot`（无子命令）→ 现在也能在 Linux 上运行
- `ww screenshot-linux`（带有 `--no-save`/`--area` 的独立命令）保持不变——它具有额外的剪贴板/象限功能

测试表明截图捕获功能正常工作（ImageMagick `import` 通过 DISPLAY=:1 运行），LLM 步骤仅因该云环境未设置 `OPENROOTER_API_KEY` 而失败——并非代码问题。

需要我将这种跨平台模式保存为技能吗？