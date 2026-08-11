---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chinese Shuangpin Input Methods on Ubuntu
translated: false
type: note
---

Question: What Chinese Shuangpin (双拼) input methods can be used on Ubuntu/Linux?

Answer:

On Ubuntu/Linux, the best options are usually based on **Fcitx5** or **IBus**. For **双拼**, Fcitx5 currently has the better experience.

## Option 1: Fcitx5 + Chinese Shuangpin (recommended)

Install:

```bash
sudo apt update
sudo apt install fcitx5 fcitx5-chinese-addons fcitx5-configtool
```

Set Fcitx5 as input framework:

```bash
im-config -n fcitx5
```

Log out and log in again.

Open configuration:

```bash
fcitx5-configtool
```

Add:

```
Add Input Method
  -> Chinese
      -> Pinyin
```

Then configure:

```
Pinyin → Shuangpin
```

Fcitx5 supports many schemes:

* Microsoft Shuangpin (微软双拼)
* Ziranma (自然码)
* Xiaohe (小鹤双拼)
* Ziguang (紫光双拼)
* ABC (智能ABC)
* Sogou-style

Example:

```
小明
```

Normal pinyin:

```
xiao ming
```

Xiaohe Shuangpin:

```
xm
```

---

## Option 2: IBus + Pinyin

Ubuntu default often uses IBus.

Install:

```bash
sudo apt install ibus-pinyin
```

Configure:

```
Settings
 -> Keyboard
 -> Input Sources
 -> Chinese (Pinyin)
```

IBus supports some double-pinyin modes, but customization is weaker than Fcitx5.

---

## Option 3: Rime (中州韵) — for power users

If you want the most customizable setup:

```bash
sudo apt install fcitx5-rime
```

Rime supports:

* 小鹤双拼
* 自然码
* 五笔
* 自定义词库
* Cloud input
* Personal dictionary

Config files:

```
~/.local/share/fcitx5/rime/
```

Example:

```yaml
# double_pinyin_flypy.schema.yaml

schema:
  schema_id: double_pinyin_flypy
  name: 小鹤双拼
```

Rime is closer to a programmable input engine.

---

For a developer who uses Linux daily, I would choose:

```
Ubuntu
  |
  +-- Fcitx5
       |
       +-- Rime
             |
             +-- 小鹤双拼
```

It gives a similar feeling to advanced Windows Chinese input methods while remaining fully Linux-native.
