---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wechaty Test Script Fix Guide
translated: false
type: note
---

## 📁 Files created

**`test.js`** — a complete, self-contained runnable test script, which fixes several issues in your original code:

| Your original code | Issue | My fix |
| --- | --- | --- |
| `import { Wechaty } from 'wechaty'` | New API recommends `WechatyBuilder` | Switched to `WechatyBuilder.build()` |
| `new Wechaty({ name })` | Missing the `puppet` parameter | Explicitly set `puppet: 'wechaty-puppet-wechat'` |
| `config` / `initDay()` | Undefined → crashes | Removed |
| `let bot = ''` | Wrong type | Used `const bot` directly |
| Only login/logout | Can't test features | Added message receive + auto-reply, and auto-sends a test message to yourself after login |

## 📦 Dependencies installed

- `wechaty@1.20.2`
- `wechaty-puppet-wechat@1.18.4` (the key one)
- `qrcode-terminal@0.12.0`
- Added `"type": "module"` to `package.json` so the `import` syntax works

## ▶️ How to run

```bash
cd /Users/lzwjava/projects/wechaty-test

# Option A: the script already specifies the puppet, no env var needed
node test.js

# Option B: or specify via environment variable (your original approach)
WECHATY_PUPPET=wechaty-puppet-wechat node test.js
```

## ✅ What to expect

1. Terminal shows the WeChat login QR code (or you can scan the online `https://wechaty.js.org/qrcode/...` link it prints)
2. Scan the QR code with your phone's WeChat → console prints `贴心小助理 xxx 登录成功 ✅`
3. The bot's WeChat account will auto-send you a `Hello! 我是你的微信小助手 🤖` message
4. Any friend who messages the bot gets an auto-reply
5. After scanning once, login data is saved to `wechat-puppet-wechat.memory-card.json`, so the next time you won't need to scan again

⚠️ **Note:** Personal WeChat web-based login (`wechaty-puppet-wechat`) carries some risk of account restriction. If you use it heavily, consider a more stable/paid puppet. Want me to also write a matching `README.md`?
