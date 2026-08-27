---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wechaty Setup Successful
translated: false
type: note
---

All four commands executed successfully. Here's the summary:

## ✅ Commands run

1. **`npm install qrcode-terminal --save`** — installed `qrcode-terminal@0.12.0`
2. **`npm install wechaty`** — installed `wechaty@1.20.2`
3. **`npm install wechaty-puppet-wechat --save`** — installed `wechaty-puppet-wechat@1.18.4` (the key one)
4. **`export WECHATY_PUPPET=wechaty-puppet-wechat`** — saved to `.env-puppet` (the env var only affects the current terminal session, so I saved it to a file you can `source`)

## 📌 `package.json` now contains

```json
"dependencies": {
    "qrcode-terminal": "^0.12.0",
    "wechaty": "^1.20.2",
    "wechaty-puppet-wechat": "^1.18.4"
}
```

Note: `npm audit` shows some warnings (mostly from old transitive deps in `wechaty-puppet-wechat`), but that's expected and won't block running the bot.

## ▶️ Now run the test

```bash
cd /Users/lzwjava/projects/wechaty-test
node test.js
```

The script already hardcodes `puppet: 'wechaty-puppet-wechat'` inside `test.js`, so you don't strictly need the env var. But if you want to set it for the session:

```bash
source .env-puppet   # sets WECHATY_PUPPET
node test.js
```

The terminal will show a login QR code — scan it with your phone WeChat and the bot will log in, send you a test message, and auto-reply to friends.
