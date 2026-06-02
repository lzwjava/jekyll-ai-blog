---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RIME搜狗双拼设置总结
translated: true
type: note
---

以下是设置完成后的全面总结，以及您现在拥有的内容：

---

## 已安装的内容

**鼠须管 (Squirrel) v1.1.2** — RIME 输入法引擎的 macOS 前端。

- 通过 `brew install --cask squirrel` 安装
- 位置：`/Library/Input Methods/Squirrel.app`
- 配置目录：`~/Library/Rime/`

**雾凇拼音 (rime-ice)** — 社区维护的最佳 RIME 词典/方案包。

- 通过 plum (RIME 包管理器) 安装至 `~/Library/Rime/`
- 来源：[iDvel/rime-ice](https://github.com/iDvel/rime-ice)

---

## ~/Library/Rime/ 目录下的内容

```
default.custom.yaml              ← 你的方案选择（搜狗双拼）
double_pinyin_sogou.schema.yaml  ← 搜狗双拼方案（来自 rime-ice）
cn_dicts/                        ← 6 本中文词典（约 220 万词）
  ├── 41448.dict.yaml            ← 41,448 个最常用汉字
  ├── 8105.dict.yaml             ← 8,105 个标准汉字（GB2312+）
  ├── base.dict.yaml             ← 基础词典
  ├── ext.dict.yaml              ← 扩展词汇
  ├── others.dict.yaml           ← 补充词条
  └── tencent.dict.yaml          ← 腾讯语料（现代流行语、人名）
en_dicts/                        ← 英文混输词典
  ├── en.dict.yaml               ← 英文单词
  ├── en_ext.dict.yaml           ← 扩展英文
  └── cn_en_sogou.txt            ← 中英混输术语（搜狗专用）
lua/                             ← Lua 插件（自动大写、日期、表情等）
opencc/                          ← OpenCC（表情、繁简转换）
squirrel.yaml                    ← Squirrel 外观配置（来自 rime-ice）
symbols_v.yaml                   ← 按 V 键调出符号选择器
symbols_caps_v.yaml              ← CapsLock+V 调出更多符号
custom_phrase.txt                ← 你的自定义短语（为空，待你填写）
```

---

## 开箱即用的功能

| 功能 | 使用方法 |
|---|---|
| 搜狗双拼 | 正常输入即可——这是你的默认方案 |
| 海量词典 | 220 万+中文词，现代流行语、网络用语 |
| 英文混输 | 无需切换即可直接输入英文单词（如输入 "hello" 即可） |
| 表情输入 | 输入表情的中文名称，即可获得表情候选 |
| 符号选择器 | 按 `V` 再按某个按键，调出符号（箭头、数学、货币等） |
| 日期/时间 | 输入 `rq`（日期）出日期，`sj`（时间）出时间，`xq`（星期）出星期几 |
| 自定义短语 | 编辑 `~/Library/Rime/custom_phrase.txt` 添加自己的短语 |
| 繁体中文 | 内置 OpenCC 转换可用 |

---

## 常用快捷键（默认 Squirrel 按键绑定）

| 快捷键 | 动作 |
|---|---|
| `Ctrl+Space` 或 `Ctrl+`` | 切换输入法（macOS 系统） |
| `Shift` | 切换中/英文 |
| `Enter` | 直接上屏原始拼音 |
| `Escape` | 清空当前输入 |
| `[` / `]` | 上/下翻页候选词 |
| `Shift+Enter` | 直接上屏为大写英文 |
| `Ctrl+.` | 切换全/半角标点 |

---

## RIME 部署流程

每当你编辑 `~/Library/Rime/` 中的任何文件后：

1. 点击菜单栏中的 Squirrel 图标
2. 点击 **"重新部署" (Deploy)**
3. 等待编译（首次约 10-30 秒，之后即时完成）

或使用键盘快捷键：`Ctrl+Option+``（如果已配置）。

---

## 个性化技巧

**外观** — 编辑 `~/Library/Rime/squirrel.custom.yaml`：

```yaml
patch:
  style/font_face: "PingFang SC"
  style/font_point: 16
  style/horizontal: false          # 竖排候选列表
  style/candidate_format: "%c. %@" # 显示数字标签
```

**添加更多输入方案** — 编辑 `~/Library/Rime/default.custom.yaml`：

```yaml
patch:
  schema_list:
    - schema: double_pinyin_sogou
    - schema: rime_ice          # 全拼作为备选
```

**自定义短语** — 编辑 `~/Library/Rime/custom_phrase.txt`：

```
# 格式：词<Tab>拼音<Tab>优先级
github	github	100
```

**更新 rime-ice**（拉取最新词典/方案）：

```bash
cd ~/Library/Rime && bash plum/bin/rime-install iDvel/rime-ice:others/recipes/full
```

---

## 从微信输入法切换的原因

- 微信输入法闭源，且会向腾讯回传数据
- Squirrel 完全本地运行，零遥测，全离线
- 所有配置均为纯 YAML — 可版本控制、可移植
- 搜狗双拼的手感可以直接迁移（按键映射相同）

---

## 登录后的后续步骤

1. 注销 / 重新登录
2. 系统设置 → 键盘 → 文字输入 → 编辑 → 添加 "Squirrel"
3. 通过菜单栏或 `Ctrl+`` 切换到 Squirrel
4. 点击"重新部署"（重新部署） — 等待词典编译
5. 开始输入 — 应能看到搜狗双拼正常工作，且候选词丰富
