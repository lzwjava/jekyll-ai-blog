---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu上的中文双拼输入法
translated: true
type: note
---

问题：在Ubuntu/Linux上可以使用哪些中文双拼输入法？

回答：

在Ubuntu/Linux上，最佳选择通常基于**Fcitx5**或**IBus**。对于**双拼**，Fcitx5目前体验更好。

## 选项一：Fcitx5 + 中文双拼（推荐）

安装：

```bash
sudo apt update
sudo apt install fcitx5 fcitx5-chinese-addons fcitx5-configtool
```

将Fcitx5设置为输入框架：

```bash
im-config -n fcitx5
```

注销并重新登录。

打开配置：

```bash
fcitx5-configtool
```

添加：

```
添加输入法
  -> 中文
      -> 拼音
```

然后配置：

```
拼音 → 双拼
```

Fcitx5支持多种方案：

* 微软双拼
* 自然码
* 小鹤双拼
* 紫光双拼
* 智能ABC
* 搜狗风格

示例：

```
小明
```

普通拼音：

```
xiao ming
```

小鹤双拼：

```
xm
```

---

## 选项二：IBus + 拼音

Ubuntu默认常使用IBus。

安装：

```bash
sudo apt install ibus-pinyin
```

配置：

```
设置
 -> 键盘
 -> 输入源
 -> 中文（拼音）
```

IBus支持一些双拼模式，但自定义能力弱于Fcitx5。

---

## 选项三：Rime（中州韵）—— 面向高级用户

如果你想要最可定制的方案：

```bash
sudo apt install fcitx5-rime
```

Rime支持：

* 小鹤双拼
* 自然码
* 五笔
* 自定义词库
* 云输入
* 个人词典

配置文件：

```
~/.local/share/fcitx5/rime/
```

示例：

```yaml
# double_pinyin_flypy.schema.yaml

schema:
  schema_id: double_pinyin_flypy
  name: 小鹤双拼
```

Rime更像一个可编程的输入引擎。

---

对于日常使用Linux的开发者，我会选择：

```
Ubuntu
  |
  +-- Fcitx5
       |
       +-- Rime
             |
             +-- 小鹤双拼
```

这提供了类似高级Windows中文输入法的体验，同时完全保持Linux原生。
