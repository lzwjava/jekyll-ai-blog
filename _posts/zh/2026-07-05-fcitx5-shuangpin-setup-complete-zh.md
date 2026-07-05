---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Fcitx5双拼设置完成
translated: true
type: note
---

完成。以下是摘要：

---

## Fcitx5 中的双拼配置 — 已完成

**配置内容**：

| 设置项 | 值 |
| -------- | ----- |
| 拼音模式 | `PinyinMode=Shuangpin` — 始终以双拼模式启动 |
| 双拼方案 | `ShuangpinProfile=MS` — 微软双拼布局 |
| 显示指示器 | `ShowShuangpinMode=True` — 在候选词弹窗中显示模式 |

**配置文件**：

- `/home/lzw/.config/fcitx5/profile` — 输入法组：`keyboard-us` + `pinyin`，默认使用 `pinyin`
- `/home/lzw/.config/fcitx5/conf/pinyin.conf` — 引擎模式设置为 `Shuangpin`

**在工作站上使用**：

- `Ctrl+Space` — 切换英文（keyboard-us）与中文双拼
- 输入 `n` + `i` → 输出 `你`（微软方案：`n`=ni, `i`=i）

**可用的双拼方案**（修改 pinyin.conf 中的 `ShuangpinProfile`）：

- `MS` — 微软双拼（默认）
- `Ziranma` — 自然码
- `Xiaohe` — 小鹤
- `Sogou` — 搜狗
- `Ziwei` — 紫光
- `ABC` — 智能ABC
- `Guobiao` — 国标
- `Pinyin++` — 拼音加加

**切换方案**：

```bash
sed -i 's/ShuangpinProfile=MS/ShuangpinProfile=Xiaohe/' ~/.config/fcitx5/conf/pinyin.conf
# 然后重启 fcitx5
```

**在机器上通过图形界面开关**：`fcitx5-config-qt` → 拼音 → 双拼选项卡。
