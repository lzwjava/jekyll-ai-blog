---
audio: false
generated: false
image: false
lang: en
layout: post
title: Code Review Web
translated: false
type: post
---

This is the README.md from github project [https://github.com/lzwjava/code-review-web](https://github.com/lzwjava/code-review-web).

---

# code-review-web

CodeReview is a professional platform for code review, communication, and sharing. Engineers can submit their code for expert review to improve the quality of their code. It was founded by 6 Internet lovers, including me.

![img](./img/cr1.jpg)

![img](./img/cr2.jpg)

# Projects

* [code-review-server](https://github.com/lzwjava/code-review-server)
* [code-review-web](https://github.com/lzwjava/code-review-web)

### Building

``` bash
npm install
# watch:
node server.js
# build:
npm run build
# deploy
npm run deploy
# submodule
git submodule init
git submodule update
```

### Debug

将 apitest.conf 复制到 /usr/local/nginx/conf/sites/ 下面。在 nginx.conf 中引入 sites/*.conf。重启 nginx。

### Contributors

| author  | commits |
| ------------- | ------------- |
| lzwjava  | 302 |
| LeslieYQ | 73  |
|Martin|52|
|zangqilong|4|
