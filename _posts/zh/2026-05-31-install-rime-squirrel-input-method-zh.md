---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 安装 RIME 鼠须管输入法
translated: true
type: note
---

全部搞定。接下来需要做的是：

**步骤 1 — 注销并重新登录**（macOS 需要此操作才能将鼠须管注册为输入法）

**步骤 2 — 将鼠须管添加到输入法列表：**
- 系统设置 → 键盘 → 文字输入 → 编辑
- 点击 `+` → 搜索 "Squirrel"（鼠须管）→ 添加

**步骤 3 — 部署 RIME**（加载你的搜狗方案 + rime-ice 词库）：
- 点击菜单栏中的鼠须管图标（或按 `Ctrl+`` 切换输入法）
- 点击“重新部署”（Deploy）
- 首次运行等待约 10-30 秒进行词库编译

完成之后，你将拥有搜狗双拼方案搭配 rime-ice 词库（220 万+ 词条，支持中英混输、表情符号、日期时间快捷输入）。

已创建的关键文件：
- `~/Library/Rime/default.custom.yaml` — 方案配置（搜狗双拼）
- `~/Library/Rime/double_pinyin_sogou.schema.yaml` — 方案本体
- `~/Library/Rime/cn_dicts/` — 6 个中文词库
- `~/Library/Rime/en_dicts/` — 英文混输词库

现在请注销登录，如果遇到任何问题，欢迎回来咨询。