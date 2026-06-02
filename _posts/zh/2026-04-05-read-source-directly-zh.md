---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 《阿凡达：水之道》
translated: true
type: note
---

问题：直接克隆 OpenClaw 源代码并阅读是否更好，而不需要 Claude Code？

回答：

是的——实际上这是**最简单、最直接的方法**。你完全不需要 Claude Code。

## 为什么直接阅读源代码在这里就足够了

你已经知道：
- ✅ Webhook 签名验证正常
- ✅ Nextcloud 正在发送 webhook
- ✅ OpenClaw 能接收到它们
- ✅ 丢弃原因是 `(no mention)`

所以你只需要**在源代码中找到该字符串**并追踪其相关逻辑。

## 直接这样做即可

```bash
git clone https://github.com/openclaw/... openclaw
cd openclaw

# 找到确切的丢弃条件
grep -r "no mention" .
grep -r "drop" . --include="*.php"
grep -r "mention" . --include="*.php"
```

就这样。`grep` 会精确定位到具体的文件和行。然后你阅读周围 20–50 行代码，就能确切知道机器人要求什么条件。

## Claude Code 在这里是大材小用

Claude Code 在以下情况下很有价值：
- 代码库庞大且不熟悉
- 需要跨多个文件追踪逻辑
- 希望 AI **解释**复杂的逻辑

但在你的情况中——一个具有已知日志信息的具体丢弃条件——**使用 grep + 阅读相关函数**比启动 Claude Code 更快速、更直接。

## 总结

| 方法 | 适用场景 |
|---|---|
| `grep` + 直接阅读源码 | ✅ 你目前的情况 |
| Claude Code | 大型不熟悉的代码库、复杂的跨文件追踪 |
| 网络搜索 / 文档 | 初始设置，而非运行时逻辑 |

你是对的。克隆它，grep 它，阅读它。完成。
