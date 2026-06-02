---
audio: false
generated: false
image: false
lang: en
layout: post
title: Code Review Server
translated: false
type: post
---

This is the README.md from github project [https://github.com/lzwjava/code-review-server](https://github.com/lzwjava/code-review-server).

---

# code-review-server

CodeReview is a professional platform for code review, communication, and sharing. Engineers can submit their code for expert review to improve the quality of their code. It was founded by 6 Internet lovers, including me.

![img](./img/cr1.jpg)

![img](./img/cr2.jpg)

# Projects

* [code-review-server](https://github.com/lzwjava/code-review-server)
* [code-review-web](https://github.com/lzwjava/code-review-web)

# Deploy

Deploy: fab -H root@reviewcode.cn deploy

Install dependencies: composer install, composer update

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
