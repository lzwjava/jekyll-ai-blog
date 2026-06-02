---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何查找你的Hugging Face注册日期
translated: true
type: note
---

公共个人资料页面不直接显示注册日期。以下是您的选项：

**1. 账户设置（最简单）**
登录HF，进入设置 → 账户。注册/加入日期应列在那里。

**2. 从公开信息来看：**
您的活动页面显示最早记录的操作是“喜欢了12个模型，超过1年前”——因此您注册了**至少1年以上**（在2025年5月之前的某个时间）。但这只是一个下限，并不精确。

**3. HF API（如果想用脚本）**
```bash
curl https://huggingface.co/api/users/lzwjava
```
这会返回包含账户元数据的JSON，其中包括`createdAt`时间戳。

**4. 检查模型时间戳**
如果您有较旧的模型，它们的创建日期会提供线索。但您只有`zz`，它是全新的。

设置页面最快——只需直接点击HF上的头像 → 设置。
