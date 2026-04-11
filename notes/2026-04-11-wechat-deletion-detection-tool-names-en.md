---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Deletion Detection Tool Names
translated: false
type: note
---

Question:
What are the Chinese names of those WeChat deletion-detection tools like WechatRealFriends, WeFriends, and PC hook / iPad protocol tools?

Answer:

Here are the commonly used **Chinese names** for those tools:

### 1. WechatRealFriends

Chinese name:

* **微信好友检测**
* **微信单向好友检测**
* **微信真实好友检测**
* Sometimes also called: **RealFriends 好友检测工具**

People usually refer to it casually as:

> “微信好友检测工具”
> “单向好友检测工具”

---

### 2. WeFriends (GitHub open-source)

Chinese name:

* **WeFriends 单向好友检测工具**
* **开源微信好友检测工具**
* **微信群拉人检测脚本**

Some communities call it:

> “WeFriends 微信好友检测”
> “微信群拉人检测工具”

It works by:

* 创建临时群
* 检测无法拉入的人
* 判断谁删除你

---

### 3. PC hook tools

Chinese name:

* **PC 端 Hook 微信工具**
* **PC 版微信插件**
* **微信 PC Hook**
* **Windows 微信 Hook 检测工具**

These usually:

* hook WeChat.exe
* read friend relationship
* batch operations

风险较高。

---

### 4. iPad protocol tools

Chinese name:

* **iPad 协议微信**
* **iPad 协议检测工具**
* **协议号微信**
* **多开协议微信**
* **iPad 登录协议工具**

These are the **most risky** type.

They:

* simulate iPad login
* read contacts
* detect deletion
* batch operations

Often bundled in:

* 微商工具
* 客户管理工具
* 群发工具

---

### Risk ranking (from low → high)

Manual group detection
↓
WeFriends (开源)
↓
WechatRealFriends
↓
PC Hook 工具
↓
iPad 协议工具（最高风险）

---

My recommendation for you:

Best balance:

> **WeFriends（开源）**

Because:

* transparent
* no binary injection
* easier to audit
* engineer-friendly

Avoid:

> iPad 协议工具

These are most likely to:

* trigger 风控
* temporarily block account
* require SMS verification

If you'd like, I can also:

* recommend safest GitHub repo
* explain how detection works internally
* show how to write your own script

Your background makes it very doable.