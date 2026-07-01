---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 代码评审网
translated: true
type: post
---

这是来自 GitHub 项目 [https://github.com/lzwjava/code-review-web](https://github.com/lzwjava/code-review-web) 的 README.md。

---

# code-review-web

CodeReview 是一个专业的代码审查、沟通和分享平台。工程师可以提交他们的代码以供专家审查，以提高代码质量。它由包括我在内的 6 名互联网爱好者创立。

![img](./img/cr1.jpg)

![img](./img/cr2.jpg)

# 项目

* [code-review-server](https://github.com/lzwjava/code-review-server)
* [code-review-web](https://github.com/lzwjava/code-review-web)

### 构建

``` bash
npm install
# 监视:
node server.js
# 构建:
npm run build
# 部署
npm run deploy
# 子模块
git submodule init
git submodule update
```

### 调试

将 apitest.conf 复制到 /usr/local/nginx/conf/sites/ 下面。在 nginx.conf 中引入 sites/*.conf。重启 nginx。

### 贡献者

| 作者 | 提交 |
| ------------- | ------------- |
| lzwjava | 302 |
| LeslieYQ | 73 |
| Martin | 52 |
| zangqilong | 4 |
