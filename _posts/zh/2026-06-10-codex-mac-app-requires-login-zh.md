---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Codex Mac 应用需要登录
translated: true
type: note
---

不。Codex Mac 应用确实需要认证。

根据当前官方 Codex 文档，当你首次打开应用时，应“使用你的 ChatGPT 账户或 OpenAI API 密钥登录”，Codex 支持这两种登录方式：ChatGPT 登录或 API 密钥登录。来源：[Codex 应用入门](https://developers.openai.com/codex/app)，[认证与会话](https://developers.openai.com/codex/auth)。

可能让人困惑的是：一旦登录过一次，Codex 会将你的凭据缓存到本地并在后续重复使用，因此在之后的启动中可能看起来“无需登录”。文档指出，应用/CLI/IDE 会缓存登录详情，ChatGPT 会话在活跃期间会自动刷新。来源：[认证与会话](https://developers.openai.com/codex/auth)。

所以简要总结如下：
- 首次使用：是的，需要登录。
- 后续使用：可能不再提示，因为应用记住了你的登录。

如果你愿意，我也可以在一分钟内解释 `ChatGPT 登录` 和 `API 密钥登录` 的区别。