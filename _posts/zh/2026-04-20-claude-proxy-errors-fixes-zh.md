---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude代理错误与修复方案
translated: true
type: note
---

问题：为什么自定义Claude API代理返回“400 Bad Request”错误提示该接口仅用于Claude Code客户端，且后续尝试为何因凭证缺失或API密钥错误而失败？

回答：

## 根本原因分析

您遇到了**三个连续发生的问题**。具体分析如下：

---

### 问题一：代理拒绝请求（400 Bad Request）

```
默认渠道限制：请求非法 接口仅可用于Claude Code客户端
（如误判请修改CC客户端版本 其他渠道不限）
```

**问题原因：**

`https://claude2.sssaicode.com/api` 上的代理是一个**第三方API转售/中继服务**。它会检查HTTP请求头部，以验证调用方是否为合法的Claude Code客户端。它会检查以下头部信息：

- `User-Agent`——必须与官方Claude Code CLI的格式一致
- `anthropic-version`
- `x-api-key`格式或令牌类型

您的自定义`claw`工具未发送符合要求的头部信息，因此无法通过检查。

**解决方案：** 错误信息本身提供了线索——“如误判请修改CC客户端版本”。您需要将客户端的`User-Agent`或版本头部设置为与官方Claude Code发送的一致。

---

### 问题二：凭证缺失（在取消环境变量后）

```
错误：缺少Anthropic凭证；请导出ANTHROPIC_AUTH_TOKEN或ANTHROPIC_API_KEY
```

出现此问题是因为您的第二次尝试运行**在`export ANTHROPIC_API_KEY=`命令之后**——该命令将密钥设置为**空字符串**，且您的shell会话可能已丢失该值。工具因此正确报告了凭证缺失的错误。

---

### 问题三：OpenAI API密钥错误（401 Unauthorized）

```
提供的API密钥不正确：999VUv4m**...8MZq
```

当您切换到`--model openai/gpt-4.1-mini`时，工具正确地路由到OpenAI的API——但它使用了您的`OPENAI_API_KEY`，而该密钥在OpenAI平台上**已失效或过期**。密钥`999VUv4m...`很可能是由代理/转售商提供的密钥，而非真实的OpenAI密钥。

---

## 问题总结表

| 错误类型 | 原因 | 解决方案 |
| --- | --- | --- |
| 代理返回400 | `claw`未发送Claude Code客户端头部 | 添加正确的`User-Agent`/客户端版本头部 |
| 凭证缺失 | `ANTHROPIC_API_KEY`被设置为空值 | 重新导出有效密钥 |
| OpenAI返回401 | `OPENAI_API_KEY`是代理密钥，非真实OpenAI密钥 | 将`OPENAI_BASE_URL`设置为代理的OpenAI兼容端点 |

---

## 推荐解决方案

若代理支持OpenAI兼容端点，请尝试：

```bash
export OPENAI_API_KEY=<您的代理密钥>
export OPENAI_BASE_URL="https://claude2.sssaicode.com/api"   # 或其OpenAI兼容路径
./target/debug/claw prompt "say hello" --model openai/claude-opus-4-6
```

或者，如果您希望将其用作Anthropic端点，则需要让`claw`发送模仿官方Claude Code客户端的头部信息——特别是正确的`User-Agent`，可能还需要添加`x-claude-code-version`头部。
