---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Wechaty 设置成功
translated: true
type: note
---

所有四条命令均成功执行。以下是总结：

## ✅ 已执行的命令

1. **`npm install qrcode-terminal --save`** — 已安装 `qrcode-terminal@0.12.0`
2. **`npm install wechaty`** — 已安装 `wechaty@1.20.2`
3. **`npm install wechaty-puppet-wechat --save`** — 已安装 `wechaty-puppet-wechat@1.18.4`（关键依赖）
4. **`export WECHATY_PUPPET=wechaty-puppet-wechat`** — 已保存至 `.env-puppet`（该环境变量仅影响当前终端会话，因此我已将其保存到文件中，你可以通过 `source` 命令加载）

## 📌 `package.json` 现在包含

```json
"dependencies": {
    "qrcode-terminal": "^0.12.0",
    "wechaty": "^1.20.2",
    "wechaty-puppet-wechat": "^1.18.4"
}
```

注意：`npm audit` 显示了一些警告（主要来自 `wechaty-puppet-wechat` 的旧传递依赖），但这是预期行为，不会影响机器人运行。

## ▶️ 现在运行测试

```bash
cd /Users/lzwjava/projects/wechaty-test
node test.js
```

脚本中已在 `test.js` 内硬编码了 `puppet: 'wechaty-puppet-wechat'`，因此严格来说无需环境变量。但如果你想为当前会话设置该变量，可以执行：

```bash
source .env-puppet   # 设置 WECHATY_PUPPET
node test.js
```

终端将显示登录二维码——用手机微信扫描后，机器人将登录，向你发送一条测试消息，并自动回复好友。
