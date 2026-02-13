---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Node.js Multipart Form Data Streams
translated: false
type: note
---

**Question:** What does the form-data npm package do?

**Answer:**

The **form-data** npm package is a popular Node.js library that helps create **multipart/form-data** encoded streams. This format is commonly used when submitting HTML forms that include files (file uploads) or when sending mixed data (text fields + binary files) via HTTP POST requests.

In browsers, you can use the native **FormData** API to prepare such data. However, Node.js (especially older versions) did not have a built-in FormData class that could generate proper multipart streams, so **form-data** fills this gap.

### Main purpose
- It lets you build a **multipart/form-data** body programmatically
- It creates a readable stream that you can pipe directly to libraries like **axios**, **node-fetch**, **request** (older), **undici**, or raw **http/https** module
- It automatically handles boundary generation, headers, and proper formatting of text fields, buffers, streams, and files

### Typical usage example

```js
const FormData = require('form-data');
const fs = require('fs');
const https = require('https');

const form = new FormData();
form.append('username', 'john_doe');
form.append('avatar', fs.createReadStream('profile.jpg'));
form.append('bio', 'Hello world');

// Get headers (includes Content-Type: multipart/form-data; boundary=xxxx)
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

Many HTTP client libraries integrate with it automatically:

```js
// axios example
axios.post('https://example.com/upload', form, {
  headers: form.getHeaders()
});
```

### Modern alternatives (2025–2026 context)
Since **Node.js 18+**, a native **`FormData`** class exists and can be used with **`fetch()`** or modern clients like **undici**. Many projects now prefer it instead of the **form-data** package because:

- It's spec-compliant with the browser FormData API
- No extra dependency needed
- Better Blob/File support in recent Node versions

However, the **form-data** package is still widely used (hundreds of millions of weekly downloads) in legacy codebases, projects supporting older Node versions, or when specific streaming behavior is needed.

**Note (security)**: In mid-2025, versions **4.0.0–4.0.3** had a critical vulnerability (CVE-2025-7783) related to weak boundary generation. Use **≥4.0.4** (or ≥3.0.4 / ≥2.5.4 in older branches) if you continue using this package.

**References:**

- [https://www.npmjs.com/package/form-data](https://www.npmjs.com/package/form-data)
- [https://github.com/form-data/form-data](https://github.com/form-data/form-data)