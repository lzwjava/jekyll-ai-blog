---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 鼠须管macOS双拼
translated: true
type: note
---

**问题：** macOS 上有没有开源的双拼输入法？我目前使用微信输入法，但希望换成一个开源的。

**回答：**

答案是 **RIME / 鼠须管 (Squirrel)**——这是最权威的开源选择，并且内置了完善的双拼支持。

---

## RIME (鼠须管) — 唯一真正的答案

RIME 是一个高度可定制的跨平台（Windows、Mac、Linux）开源输入法引擎。它开箱即用就能提供良好的用户体验，并且包含你需要的所有字符。在 macOS 上，其前端称为 **鼠须管 (Squirrel)**，由 Rime 输入法引擎及其他开源技术驱动。

GitHub: [rime/squirrel](https://github.com/rime/squirrel)

---

## 安装

```bash
brew install --cask squirrel
```

然后退出并重新登录。进入 **系统设置 → 键盘 → 文字输入 → 编辑**，搜索 "Squirrel"，添加到输入法列表。

---

## 启用双拼

RIME 内置了多种双拼方案。最常用的几种：

| 方案 ID | 布局 |
|---|---|
| `double_pinyin` | 自然码 (Ziranma) |
| `double_pinyin_flypy` | 小鹤 (Xiaohe/Flypy) — 目前最流行 |
| `double_pinyin_mspy` | 微软双拼 (Microsoft) |
| `double_pinyin_abc` | 智能ABC |
| `double_pinyin_thunisoft` | 紫光 |

创建 `~/.config/rime/default.custom.yaml`（macOS 上为 `~/Library/Rime/default.custom.yaml`）：

```yaml
patch:
  schema_list:
    - schema: double_pinyin_flypy   # 或使用 double_pinyin 表示自然码
```

然后点击 RIME 菜单栏图标 → **重新部署 (Deploy)**。完成。

---

## 推荐：Weasel/Rime + 雾凇拼音词典以获得更好的词库覆盖

默认词典比较精简。社区维护的 **雾凇拼音 (rime-ice)** 提供了约 220 万词条：

```bash
# 安装 rime-ice 方案包
cd ~/Library/Rime
curl -fsSL https://git.io/rime-install | bash -s -- iDvel/rime-ice:others/recipes/full
```

或手动安装：[iDvel/rime-ice](https://github.com/iDvel/rime-ice) — 多数高级用户都在使用此方案。它预配置了小鹤双拼方案并带有庞大词库。

---

## 快速配置示例 (`~/Library/Rime/squirrel.custom.yaml`)

```yaml
patch:
  # 候选窗口样式
  style/horizontal: false
  style/font_face: "PingFang SC"
  style/font_point: 16
  style/candidate_list_layout: linear
```

---

## 总结

- **鼠须管 (Squirrel / RIME)** — 100% 开源（BSD/GPL），积极维护，内置双拼，拥有庞大的社区方案生态。
- Apple 自带双拼确实存在，但如你所想是闭源的。
- 微信输入法：闭源，会向腾讯回传数据——对于注重隐私的开发工作流来说并不理想。

RIME 是中国黑客/程序员社区的标准选择。安装后，前往系统设置 → 键盘 → 文字输入 → 编辑，搜索“中文”并添加“Squirrel”到输入法选项。初始设置大约需要 10 分钟，之后完全本地运行，可通过 YAML 完全自定义，且无任何遥测。

**参考：**

- [rime/squirrel — GitHub](https://github.com/rime/squirrel)
- [iDvel/rime-ice — 雾凇拼音（大词库 + 双拼配置）](https://github.com/iDvel/rime-ice)
- [在 macOS 上配置 Rime — bdim.moe](https://blog.bdim.moe/posts/configuring-rime-input-method-on-macos/)
