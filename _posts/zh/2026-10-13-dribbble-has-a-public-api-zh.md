---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Dribbble 拥有公开 API
translated: true
type: note
---

**问题：** Dribbble 有 API 吗？

**回答：** 是的，Dribbble 有一个公共 API。

以下是关键细节：

- **官方文档：** `https://developer.dribbble.com`
- **身份验证：** 该 API 使用 OAuth 进行身份验证，这比简单的 API 密钥更复杂，但提供了更好的安全性，尤其是在访问用户数据时。
- **费用：** Dribbble 被列为免费公共 API。
- **状态：** 截至 2026 年 4 月，该 API 响应正常。
- **你可以做什么：** 它允许你管理 shots、创建项目、上传附件和发表评论。
- **协议：** 仅支持 HTTPS；CORS 支持未记录在案，因此如果你在浏览器中遇到跨域错误，请尝试从你的服务器调用 API。

**参考资料：**

- [Dribbble Developer Portal](https://developer.dribbble.com)
- [API Bouncer – Dribbble](https://www.apibouncer.com/apis/1190/dribbble)
