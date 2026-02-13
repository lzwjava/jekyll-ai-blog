---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Node.js 多部分表单数据流
translated: true
type: note
---

**Question:** form-data npm package 的作用是什么？

**Answer:**

**form-data** npm package 是一个流行的 Node.js 库，用于创建 **multipart/form-data** 编码的 streams。这种格式通常用于提交包含文件（文件上传）的 HTML 表单，或者通过 HTTP POST 请求发送混合数据（文本字段 + 二进制文件）。

在浏览器中，你可以使用原生的 **FormData** API 来准备此类数据。然而，Node.js（尤其是较旧的版本）没有内置的 FormData 类来生成正确的 multipart streams，因此 **form-data** 填补了这一空白。

### 主要用途

- 它允许你通过编程方式构建 **multipart/form-data** body
- 它创建一个 readable stream，你可以将其直接 pipe 到 **axios**、**node-fetch**、**request**（较旧）、**undici** 或原生的 **http/https** module 等库
- 它自动处理 boundary 生成、headers 以及文本字段、buffers、streams 和文件的正确格式化

### 典型使用示例

```js
const FormData = require('form-data');
const fs = require('fs');
const https = require('https');

const form = new FormData();
form.append('username', 'john_doe');
form.append('avatar', fs.createReadStream('profile.jpg'));
form.append('bio', 'Hello world');

// 获取 headers (包括 Content-Type: multipart/form-data; boundary=xxxx)
const headers = form.getHeaders();

const req = https.request({
  hostname: 'example.com',
  path: '/upload',
  method: 'POST',
  headers: headers
});

form.pipe(req);

req.on('response', (res) => {
  console.log('Status:', res.statusCode);
});
```

许多 HTTP client 库会自动与其集成：

```js
// axios 示例
axios.post('https://example.com/upload', form, {
  headers: form.getHeaders()
});
```

### 现代替代方案 (2025–2026 背景)

自 **Node.js 18+** 起，已经存在原生的 **`FormData`** 类，可以与 **`fetch()`** 或 **undici** 等现代 clients 一起使用。许多项目现在更倾向于使用原生方案而不是 **form-data** package，原因如下：

- 它与浏览器 FormData API 规范保持一致
- 无需额外的 dependency
- 在最近的 Node 版本中对 Blob/File 有更好的支持

然而，**form-data** package 在遗留代码库、支持旧版 Node 版本的项目或需要特定 streaming 行为的情况下，仍然被广泛使用（每周有数亿次下载）。

**注意 (security)**：在 2025 年中期，**4.0.0–4.0.3** 版本存在与弱 boundary 生成相关的严重漏洞 (CVE-2025-7783)。如果你继续使用此 package，请使用 **≥4.0.4**（或旧分支中的 ≥3.0.4 / ≥2.5.4）。

**References:**

- [https://www.npmjs.com/package/form-data](https://www.npmjs.com/package/form-data)
- [https://github.com/form-data/form-data](https://github.com/form-data/form-data)