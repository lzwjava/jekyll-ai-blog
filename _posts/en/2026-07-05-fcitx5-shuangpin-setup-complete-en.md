---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fcitx5 Shuangpin Setup Complete
translated: false
type: note
---

All set. Here's the summary:

---

## Shuangpin (双拼) in Fcitx5 — Done

**What was configured**:

| Setting | Value |
| --------- | ------- |
| Pinyin mode | `PinyinMode=Shuangpin` — always starts in shuangpin mode |
| Shuangpin scheme | `ShuangpinProfile=MS` — Microsoft 双拼 layout |
| Show indicator | `ShowShuangpinMode=True` — shows mode in candidate popup |

**Config files**:

- `/home/lzw/.config/fcitx5/profile` — input method group: `keyboard-us` + `pinyin`, default is `pinyin`
- `/home/lzw/.config/fcitx5/conf/pinyin.conf` — engine mode set to `Shuangpin`

**How to use on the workstation**:

- `Ctrl+Space` — toggle between English (keyboard-us) and Chinese shuangpin
- Type `n` + `i` → outputs `你` (Microsoft scheme: `n`=ni, `i`=i)

**Available Shuangpin schemes** (change `ShuangpinProfile` in pinyin.conf):

- `MS` — 微软双拼 (default)
- `Ziranma` — 自然码
- `Xiaohe` — 小鹤
- `Sogou` — 搜狗
- `Ziwei` — 紫光
- `ABC` — 智能ABC
- `Guobiao` — 国标
- `Pinyin++` — 拼音加加

**To switch scheme**:

```bash
sed -i 's/ShuangpinProfile=MS/ShuangpinProfile=Xiaohe/' ~/.config/fcitx5/conf/pinyin.conf
# Then restart fcitx5
```

**To toggle on/off via GUI** when physically on the machine: `fcitx5-config-qt` → Pinyin → Double Pinyin tab.
