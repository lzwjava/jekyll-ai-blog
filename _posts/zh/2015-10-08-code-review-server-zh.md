---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 代码审核服务器
translated: true
type: post
---

这是来自 GitHub 项目 [https://github.com/lzwjava/code-review-server](https://github.com/lzwjava/code-review-server) 的 README.md。

---

# code-review-server

CodeReview 是一个专业的代码评审、沟通和分享平台。工程师可以将他们的代码提交给专家评审，以提高代码质量。它由包括我在内的 6 名互联网爱好者创立。

![img](./img/cr1.jpg)

![img](./img/cr2.jpg)

# 项目

* [code-review-server](https://github.com/lzwjava/code-review-server)
* [code-review-web](https://github.com/lzwjava/code-review-web)

# 部署

部署: fab -H root@reviewcode.cn deploy

安装依赖: composer install, composer update

# API

- `GET /user/self`
- `DELETE /user/tags/:tagId`
- `POST /user/tags`
- `POST /orders`
- `GET /user/orders`
- `GET /orders/:orderId`
- `POST /orders/:orderId`
- `POST /orders/:orderId`
- `POST /orders/:orderId/reward`
- `GET /qiniu/token`
- `GET /reviewers`
- `GET /reviewers/:reviewerId`
- `POST /reviews`
- `PATCH /reviews/:reviewId`
- `GET /reviews`
- `GET /reviewers/:reviewerId/reviews`
- `POST /reviews/:reviewId/visits`
- `GET /videos`
- `POST /videos/:videoId/visits`
- `DELETE /orders/:orderId`
- `POST /user/requestResetPassword`
- `POST /user/resetPassword`
