---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyPI 命名空间与拼写劫持风险
translated: true
type: note
---

不，不完全对。PyPI（官方 Python Package Index）的工作方式如下：

**任何人都可以发布 packages，但仅限于自己的 namespace：**
- 你在 pypi.org 创建一个免费账户
- 你可以发布任何名称未被占用的 package
- 一旦你拥有一个 package 名称，只有你（以及你授予访问权限的协作者）可以发布新版本

**防止滥用的机制：**
- Package 名称是先到先得
- 你不能向他人拥有的名称发布
- PyPI 有针对 name squatting 和 typosquatting 的政策
- Malicious packages 会被报告并移除，但没有 pre-screening

**真正的风险——typosquatting：**
- 攻击者注册类似于流行 packages 的名称（例如，`reqeusts` 而非 `requests`）
- 这是已知的一种 supply chain attack vector
- PyPI 有 tooling 来检测并移除明显案例，但它是 reactive 而非 proactive

**所以答案是：** 是的，任何人都可以发布 packages，但你不能 overwrite 或 hijack 你不拥有的现有 package。危险在于新名称/相似名称，而不是接管已建立的 ones。

这就是为什么从不受信任来源或带有拼写错误的 `pip install` 可能有风险。