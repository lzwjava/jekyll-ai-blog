---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Wechaty 测试脚本修复指南
translated: true
type: note
---

## 📁 创建的文件

**`test.js`** — 一个完整、自包含的可运行测试脚本，修复了你原始代码中的几个问题：

| 你的原始代码 | 问题 | 我的修复 |
|---|---|---|
| `import { Wechaty } from 'wechaty'` | 新 API 推荐使用 `WechatyBuilder` | 切换为 `WechatyBuilder.build()` |
| `new Wechaty({ name })` | 缺少 `puppet` 参数 | 显式设置 `puppet: 'wechaty-puppet-wechat'` |
| `config` / `initDay()` | 未定义 → 导致崩溃 | 已移除 |
| `let bot = ''` | 类型错误 | 直接使用 `const bot` |
| 仅登录/登出 | 无法测试功能 | 添加了消息接收 + 自动回复，并在登录后自动向自己发送一条测试消息 |

## 📦 安装的依赖项

- `wechaty@1.20.2`
- `wechaty-puppet-wechat@1.18.4`（关键依赖）
- `qrcode-terminal@0.12.0`
- 在 `package.json` 中添加了 `"type": "module"`，以便 `import` 语法能够正常工作

## ▶️ 如何运行

```bash
cd /Users/lzwjava/projects/wechaty-test

# 选项 A：脚本已指定 puppet，无需设置环境变量
node test.js

# 选项 B：或通过环境变量指定（你的原始方式）
WECHATY_PUPPET=wechaty-puppet-wechat node test.js
```

## ✅ 预期结果

1. 终端显示微信登录二维码（或你可以扫描它打印的在线链接 `https://wechaty.js.org/qrcode/...`）
2. 用手机微信扫描二维码 → 控制台打印 `贴心小助理 xxx 登录成功 ✅`
3. 机器人的微信账号会自动向你发送一条 `Hello! 我是你的微信小助手 🤖` 消息
4. 任何向机器人发送消息的好友都会收到自动回复
5. 扫描一次后，登录数据会保存到 `wechat-puppet-wechat.memory-card.json`，下次无需再次扫描

⚠️ **注意：** 个人微信网页版登录（`wechaty-puppet-wechat`）存在一定的账号限制风险。如果大量使用，请考虑更稳定/付费的 puppet。需要我同时编写一个配套的 `README.md` 吗？